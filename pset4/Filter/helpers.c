#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    //iterate over height
    for (int h = 0; h < height; h++)
    {
        //iterate over width
        for (int w = 0; w < width; w++)
        {
            float redvalue = image[h][w].rgbtRed;
            float greenvalue = image[h][w].rgbtGreen;
            float bluevalue = image[h][w].rgbtBlue;
            int averagevalue = round((redvalue + greenvalue + bluevalue) / 3);
            image[h][w].rgbtRed = averagevalue;
            image[h][w].rgbtGreen = averagevalue;
            image[h][w].rgbtBlue = averagevalue;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            int sepiaredvalue = round(.393 * image[h][w].rgbtRed + .769 * image[h][w].rgbtGreen + .189 * image[h][w].rgbtBlue);
            int sepiagreenvalue = round(.349 * image[h][w].rgbtRed + .686 * image[h][w].rgbtGreen + .168 * image[h][w].rgbtBlue);
            int sepiabluevalue = round(.272 * image[h][w].rgbtRed + .534 * image[h][w].rgbtGreen + .131 * image[h][w].rgbtBlue);

            if (sepiaredvalue > 255)
            {
                sepiaredvalue = 255;
            }
            if (sepiagreenvalue > 255)
            {
                sepiagreenvalue = 255;
            }
            if (sepiabluevalue > 255)
            {
                sepiabluevalue = 255;
            }
            image[h][w].rgbtRed = sepiaredvalue;
            image[h][w].rgbtGreen = sepiagreenvalue;
            image[h][w].rgbtBlue = sepiabluevalue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            temp[i][j] = image[i][j];
        }
    }
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            image[h][w] = temp[h][width-(w+1)];
            image[h][width-(w+1)] = temp[h][w];
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            temp[i][j] = image[i][j];
        }
    }
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            float redsum = 0;
            float greensum = 0;
            float bluesum = 0;
            int counter = 0;
            for (int x = -1; x < 2; x++)
            {
                for (int y = -1; y < 2; y++)
                {
                    if (h + x < 0 || h + x >= height)
                    {
                        continue;
                    }
                    if (w + y < 0 || w + y >= width)
                    {
                        continue;
                    }
                    redsum += temp[h+x][w+y].rgbtRed;
                    greensum += temp[h+x][w+y].rgbtGreen;
                    bluesum += temp[h+x][w+y].rgbtBlue;
                    counter++;
                }

            }
            image[h][w].rgbtRed = round(redsum / counter);
            image[h][w].rgbtGreen = round(greensum / counter);
            image[h][w].rgbtBlue = round(bluesum / counter);
        }
    }
    return;
}