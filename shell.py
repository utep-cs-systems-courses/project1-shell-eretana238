#! /usr/bin/env python3

import os, sys, re

def tokenize(command):
    pass

commands = ['cd', 'ls', 'sort']
while True:
    prompt = input('$ ')
    if prompt == 'exit':
        sys.exit(0)
    
