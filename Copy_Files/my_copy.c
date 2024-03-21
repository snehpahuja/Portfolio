#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/stat.h>
#include <string.h>

int main(int argc, char *argv[]){

	const char *input_file_path = NULL;
	const char *output_file_path = NULL;
	int input_file_descriptor;
     	int output_file_descriptor;
	
	//parsing command line arguments
	for(int i = 1; i <argc; i++){
		if(strcmp(argv[i], "-i") == 0 && i+1 < argc){
			input_file_path = argv[i+1];
			i++;
		}
		else if(strcmp(argv[i], "-o") == 0 && i+1 < argc){
			output_file_path = argv[i+1];
			i++;
		}
		else{
			return 1;
		}
	}

	//to check if the file paths are null
	if(input_file_path == NULL || output_file_path == NULL) {
		return 2;
	}

	//in case of standard input
	if(strcmp(input_file_path, "-") == 0){
		input_file_descriptor = 0;
	}
	
	//in case of path name
	else{
	    input_file_descriptor = open(input_file_path, O_RDONLY);	

	   //changing file permissions so that input file can be read 
      	    if(chmod(input_file_path, S_IRUSR | S_IRGRP | S_IROTH) == -1){
	       	return 3;}
	   	
      	}

	//if input_file cannot be opened
	if(input_file_descriptor == -1){
		return 4;
	}

	//get input file size 
	struct stat file_info;
	if(fstat(input_file_descriptor, &file_info) == -1){
		return 5;
		}

	off_t file_size = file_info.st_size;
	char *buf = (char*)malloc(file_size);
	
	//if memory cannot be allocated properly
	if(buf == NULL){
		close(input_file_descriptor);
		return 6;
	}

	ssize_t bytes_read = read(input_file_descriptor, buf, file_size);

	//if input file cannot be read
	if(bytes_read == -1){
		free(buf);
		close (input_file_descriptor);
		return 7;
		}
	
	// for standard output
	if(strcmp(output_file_path,"-") == 0){
        	output_file_descriptor = 1;
	}

	//for specified output file
	else{
	       output_file_descriptor = open(output_file_path, O_RDWR | O_CREAT | O_TRUNC, S_IRWXU | S_IRWXG | S_IRWXO);
	       if(chmod(output_file_path, S_IRWXU | S_IRWXG | S_IRWXO) == -1){
			free(buf);
			close(input_file_descriptor);
			return 8;
		}

	}

	//if ouput file cannot be opened
	if(output_file_descriptor == -1){
		free(buf);
		close(input_file_descriptor);
		return 9;
		}

	ssize_t bytes_written_output = write(output_file_descriptor, buf, bytes_read);
	
	// if ouput file cannot be written to
	if(bytes_written_output == -1) {
		free(buf);
		close(input_file_descriptor);
		close(output_file_descriptor);
		return 10;
		}	

	//closing files and freeing memory
	close(input_file_descriptor);
	close(output_file_descriptor);
	free(buf);
	return 0;
}
