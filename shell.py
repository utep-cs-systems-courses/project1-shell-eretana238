#! /usr/bin/env python3

import os, sys, re

def tokenize(command):
    pass

commands = ['ls', 'cd', 'sort']

prompt_string = '$ '
try:
    if not os.environ['PS1']:
        prompt_string = os.environ['PS1']
except KeyError as error:
    print("Unexpected error: ", error)

while True:
    user_input = input(prompt_string)
    if user_input.startswith('exit'):
        sys.exit(0)