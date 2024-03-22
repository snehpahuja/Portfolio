// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <strings.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdint.h>

#include "dictionary.h"

int dsize = 0;

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 676;

// Hash table
node *table[N];

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    for (int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }

    FILE *input = fopen(dictionary, "r");

    if (dictionary == NULL)
    {
        return false;
    }

    char word[LENGTH + 1];
    while ((fscanf(input, "%s", word)) != EOF)
    {
        node *temp = malloc(sizeof(node));
        if (temp == NULL)
        {
            return false;
        }

        strcpy(temp->word, word);
        unsigned int hashnumber = hash(word);
        if (table[hashnumber] == NULL)
        {
            table[hashnumber] = temp;
            dsize++;
        }
        else
        {
            temp->next = table[hashnumber];
            table[hashnumber] = temp;
            dsize++;
        }
    }
    fclose(input);
    return true;
}

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    // hash word
    unsigned int hashnumber = hash(word);
    node *cursor = table[hashnumber];
    // traversing linked list at that hash number
    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    int first = 0;
    int second = 1;
    unsigned int hashvalue;
    if (strlen(word) < 2)
    {
        for (int i = 97; i < 123; i ++)
        {
            // check asciivalue both uppercase and lowercase for first letter
            if (word[first] == (char)i || word[first] == (char)(i - 32))
            {
                hashvalue = (i - 97) * 26;
            }
        }
    }
    else
    {
        for (int i = 97; i < 123; i ++)
        {
            // check asciivalue both uppercase and lowercase for first letter
            if (word[first] == (char)i || word[first] == (char)(i - 32))
            {
                hashvalue = (i - 97) * 26;
                for (int j = 97; j < 122; j++)
                {
                    if (word[second] == (char)39)
                    {
                        second++;
                    }
                    // check asciivalue both uppercase and lowercase for second alphabet
                    if (word[second] == (char)j || word[second] == (char)(j - 32))
                    {
                        hashvalue = hashvalue + (j - 97);
                    }
                }
            }
        }
    }
    return hashvalue;

}



// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return dsize;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
        if (cursor == NULL && i == (N - 1))
        {
            return true;
        }
    }

    return false;

}
