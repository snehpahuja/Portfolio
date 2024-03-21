#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <string.h>
#include <errno.h>

#define MAX_OPTIONS_LENGTH 100 // Maximum length of options string

int main(int argc, char *argv[])
{
    if (argc < 4)
    {
        // Check if minimum the minimum arguments passed are 4
        return 1;
    }

    // Variables for pathname, options string and mode (background/foreground)
    char *executable_path = NULL;
    char *option_string = NULL;
    char *mode = NULL;

    // Parse command line arguments
    for (int i = 1; i < argc; i++)
    {
        // Check for the -e option
        if (strcmp(argv[i], "-e") == 0)
        {
            if (i + 1 < argc)
            {
                // Set executable_path
                executable_path = argv[i + 1];
                i++; // Skip next argument since it is the path
            }
            else
            {
                return 1; // Program ends if there is no executable_path file found
            }
        }
        // Check for the -o options
        else if (strcmp(argv[i], "-o") == 0)
        {
            // Set string of options
            if (i + 1 < argc)
            {
                option_string = argv[i + 1];
                i++; // Skip next argument since it is the options
            }
            else
            {
                return 1; // Program ends if there is no string of options found
            }
        }
        // Check for the -f or -b options
        else if (strcmp(argv[i], "-b") == 0 || strcmp(argv[i], "-f") == 0)
        {
            mode = argv[i];
        }
        else
        {
            return 1; // Program ends if there unknown options
        }
    }

    // Check if executable path is provided
    if (executable_path == NULL)
    {
        return 1;
    }

     // If options string is not provided, set it to an empty string
    if (option_string == NULL)
    {
        option_string = "";
    }

    // Fork a child process
    pid_t pid = fork();
    if (pid < 0)
    {
        return 1;
    }
    else if (pid == 0)
    {
        // Child process
        // Split the options string into separate arguments
        char *options[MAX_OPTIONS_LENGTH];
        char *token = strtok(option_string, " ");
        int count = 0;
        while (token != NULL && count < MAX_OPTIONS_LENGTH - 1)
        {
            // Handle nested quotes
            if (token[0] == '\'' || token[0] == '"')
            {
                options[count++] = token + 1; // Skip the opening quote
                token = strtok(NULL, " ");
                while (token != NULL && token[strlen(token) - 1] != token[0])
                {
                    options[count - 1] = strcat(options[count - 1], " ");
                    options[count - 1] = strcat(options[count - 1], token);
                    token = strtok(NULL, " ");
                }
                if (token != NULL)
                {
                    options[count - 1] = strcat(options[count - 1], " ");
                    options[count - 1] = strcat(options[count - 1], token);
                    options[count - 1][strlen(options[count - 1]) - 1] = '\0'; // Remove the closing quote
                }
            }
            else
            {
                options[count++] = token;
            }
            token = strtok(NULL, " ");
        }
        options[count] = NULL; // Terminate the arguments with NULL

        // Set arguments for execve, including executable path and options
        char *args[count + 2];
        args[0] = executable_path;
        for (int i = 0; i < count; i++)
        {
            args[i + 1] = options[i];
        }
        args[count + 1] = NULL; // Terminate the arguments with NULL

        execve(executable_path, args, NULL);
        return errno; // execve only returns if there's an error
    }
    else
    { // Parent process
        int status;
        if (strcmp(mode, "-b") == 0)
        {
            write(STDOUT_FILENO, "Running in background mode\n", 28);
            waitpid(pid, &status, WNOHANG); // Don't wait for child to finish (Return immediately if no child has exited)
        }
        else
        { // Foreground mode
            write(STDOUT_FILENO, "Running in foreground mode\n", 28);
            waitpid(pid, &status, 0); // Wait for child to finish (meaning wait for any child process whose process group ID is equal to that of the calling process at the time of the call)
        }
        // Write the full command line of C program received for execution to the Standard Output.
        write(STDOUT_FILENO, "Command line: ", 14);
        for (int i = 0; i < argc; i++)
        {
            write(STDOUT_FILENO, argv[i], strlen(argv[i]));
            write(STDOUT_FILENO, " ", 1);
        }

        write(STDOUT_FILENO, "\n", 1); // Move to new line for better readability

        char pid_msg[50];
        snprintf(pid_msg, 50, "Process ID of the child: %d\n", pid);
        write(STDOUT_FILENO, pid_msg, strlen(pid_msg)); // Write Process ID of the child to the Standard Output

        // Write Exit code of the child to the Standard Output, if any
        if (WIFEXITED(status))
        {
            char exit_msg[50];
            snprintf(exit_msg, 50, "Exit code of the child: %d\n", WEXITSTATUS(status));
            write(STDOUT_FILENO, exit_msg, strlen(exit_msg));
        }
        // Write error codes, if any
        if (WIFSIGNALED(status))
        {
            char signal_msg[50];
            snprintf(signal_msg, 50, "Child process terminated by signal: %d\n", WTERMSIG(status));
            write(STDOUT_FILENO, signal_msg, strlen(signal_msg));
        }
    }
    return 0;
}
