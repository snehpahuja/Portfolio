
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/stat.h>
#include <string.h>
#include <errno.h>

#define E_OK 0

int ec = E_OK;

int main(int argc, char *argv[]){

const char* filename = NULL;
int return_value,return_value_2,return_value_3, return_value_4;

//parsing command line
	for(int i = 1; i <argc; i++){
		switch(argv[i][1]) {
		    //for getting name of file/directory to be operated on
        	    case 'n':
                	if (i + 1 < argc) {
                        filename = argv[i + 1];
                        i++;
               		 }
               	    break;
		    //for creating
           	    case 'c':
			//for creating new file
                	if (argv[i][2] == 'f') {
                        	return_value = creat(filename, S_IRUSR | S_IWUSR | S_IRGRP |S_IWGRP | S_IROTH | S_IWOTH);
                        	if (return_value == -1) { goto error_handling; }
              	        } 
			//for creating new directory
			else if (argv[i][2] == 'd') {
                       		 return_value = mkdir(filename, S_IRUSR | S_IWUSR | S_IRGRP |S_IWGRP | S_IROTH | S_IWOTH);
                    		if (return_value == -1) { goto error_handling; }
              	        }
               	    break;
		    //for renaming file or directory 
           	    case 'r':
			//only going forward if there is an argument given after -r for the newname
               		 if (i + 1 < argc) {
                   		 const char *newname = argv[i + 1];
                   		 return_value = rename(filename, newname);
                         if (return_value == -1) { goto error_handling; }
			//replacing filename with newname in case futher operations are specified in the same command line
                 	filename = newname;
               		 }
			i++;
                   break;
		 //for deleting files and empty directories
           	 case 'd':
                	return_value = remove(filename);
                	if (return_value == -1) { goto error_handling; }
                 break;
		 //for writing first 50 bytes to standard output
           	 case 'w':
                	char buf[50];
			//opening file
                	return_value = open(filename, O_RDWR);
               	 	if (return_value == -1) { goto error_handling; }
			//reading file into buffer
               	 	return_value_2 = read(return_value, buf, 50);
	               	if (return_value_2 == -1) { goto error_handling; }
        		//writing to standard output
	        	return_value_3 = write(1, buf, 50);
	        	if (return_value_3 == -1) { goto error_handling; }
			//closing file
		        return_value_4 = close(return_value);
			if (return_value_4 == -1) { goto error_handling; }
                break;
		//for appending 50 bytes to file
	   	case 'a':
			if (i + 1 < argc) {
			int is_binary = 0;
                        char binary_buffer[1024];
                        //checking  if file is binary
                        //opening file
                        return_value = open(filename, O_CREAT | O_WRONLY | O_APPEND,  S_IRUSR | S_IWUSR | S_IRGRP |S_IROTH | S_IWOTH ); 
                        if (return_value == -1) { goto error_handling; }
                        ssize_t bytes_read = read(return_value, binary_buffer, 1024);
                        if (bytes_read == -1){ goto error_handling;}
                        for(ssize_t i = 0; i < bytes_read; i++){
                                //assigning 1 to is_binary if file is binary file(contains null)
                                if(binary_buffer[i] = '\0') {
                                        is_binary = 1;
                                        break;
                                }
                        }
			//for text file
			if (argv[i][2] == 't' && is_binary == 0) {
		    		char buf[50];
				//getting string to be appended from command line
		    		strcpy(buf, argv[i+1]);	
				//appending string to file
		    		return_value_2 = write(return_value, buf, 50);
		    		if (return_value == -1) { goto error_handling; }
	                }
			//for binary file
		 	else if (argv[i][2] == 'b' && is_binary == 1) {
				//converting command line argument to integer
		    		int start = atoi(argv[i+1]);
		    		if(start >50 && start <200){
					int values[12];
					int size=0, bytes=0;
					//calculating values
					for(int i =  0 ; i < 12; i++){
						if(start < 200){
							values[i] = start;
							size++;
							bytes+=4;
							start+=2; 
						}
			   		}
					//appending to file
					return_value_2 = write(return_value,values, size * sizeof(int));
					if(return_value_2 == -1){ goto error_handling;}
		 			return_value_2 = close(return_value);
                    			if (return_value_2 == -1) { goto error_handling; }
		   		}}
			i++;}
         	 break;


        	}}	//for returning errno codes
			error_handling:
				ec = errno;
				return ec;


		}
