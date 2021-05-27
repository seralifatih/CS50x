#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    float amount_owed;
    do
    {
        amount_owed = get_float("Change owed: ");
    }
    while (amount_owed <= 0);

    int amount_cents = round(amount_owed * 100);
    int owed = amount_cents;
    int coins = 0;

    while (owed >= 25)
    {
        coins += 1;
        owed -= 25;
    }
    while (owed >= 10)
    {
        coins += 1;
        owed -= 10;
    }
    while (owed >= 5)
    {
        coins += 1;
        owed -= 5;
    }
    while (owed >= 1)
    {
        coins += 1;
        owed -= 1;
    }
    printf("%i\n", coins);
}