#!/usr/bin/env python
from __future__ import absolute_import, unicode_literals

import os
import sys
import environ

# Load operating system environment variables and then prepare to use them
env = environ.Env()
root = environ.Path(__file__) - 1
env_file = root('.env')
if os.path.exists(env_file):
    # Operating System Environment variables have precedence over variables defined in the .env file,
    # that is to say variables from the .env files will only be used if not defined as environment variables.
    print('Loading : {}'.format(env_file))
    env.read_env(env_file)
    print('The .env file has been loaded. See base.py for more information')

DJANGO_SETTINGS_MODULE = env.str('DJANGO_SETTINGS_MODULE', default="config.settings.production")

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS_MODULE)

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
