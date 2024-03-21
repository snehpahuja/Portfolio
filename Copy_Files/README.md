Sneh Pahuja and Ananya Pandit

# Single File Operations

# Project Description

C Program:
The c program uses switch case to parse through the command line. This switch case in place of the if else is more for the readability of the code. For errno error codes, rather than rewriting the process each time, we've written the block at the end, and the program just goes to the block directly. When renaming the file, the filename is updated, so that if more than one operation is mentioned on the command line, the new filename is the most current version. Before any operation commands the filename has to be specified. This is standards for all operations to simplify the process. For deleting files and empty directories, there is a system call called remove that utilises two others to handle cases for both files(unlink) and empty directories(rmdir). Before appending to files, there is a checker to see whether the file is binary or text (through looking for a null character while reading the file). Instead of mallocing space for the buffer to read, we have kept a standard file size of 1024 bytes. For appending to files, there are two cases. When appending text, the process is quite straightforward(appending the buffer to the file). For appending the odd numbers, first there is a check to make sure it is within the specified range(50-200). Then the sequential odd numbers are calculated till 200. The number of odd numbers is also stored. Once the array of values is created and filled, the array is appended to the file.Even though there is a check for binary file, we have kept two separate commands for clarity purposes. Error handling is taken care of every time a system call is used.

# Usage

To create a file:
With makefile: make run ARGS="-n input_file.c -cf"

To create a directory:
With makefile: make run ARGS="-n input_file.c -cd"

To rename file or directory:
With makefile: make run ARGS="-n filename -r newname"

To delete file or empty directory:
With makefile: make run ARGS="-n filename -d"

To write first 50 bytes of file to standard ouput:
With makefile: make run ARGS="-n filename -w"

To append to file 50 bytes of text:
With makefile: make run ARGS="-n filename -at 'string of text'"

To append to file 50 bytes of odd numbers:
With makefile: make run ARGS="-n filename -ab starting_number"
