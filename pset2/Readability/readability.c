#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <math.h>


int count_letters(string text);
int count_words(string text);
int count_sentences(string text);
int main(void)
{
    //get text from the user
    string text = get_string("Text: ");
    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentences(text);
    float preindex = 0.0588 * (letters * 100.0) / words - 0.296 * (sentences * 100.0) / words - 15.8;
    int index = round(preindex);
    printf("%i\n", letters);
    printf("%i\n", words);
    printf("%i\n", sentences);
    printf("%i\n", index);
    if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}

int count_letters(string text)
{
    int counter = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (isupper(text[i]))
        {
            counter += 1;
        }
        else if (islower(text[i]))
        {
            counter += 1;
        }
    }
    return counter;
}

int count_words(string text)
{
    int word_counter = 1;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (isspace(text[i]))
        {
            word_counter += 1;
        }
    }
    return word_counter;
}

int count_sentences(string text)
{
    int sentence_counter = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == '.' || text[i] == '?' || text[i] == '!')
        {
            sentence_counter += 1;
        }
    }
    return sentence_counter;
}
