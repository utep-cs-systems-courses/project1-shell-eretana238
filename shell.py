#! /usr/bin/env python3

import os, sys, re

commands = ['ls', 'cd', 'sort']

prompt_string = '$ '
if 'PS1' in os.environ:
    prompt_string = os.environ['PS1']

while True:
    user_input = input(prompt_string)
    args = re.split('\W+\s', user_input)
    if args[0] == 'exit':
        sys.exit(0)

    # rc = os.fork()
    
    # if rc < 0:
    #     os.write(2, ("fork failed, returning %d\n" % rc).encode())
    #     sys.exit(1)

    # elif rc == 0:                   # child
    #     os.close(1)                 # redirect child's stdout
    #     os.open("p4-output.txt", os.O_CREAT | os.O_WRONLY);
    #     os.set_inheritable(1, True)

    #     for dir in re.split(":", os.environ['PATH']): # try each directory in path
    #         program = "%s/%s" % (dir, args[0])
    #         try:
    #             os.execve(program, args, os.environ) # try to exec program
    #         except FileNotFoundError:             # ...expected
    #             pass                              # ...fail quietly 

    #     os.write(2, ("Child: Error: Could not exec %s\n" % args[0]).encode())
    #     sys.exit(1)          
    # else:                           # parent (forked ok)
    #     os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" % 
    #                 (pid, rc)).encode())
    #     childPidCode = os.wait()
    #     os.write(1, ("Parent: Child %d terminated with exit code %d\n" % 
    #                 childPidCode).encode())