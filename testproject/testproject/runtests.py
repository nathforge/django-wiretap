#!/usr/bin/env python

import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'testproject.settings'

sys.path.insert(0, os.path.dirname(__file__))

import django
from django.conf import settings
from django.test.utils import get_runner

def main():
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=False)
    failures = test_runner.run_tests(['wiretap'])
    sys.exit(1 if failures else 0)

if __name__ == '__main__':
    main()
