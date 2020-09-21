## Unix Shell

Project that replicates the functionality of the bash shell. The shell is able to run builtin functions such as `exit`, and `cd`. Other commands are ran through `execve` using the os library part of python. The shell should be able to 

### Usage

To use the shell replica, python3 should be installed to run the program. Run the command below and the shell should start automatically. To finish the shell program, just type `exit`.

```
~project1-shell-eretana238> ./shell.py
```
or
```
~project1-shell-eretana238> python3 shell.py
```

The shell should be presented by a `$`, however if the `PS1` environment variable is changed, it should use that instead.

### Testing
For faster revising, `testShell.sh` was provided to test important commands and concepts such as piping, redirection and forking.

To test the shell, the commands below should do the trick.

```
~project1-shell-eretana238> ./shell/testShell.sh ./shell.py
```