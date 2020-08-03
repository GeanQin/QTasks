#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from crontab import CronTab

class CronManager:

    def __init__(self):
        self.cron = CronTab(user=True)
    
    def addCron(self, task, time, id, who):
        job = self.cron.new(command=task)
        job.setall(time)
        job.set_comment(id)
        self.cron.write_to_user(user=who)

    def deleteCron(self, id, who):
        self.cron.remove_all(comment=id)
        self.cron.write_to_user(user=who)
