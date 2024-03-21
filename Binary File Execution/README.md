README for my_cmd.c

===================================
Custom Command Execution Program
===================================

This C program is designed to execute a binary executable file with specified command line options either in the foreground or in the background.

Compilation:
------------
To compile the program, ensure that you have GCC (GNU Compiler Collection) installed on your system. Then, follow these steps:

1. Open a terminal and navigate to the directory containing the source code (my_cmd.c) and the Makefile.

2. Run the following command:
make
This command will compile the program and generate the executable file named "my_cmd".

Usage:------
Once the program is compiled, you can run it with various command-line options.

Syntax:
./my_cmd [options]

Options:
--------
The program supports the following options:

1. '-e': Specifies the path to the executable file to be executed.

2. '-o': Specifies the options string to be passed to the executable file. The options string should be enclosed in double quotes ("") if it contains spaces or special characters.

3. '-f': Specifies foreground mode. The program waits for the child process to finish before continuing execution.

4. '-b': Specifies background mode. The program continues execution immediately after forking the child process.

Examples:
---------
1. Execute a command in foreground mode:
./my_cmd -e /bin/ls -o "-l -a" -f
This command executes the "ls" command with the options "-l -a" in foreground mode.

2. Execute a command in background mode:
./my_cmd -e /bin/ls -o "-l -a" -b
This command executes the "ls" command with the options "-l -a" in background mode.

3. Execute command of any order provided all the necessary arguments are given . 
./my_cmd -e /bin/ls -o "-l -a" -f
            or
./my_cmd -o "-l -a" -e /bin/ls -f  
            or 
./my_cmd -f -o "-l -a" -e /bin/ls 
All the three commands give same output. 

4. Execute the program itself with nested quotes in options:

This command executes the "my_cmd" program with the options "-e /usr/bin/ls -o '-l -a' -f". Note the use of nested quotes to properly handle the options.

5. Execute a command with multiple options:
./my_cmd -e /bin/cat -o "file1.txt file2.txt" -f
This command executes the "cat" command to concatenate the contents of "file1.txt" and "file2.txt" in foreground mode.

Program Behavior:
-----------------
- The Program first parses through the command line, checking if the required command line arguments (the pathname of the executable and the b/f control option) are given as well as their validity. It also extracts any options of the executable that are within a length of 100.
- After parsing the arguments, the program forks a child process using the fork() system call. If there is a fork failure, an error code is returned. This child process is responsible for executing the specified executable using the execve() system call.
- Depending on the mode (-b for background or -f for foreground), the parent process either waits for the child process to finish or continues execution immediately.
- If the execution fails, an error is returned.
- After the child process terminates, the program prints the command line, process ID of the child, exit code of the child (if any), and any error information.

Note:
-----
- Minimum of 4 arguments are expected from the command line 
- '-e' option should be immediately followed by <binary_file_path> name. It is also compulsory to provide this option.
- '-o' option should be immediately followed by <string_of_options_seperated_by_space>. It is optional to provide this option. 
- Either of '-b' or '-f' is mandatory to provide. If both the options are provided then the option with the largest index value in the 'argv[]' will be taken as mode. 
    Example: ./my_cmd -e /usr/bin/ls -o '-l -a' -f -b  // Here the '-b' option is assigned to mode.
             ./my_cmd -e /usr/bin/ls -o '-l -a' -b -f  // Here the '-f' option is assigned to mode.
- ./my_cmd -e ./my_cmd -f -o "-e /usr/bin/ls -o '-l -a' -f" // This should not give the desired output because if parent process runs in foreground mode, it will wait for the child process to finish before continuing execution.
  ./my_cmd -e ./my_cmd -d -o "-e /usr/bin/ls -o '-l -a' -d" // But this will give the desired output. 

Compatibility:
--------------
This program is designed to work on any recent GNU/Linux system, such as Ubuntu 22.04 LTS.

Author:
-------
Keeran Dhami 
Sneh Pahuja
