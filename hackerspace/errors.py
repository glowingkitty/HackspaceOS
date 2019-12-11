
import json
import random
import re
import string
import time

from django.db import models

from hackerspace.git import add_issue
from hackerspace.notify import notify

# define what to do when an error occures, on the website (backend) or in one of the cronjobs


def getErrorName(error_log):
    # get error name
    lines = error_log.split('\n')
    lines_length = len(lines)

    # go over the last rows and see if Error is in line, if true, save as name
    str_name_en_US = None
    counter = 1
    while str_name_en_US == None and counter < lines_length:
        last_line = lines_length-counter
        counter += 1
        if 'Error:' in lines[last_line]:
            str_name_en_US = lines[last_line]
            break
    if not str_name_en_US:
        str_name_en_US = 'New Error'

    return str_name_en_US


def clearFromNumbers(message):
    # remove line numbers (line 000) in Error model
    line_numbers = re.findall("(line \d{1,})", message)
    for line_number in line_numbers:
        message = message.replace(line_number, 'line XXX')

    # remove version numbers ([00]) to search for in Error model
    doc_numbers = re.findall("(\[\d{1,}\])", message)
    for doc_number in doc_numbers:
        message = message.replace(doc_number, '[XXX]')

    return message


def getErrorDetails(error_log=None, exc_type=None, exc_value=None, tb=None):
    error = {}

    if tb is not None:
        prev = tb
        curr = tb.tb_next
        while curr is not None:
            prev = curr
            curr = curr.tb_next

        output = prev.tb_frame.f_locals
        error = {
            'text_log': error_log,
            'str_name_en_US': output['exc_value'] if 'exc_value' in output else getErrorName(error_log),
            'json_variables': {}
        }
        ignore = ['self', 'options', 'sys', 'traceback',
                  'error_message', 'exc_type', 'exc_value', 'tb', 'args']
        for field in output:
            if field not in ignore:
                error['json_variables'][field] = str(output[field])

    return error


class ErrorSet(models.QuerySet):
    def unsolved(self):
        return self.filter(boolean_fixed=False)


class Error(models.Model):
    objects = ErrorSet.as_manager()
    str_error_code = models.CharField(
        max_length=250, unique=True, blank=True, null=True)
    str_name_en_US = models.CharField(max_length=250, blank=True, null=True)
    int_count = models.IntegerField(default=0)
    text_description_en_US = models.TextField(blank=True, null=True)
    text_description_no_numbers = models.TextField(blank=True, null=True)
    text_context = models.TextField(blank=True, null=True)
    boolean_fixed = models.BooleanField(default=False)
    text_origins = models.TextField(
        blank=True, null=True)  # URLs and .py scripts
    text_dateUNIXtimes = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField('published', auto_now_add=True)
    date_updated = models.DateTimeField('last_updated', auto_now=True)

    def __str__(self):
        if self.str_name_en_US:
            return self.str_name_en_US
        elif self.text_description_en_US:
            return self.text_description_en_US_en_US
        else:
            return 'New Error'

    def create_or_update(self):
        json_context = json.loads(self.text_context)
        context = {}

        # get error information from system
        new_error_details = getErrorDetails(
            error_log=json_context['error_log'],
            exc_type=json_context['exc_type'],
            exc_value=json_context['exc_value'],
            tb=json_context['tb']
        )
        try:
            context['json_variables'] = new_error_details['json_variables']
        except:
            print('Failed to save json_variables')

        # clear message from numbers to check better for already existing errors
        error_log_no_numbers = clearFromNumbers(
            new_error_details['text_log'])

        # check if error already exists
        found_error = Error.objects.filter(
            str_name_en_US=new_error_details['str_name_en_US']).first()

        # if found_error, update it
        if found_error:
            found_error.boolean_fixed = False

            if json_context['origin'] not in found_error.text_origins:
                found_error.text_origins = json_context['origin'] + \
                    ','+found_error.text_origins

            # overwrite error message
            found_error.text_description_en_US = new_error_details['text_log']

            # add the 5 most recent contexts as examples
            found_error.text_context.insert(0, context)
            found_error.text_context = found_error.text_context[:5]

            found_error.text_dateUNIXtimes = str(
                time.time())+','+found_error.text_dateUNIXtimes

            found_error.save()

            # send notification
            if len(found_error.text_dateUNIXtimes.split(',')) == 10:
                notify(json_context={
                    'str_what': 'error_repeated_10',
                    'str_error_code': self.str_error_code,
                    'str_name_en_US': self.str_name
                })
            elif len(found_error.text_dateUNIXtimes.split(',')) == 100:
                notify(json_context={
                    'str_what': 'error_repeated_100',
                    'str_error_code': self.str_error_code,
                    'str_name_en_US': self.str_name
                })
            elif len(found_error.text_dateUNIXtimes.split(',')) == 1000:
                notify(json_context={
                    'str_what': 'error_repeated_1000',
                    'str_error_code': self.str_error_code,
                    'str_name_en_US': self.str_name
                })

            return found_error

        # else create a new entry
        else:
            self.str_name_en_US = new_error_details['str_name_en_US']
            self.text_description_en_US = new_error_details['text_log']
            self.text_origins = json_context['origin']
            self.text_dateUNIXtimes = str(time.time())
            self.text_context = str(context)

            # generate random str_error_code
            random_string = ''.join(random.choice(
                string.ascii_lowercase + string.digits) for x in range(7))

            # check if random str_error_code already exists
            while Error.objects.filter(str_error_code=random_string).count() > 0:
                random_string = ''.join(random.choice(
                    string.ascii_lowercase + string.digits) for x in range(7))

            self.str_error_code = random_string

            super(Error, self).save()

            # add issue to github
            add_issue(self)

            # send notification
            notify(json_context={
                'str_what': 'error_new',
                'str_error_code': self.str_error_code,
                'str_name_en_US': self.str_name
            })

            return self

    def save(self, *args, **kwargs):
        self.int_count = len(self.text_dateUNIXtimes.split(','))

        if not self.str_name_en_US:
            self = self.create_or_update()

        super(Error, self).save(*args, **kwargs)

        return self
