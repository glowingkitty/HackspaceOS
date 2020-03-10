from crontab import CronTab
import getpass
import time
import os


class Cronjob():
    def __init__(self):
        self.logs = ['self.__init__']
        self.started = round(time.time())
        self.crontab = CronTab(user=getpass.getuser())

    def log(self, text):
        from _setup.models import Log
        self.logs.append(text)
        Log().print('{}'.format(text), os.path.basename(__file__), self.started)

    def setup(self):
        # check if all jobs from cronjobs.txt already exist, else create them
        cronjobs_file = open("_setup/cronjobs.txt", "r")
        for line in cronjobs_file:
            command = line.split('* ')[-1].replace('\n', '')
            timing = line.split(command)[0]
            if timing.endswith(' '):
                timing = timing[:-1]

            for job in self.crontab:
                if job.command == command:
                    break
            else:
                self.add(command, timing)
        self.log('-> Done')

    @property
    def schedule(self):
        import datetime
        for job in self.crontab:
            sch = job.schedule(date_from=datetime.datetime.now())
            self.log('{} (Next: {})'.format(job, sch.get_next()))

    @property
    def jobs(self):
        jobs = []
        for job in self.crontab:
            jobs.append(job)
        return jobs

    @property
    def count(self):
        return len(self.jobs)

    def add(self, command, timing):
        job = self.crontab.new(command=command)
        job.setall(timing)

        self.crontab.write()
        self.log('-> Added cronjob: '+command)

    def delete(self, command):
        for job in self.crontab:
            if job.command == command:
                self.crontab.remove(job)
                self.crontab.write()
                self.log('-> Deleted cronjob: '+command)
                break

    def delete_all(self):
        for job in self.crontab:
            self.crontab.remove(job)
        self.crontab.write()
        self.log('-> Deleted all cronjobs.')
