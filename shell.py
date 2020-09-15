#! /usr/bin/env python3

import os, sys, re, fileinput

pid = os.getpid()               # get and remember pid

pr,pw = os.pipe()
for f in (pr, pw):
    os.set_inheritable(f, True)

builtin_cmd = ['cd','exit']

prompt_string = '$ '
if 'PS1' in os.environ:
    prompt_string = os.environ['PS1']

def has_redirects(user_input):
    return '>' in user_input or '<' in user_input

def has_pipes(user_input):
    return '|' in user_input

# checks and executes builtin commands "cd" and "exit"
def exec_builtin(command):
    if command[0] not in builtin_cmd:
        return
    if command[0] == 'exit':
        sys.exit(0)
    elif command[0] == 'cd': 
        cwd = os.getcwd()
        if len(command) > 1:
            try: 
                os.chdir(os.path.join(cwd,command[1]))
            except FileNotFoundError: 
                print('-bash: cd: %s: No such file or directory' % command[1])
            except NotADirectoryError:
                os.chdir(cwd)
    return 0

def exec_command(commands):
    for dir in re.split(":", os.environ['PATH']): 
        program = "%s/%s" % (dir, commands[0])
        try:
            os.execve(program, commands, os.environ) 
        except FileNotFoundError:
            pass
    return

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

def parse_pipe(user_input):
    cmd1, cmd2 = None
    if '|' in user_input:
        cmd1, cmd2 = user_input.split('|',1)


while True:
    user_input = input(prompt_string)
    if not user_input:
        continue
    # check for more complex commands
    args = None
    redirect_args = None
    pipe_args = None
    if has_redirects(user_input):
        redirect_args = parse_redirect(user_input)
    elif has_pipes(user_input):
        pipe_args = parse_pipe(user_input)
    else:
        args = re.split(' ', user_input)
        exec_builtin(args)


    rc = os.fork()

    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)

    elif rc == 0:                   # child
        if redirect_args:
            if redirect_args[1]:
                os.close(1)                 # redirect child's stdout
            else:
                os.close(0)
            os.open(redirect_args[1], os.O_CREAT | os.O_WRONLY);
            os.set_inheritable(1, True)
            exec_command(list(redirect_args[0]))
            sys.exit(1)
        if pipe_args:
            os.close(1)                 # redirect child's stdout
            os.dup(pw)
            for fd in (pr, pw):
                print(fd)
                os.close(fd)
            print("hello from child")
        else:
            exec_command(args)
            sys.exit(1)
    else:                           # parent (forked ok)
        if redirect_args:
            childPidCode = os.wait()
            if childPidCode[1] % 256 != 0:
                os.write(1, ("Program terminated with exit code %d\n" % childPidCode[1]).encode())

        elif pipe_args:
            os.close(0)
            os.dup(pr)
            for fd in (pw, pr):
                os.close(fd)
            for line in fileinput.input():
                print("From child: <%s>" % line)
        else:
            childPidCode = os.wait()
            if childPidCode[1] % 256 != 0:
                os.write(1, ("Program terminated with exit code %d\n" % childPidCode[1]).encode())
