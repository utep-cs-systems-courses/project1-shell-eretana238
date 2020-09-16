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
        if len(command) > 1:
            try: 
                os.chdir(command[1])
            except FileNotFoundError: 
                print('-bash: cd: %s: No such directory' % command[1])
            except NotADirectoryError:
                print('-bash: cd: %s: No such directory' % command[1])

# checks and executes builtin commands "cd" and "exit"
def exec_command(commands):
    for dir in re.split(":", os.environ['PATH']): 
        program = "%s/%s" % (dir, commands[0])
        try:
            os.execve(program, commands, os.environ)
        except FileNotFoundError:
            pass

def redirect(args,n):
    os.close(n)                 # redirect child's stdout
    if n == 0:
        os.open(args[-1], os.O_RDONLY);
    else:
        os.open(args[-1], os.O_CREAT | os.O_WRONLY);
    os.set_inheritable(n, True)

def run_process(args):
    rc = os.fork()

    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)

    elif rc == 0:                   # child
        if '>' in args:
            redirect(args,1)
            exec_command(args)
            os.write(2, ("Child:    Error: Could not exec %s\n" % args[0]).encode())
            sys.exit(1)
        elif '<' in args:
            redirect(args,0)
            exec_command(args)
            os.write(2, ("Child:    Error: Could not exec %s\n" % args[0]).encode())
            sys.exit(1)
        elif '|' in args:
            os.close(1)                 # redirect child's stdout
            os.dup(pw)
            for fd in (pr, pw):
                print(fd)
                os.close(fd)
            print("hello from child")
        elif '/' in args[0]:
            try:
                os.execve(args[0], args, os.environ)
            except FileNotFoundError:
                pass
        else:
            exec_command(args)

    else:                           # parent (forked ok)
        if '|' in args:
            os.close(0)
            os.dup(pr)
            for fd in (pw, pr):
                os.close(fd)
            for line in fileinput.input():
                print("From child: <%s>" % line)
        else:
            childPidCode = os.wait()
            if childPidCode[1] % 256 != 0:
                os.write(1, ("Program terminated with exit code %d\n" % 
                    childPidCode[1]).encode())

while True:
    pid = os.getpid()

    prompt_string = get_ps1()
    
    args = re.split(' ', input(prompt_string).strip())
    # make sure to continue prompt in empty string
    if args[0] == '':
        continue

    exec_builtins(args)

    run_process(args)

    
