
import random
import string

from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
import time
import re
from hackerspace.notify import notify
from hackerspace.git import add_issue

# define what to do when an error occures, on the website (backend) or in one of the cronjobs


def getErrorName(error_log):
    # get error name
    lines = error_log.split('\n')
    lines_length = len(lines)

    # go over the last rows and see if Error is in line, if true, save as name
    str_name = None
    counter = 1
    while str_name == None and counter < lines_length:
        last_line = lines_length-counter
        counter += 1
        if 'Error:' in lines[last_line]:
            str_name = lines[last_line]
            break
    if not str_name:
        str_name = 'New Error'

    return str_name


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
            'str_name': output['exc_value'] if 'exc_value' in output else getErrorName(error_log),
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
    str_name = models.CharField(max_length=250, blank=True, null=True)
    int_count = models.IntegerField(default=0)
    text_description = models.TextField(blank=True, null=True)
    text_description_no_numbers = models.TextField(blank=True, null=True)
    json_context = JSONField(default=list, blank=True, null=True)
    boolean_fixed = models.BooleanField(default=False)
    list_origins = ArrayField(models.CharField(
        max_length=250, blank=True, null=True), blank=True, null=True)  # URLs and .py scripts
    list_dateUNIXtimes = ArrayField(models.IntegerField(
        blank=True, null=True), blank=True, null=True)
    date_created = models.DateTimeField('published', auto_now_add=True)
    date_updated = models.DateTimeField('last_updated', auto_now=True)

    def __str__(self):
        if self.str_name:
            return self.str_name
        elif self.text_description:
            return self.text_description
        else:
            return 'New Error'

    def create_or_update(self):
        context = {}

        # get error information from system
        new_error_details = getErrorDetails(
            error_log=self.json_context['error_log'],
            exc_type=self.json_context['exc_type'],
            exc_value=self.json_context['exc_value'],
            tb=self.json_context['tb']
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
            str_name=new_error_details['str_name']).first()

        # if found_error, update it
        if found_error:
            found_error.boolean_fixed = False

            if self.json_context['origin'] not in found_error.list_origins:
                found_error.list_origins.insert(
                    0, self.json_context['origin'])

            # overwrite error message
            found_error.text_description = new_error_details['text_log']

            # add the 5 most recent contexts as examples
            found_error.json_context.insert(0, context)
            found_error.json_context = found_error.json_context[:5]

            found_error.list_dateUNIXtimes.insert(0, time.time())

            found_error.save()

            # send notification
            if len(found_error.list_dateUNIXtimes) == 10:
                notify(json_context={
                    'str_what': 'error_repeated_10',
                    'str_error_code': self.str_error_code,
                    'str_name': self.str_name
                })
            elif len(found_error.list_dateUNIXtimes) == 100:
                notify(json_context={
                    'str_what': 'error_repeated_100',
                    'str_error_code': self.str_error_code,
                    'str_name': self.str_name
                })
            elif len(found_error.list_dateUNIXtimes) == 1000:
                notify(json_context={
                    'str_what': 'error_repeated_1000',
                    'str_error_code': self.str_error_code,
                    'str_name': self.str_name
                })

            return found_error

        # else create a new entry
        else:
            self.str_name = new_error_details['str_name']
            self.text_description = new_error_details['text_log']
            self.list_origins = [self.json_context['origin']]
            self.list_dateUNIXtimes = [time.time()]
            self.json_context = [context]

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
                'str_name': self.str_name
            })

            return self

    def save(self, *args, **kwargs):
        self.int_count = len(self.list_dateUNIXtimes)

        if not self.str_name:
            self = self.create_or_update()

        super(Error, self).save(*args, **kwargs)

        return self
