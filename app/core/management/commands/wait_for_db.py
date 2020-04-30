import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """ Django command - stop the processs until the db is available """

    def handle(self, *arg, **options):
        self.stdout.write('waiting for database ...')

        con = None
        while not con:
            try:
                con = connections['default']
            except OperationalError:
                self.stdout.write('Database unavailable,wait 1 secound ...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available.'))
