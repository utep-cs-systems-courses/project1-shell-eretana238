#! /usr/bin/env python3

import os, re, sys

def get_ps1():
    if 'PS1' in os.environ:
        return os.environ['PS1']
    return '$ '

def exec_builtins(command):
    if command[0] == 'exit':
        sys.exit(0)
    elif command[0] == 'cd': 
        cwd = os.getcwd()
        if len(command) > 1:
            try: 
                os.chdir(command[1])
            except FileNotFoundError: 
                print('-bash: cd: %s: No such file or directory' % command[1])

# checks and executes builtin commands "cd" and "exit"
def exec_command(command):
    for dir in re.split(":", os.environ['PATH']): 
        program = "%s/%s" % (dir, command[0])
        try:
            os.execve(program, command, os.environ)
        except FileNotFoundError:
            pass
        
# parese redirect provided by os instructors
def parse_redirect(user_input):
    output_file = None
    input_file = None
    cmd = ''
 
    if '>' in user_input:
        [cmd, output_file] = user_input.split('>',1)
        output_file = output_file.strip()
 
    elif '<' in cmd:
        [cmd, input_file] = cmd.split('<', 1)
        input_file = input_file.strip()
    
    elif output_file != None and '<' in output_file:
        [output_file, input_file] = output_file.split('<', 1)
        
        output_file = output_file.strip()
        input_file = input_file.strip()
        
    return cmd.split(), output_file, input_file

def run_process(args):
    rc = os.fork()

    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)

    elif rc == 0:                   # child
        exec_command(args)
        sys.exit(1)

    else:                           # parent (forked ok)
        childPidCode = os.wait()
        if childPidCode[1] % 256 != 0:
            os.write(1, ("Program terminated with exit code %d\n" % 
                childPidCode[1]).encode())

while True:
    pid = os.getpid()

    prompt_string = get_ps1()
    
    args = re.split(' ', input(prompt_string).strip())
    if not args:
        continue

    exec_builtins(args)

    run_process(args)

    
