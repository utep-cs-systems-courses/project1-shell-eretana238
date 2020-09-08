#! /usr/bin/env python3

import os, sys, re

pid = os.getpid()               # get and remember pid

prompt_string = '$ '
if 'PS1' in os.environ:
    prompt_string = os.environ['PS1']

while True:
    user_input = input(prompt_string)
    if not user_input:
        continue
    args = re.split(' ', user_input)
    if args[0] == 'exit':
        sys.exit(0)

    rc = os.fork()
    
    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)

    elif rc == 0:                   # child
        for dir in re.split(":", os.environ['PATH']): # try each directory in path
            program = "%s/%s" % (dir, args[0])
            try:
                print(os.execve(program, args, os.environ)) # try to exec program
            except FileNotFoundError:             # ...expected
                pass                              # ...fail quietly 

        sys.exit(1)          
    else:                           # parent (forked ok)
        childPidCode = os.wait()