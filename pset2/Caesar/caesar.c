#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>


int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    else
    {
        int number = strlen(argv[1]);
        int counter = 0;
        for (int i = 0; i < number; i++)
        {
            if (isdigit(argv[1][i]))
            {
                counter += 1;
            }
        }
        if (number == counter)
        {
            int key = atoi(argv[1]);
            string text = get_string("plaintext: ");
            printf("ciphertext: ");
            for (int i = 0, n = strlen(text); i < n; i++)
            {
                if isalpha(text[i])
                {
                    if isupper(text[i])
                    {
                        int charindexupper = text[i] - 65;
                        int charupperencr = ((charindexupper + key) % 26) + 65;
                        printf("%c", charupperencr);
                    }
                    else if islower(text[i])
                    {
                        int charindexlower = text[i] - 97;
                        int charlowerencr = ((charindexlower + key) % 26) + 97;
                        printf("%c", charlowerencr);
                    }
                }
                else
                {
                    printf("%c", text[i]);
                }
            }
            printf("\n");
        }
        else
        {
            printf("Usage: ./caesar key\n");
        }
    }
}