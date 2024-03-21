neh Pahuja and Ananya Pandit

# Command-Line Based C Program to Copy Files 


# Project Description

C Program:
After declaring variables for the input and output file paths and descriptors, the program loops through the command line argument and stores the input and output file paths. If there are any errors in the command line usage(for example the user types in -h instead of -i), the program returns an exit code and the error is printed out on standard error by the BASH shell script. After the command line arguments are parsed, it checks whether the input and ouput file path are null. After handling that the program handles the standard input case by assigning the file descriptor to 0. It does the same later for the standard output case assigning the output file descriptor to 1. After the file descriptors are set in both cases the file are opened for reading and writing respectively with appropriate permissions being set. To ensure that the reading buffer is the exact size required, first the size of the the input file is found through fstat, and then memory is allocated for the buffer accordingly. There are further error handling cases for memory management issues and writing issues. The files are closed and the allocated memory is freed before returning exit codes. If there are no errors the program returns 0.

# Usage 
Without makefile:  ./flame_cp -i input_file.c -o output_file.c
Without makefile(with BASH): ./errors.sh ./flame_cp -i input_file.c -o output_file.c

With makefile: make run ARGS="-i input_file.c -o output_file.c 
