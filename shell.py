#! /usr/bin/env python3

import os, sys, re

pid = os.getpid()               # get and remember pid

builtin_cmd = ['cd','exit']
prompt_string = '$ '
if 'PS1' in os.environ:
    prompt_string = os.environ['PS1']

def pipe_process():
    pass

def exec_builtin(in_str):
    if in_str not in builtin_cmd:
        return 0
    if in_str.startsWith('exit'):
        sys.exit(0)
    elif in_str.startsWith('cd'):
        pass
    return 0

def exec_command(commands):
    for dir in re.split(":", os.environ['PATH']): 
        program = "%s/%s" % (dir, commands[0])
        try:
            os.execve(program, args, os.environ) 
        except FileNotFoundError:
            pass

while True:
    user_input = input(prompt_string)
    if not user_input:
        continue
    args = re.split(' ', user_input)

    rc = os.fork()
    
    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)

    elif rc == 0:                   # child
        os.close(1)                 # redirect child's stdout
        # os.open("p4-output.txt", os.O_CREAT | os.O_WRONLY);
        # os.set_inheritable(1, True)

        exec_command(args)

        sys.exit(1)          
    else:                           # parent (forked ok)
        childPidCode = os.wait()
        os.write(1, ("Parent: Child %d terminated with exit code %d\n" % childPidCode).encode())