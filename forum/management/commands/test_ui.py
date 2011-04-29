import os
import glob
import logging
import subprocess

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

        # Loop through all args and try to get the python test files that match
        print args
        files = []
        for arg in args:
            matching_files = glob.glob('%s/%s.py' % (TEST_FOLDER, arg))
            for matching_file in matching_files:
                files.append(matching_file)

        # Loop through all test files
        for file in files:
            file_name = file.split('/')[-1]
            print "Starting test %s" % file_name
            child = subprocess.Popen('python %s' % file, shell=True)
