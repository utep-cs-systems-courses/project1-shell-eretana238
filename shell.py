#! /usr/bin/env python3

import os, re, sys

def get_ps1():
    if 'PS1' in os.environ:
        return os.environ['PS1']
    return "\033[1;34;40m %s\x1b[0m$ " % os.getcwd()

def exec_builtins(command):
    if command[0].lower() == 'exit':
        sys.exit(0)
    elif '&' in command:
        command.remove('&')
        return False
    elif command[0] == 'cd': 
        if len(command) > 1:
            try: 
                os.chdir(command[1])
            except FileNotFoundError: 
                os.write(1,('-bash: cd: %s: No such directory' % command[1]).encode())
            except NotADirectoryError:
                os.write(1,('-bash: cd: %s: No such directory' % command[1]).encode())
    return True
    
# checks and executes builtin commands "cd" and "exit"
def exec_command(command):
    for dir in re.split(":", os.environ['PATH']): 
        program = "%s/%s" % (dir, command[0])
        try:
            os.execve(program, command, os.environ)
        except FileNotFoundError:
            pass

def exec_pipe(args):
    cmd1 = args[:args.index('|')]
    cmd2 = args[args.index('|')+1:]

    pr,pw = os.pipe()
    for f in (pr, pw):
        os.set_inheritable(f, True)

    rc = os.fork()
    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)
    elif rc == 0:
        os.close(1)                 # redirect child's stdout
        os.dup(pw)
        os.set_inheritable(1, True)
        for fd in (pr, pw):
            os.close(fd)
        exec_command(cmd1)
        sys.exit(1)
    else:
        os.close(0)
        os.dup(pr)
        os.set_inheritable(0, True)
        for fd in (pw, pr):
            os.close(fd)
        if '|' in cmd2:
            exec_pipe(cmd2)
            sys.exit(1)
        exec_command(cmd2)

def redirect(args,n):
    os.close(n)                 # redirect child's stdout
    if n == 0:
        os.open(args[-1], os.O_RDONLY);
    else:
        os.open(args[-1], os.O_CREAT | os.O_WRONLY);
    os.set_inheritable(n, True)

def run_process(args, waiting):
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
            exec_pipe(args)
            sys.exit(1)
        elif '/' in args[0]:
            try:
                os.execve(args[0], args, os.environ)
            except FileNotFoundError:
                pass
        else:
            exec_command(args)
            sys.exit(1)
    else:                           # parent (forked ok)
        if waiting:
            childPidCode = os.wait()
            if childPidCode[1] % 256 != 0:
                os.write(1, ("Program terminated with exit code %d\n" % 
                    childPidCode[1]).encode())
                    
while True:
    waiting = True
    pid = os.getpid()
    os.write(1,get_ps1().encode())
    user_input = os.read(0,1000).decode()
    if not user_input:
        break
    commands = re.split('[\n]', user_input)
    while '' in commands: commands.remove('')
    while commands:
        args = re.split(' ', commands[0])
        while '' in args: args.remove('')
        if len(args) > 0:
            waiting = exec_builtins(args)
            run_process(args, waiting)
            commands.pop(0)
    