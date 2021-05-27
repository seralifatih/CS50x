#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int size;
    do
    {
        size=get_int("Height: ");
    }
    while (size>8 || size<1);

    for (int counter_one=0; counter_one<size; counter_one++)
    {
        for (int counter_two=0; counter_two<size ;counter_two++)
        {
            if(counter_one+counter_two<size-1)
                printf(" ");
            else
                printf("#");
        }
        printf("\n");
    }
}