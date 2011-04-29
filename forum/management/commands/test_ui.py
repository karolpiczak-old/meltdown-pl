import os
import glob
import logging

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings as django_settings

from forum import settings

class Command(BaseCommand):
    args = '<test1 test2 test3 ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        # Try to load Selenium.
        try:
            import selenium
            print "Selenium has been successfully loaded"
        except ImportError:
            logging.error("Couldn't load selenium")
            exit("Python Selenium couldn't be loaded: pip install selenium")

        # Tests folder
        TEST_FOLDER = '%s/forum/skins/%s/tests' % (django_settings.SITE_SRC_ROOT, django_settings.OSQA_DEFAULT_SKIN)

        # Check if the UI tests folder exists
        if os.path.exists(TEST_FOLDER):
            print 'Loading UI tests from %s' % TEST_FOLDER
        else:
            exit("UI tests folder couldn't be loaded")