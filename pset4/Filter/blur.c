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
    for (int w = 0; w < width; w++)
    {
        for (int h = 0; h < height; h++)
        {
            if (w == 0 && h == 0) //upper left corner
            {
                int averagered = round((temp[w][h].rgbtRed + temp[w][h+1].rgbtRed + temp[w+1][h].rgbtRed + temp[w+1][h+1].rgbtRed) / 4);
                int averagegreen = round((temp[w][h].rgbtGreen + temp[w][h+1].rgbtGreen + temp[w+1][h].rgbtGreen + temp[w+1][h+1].rgbtGreen) / 4);
                int averageblue = round((temp[w][h].rgbtBlue + temp[w][h+1].rgbtBlue + temp[w+1][h].rgbtBlue + temp[w+1][h+1].rgbtBlue) / 4);
                image[w][h].rgbtRed = averagered;
                image[w][h].rgbtGreen = averagegreen;
                image[w][h].rgbtBlue = averageblue;
            }
            else if (w == width && h == height) //lower right corner
            {
                int averagered = round((temp[w][h].rgbtRed + temp[w-1][h-1].rgbtRed + temp[w][h-1].rgbtRed + temp[w-1][h].rgbtRed) / 4);
                int averagegreen = round((temp[w][h].rgbtGreen + temp[w-1][h-1].rgbtGreen + temp[w][h-1].rgbtGreen + temp[w-1][h].rgbtGreen) / 4);
                int averageblue = round((temp[w][h].rgbtBlue + temp[w-1][h-1].rgbtBlue + temp[w][h-1].rgbtBlue + temp[w-1][h].rgbtBlue) / 4);
                image[w][h].rgbtRed = averagered;
                image[w][h].rgbtGreen = averagegreen;
                image[w][h].rgbtBlue = averageblue;
            }
            else if (w == 0 && h == height) //upper right corner
            {
                int averagered = round((temp[w][h].rgbtRed + temp[w+1][h-1].rgbtRed + temp[w][h-1].rgbtRed + temp[w+1][h].rgbtRed) / 4);
                int averagegreen = round((temp[w][h].rgbtGreen + temp[w+1][h-1].rgbtGreen + temp[w][h-1].rgbtGreen + temp[w+1][h].rgbtGreen) / 4);
                int averageblue = round((temp[w][h].rgbtBlue + temp[w+1][h-1].rgbtBlue + temp[w][h-1].rgbtBlue + temp[w+1][h].rgbtBlue) / 4);
                image[w][h].rgbtRed = averagered;
                image[w][h].rgbtGreen = averagegreen;
                image[w][h].rgbtBlue = averageblue;
            }
            else if (w == width && h == 0) //lower left corner
            {
                int averagered = round((temp[w][h].rgbtRed + temp[w-1][h+1].rgbtRed + temp[w-1][h].rgbtRed + temp[w][h+1].rgbtRed) / 4);
                int averagegreen = round((temp[w][h].rgbtGreen + temp[w-1][h+1].rgbtGreen + temp[w-1][h].rgbtGreen + temp[w][h+1].rgbtGreen) / 4);
                int averageblue = round((temp[w][h].rgbtBlue + temp[w-1][h+1].rgbtBlue + temp[w-1][h].rgbtBlue + temp[w][h+1].rgbtBlue) / 4);
                image[w][h].rgbtRed = averagered;
                image[w][h].rgbtGreen = averagegreen;
                image[w][h].rgbtBlue = averageblue;
            }
            else if ((w == 0) && (h > 0 && h < height)) //upper edge
            {
                int averagered = round((temp[w][h].rgbtRed + temp[w][h-1].rgbtRed + temp[w+1][h].rgbtRed + temp[w+1][h-1].rgbtRed + temp[w+1][h+1].rgbtRed + temp[w][h+1].rgbtRed) / 6);
                int averagegreen = round((temp[w][h].rgbtGreen + temp[w][h-1].rgbtGreen + temp[w+1][h].rgbtGreen + temp[w+1][h-1].rgbtGreen + temp[w+1][h+1].rgbtGreen + temp[w][h+1].rgbtGreen) / 6);
                int averageblue = round((temp[w][h].rgbtBlue + temp[w][h-1].rgbtBlue + temp[w+1][h].rgbtBlue + temp[w+1][h-1].rgbtBlue + temp[w+1][h+1].rgbtBlue + temp[w][h+1].rgbtBlue) / 6);
                image[w][h].rgbtRed = averagered;
                image[w][h].rgbtGreen = averagegreen;
                image[w][h].rgbtBlue = averageblue;
            }
            else if ((w == width) && (h > 0 && h < height)) //lower edge
            {
                int averagered = round((temp[w][h].rgbtRed + temp[w][h-1].rgbtRed + temp[w][h+1].rgbtRed + temp[w-1][h].rgbtRed + temp[w-1][h-1].rgbtRed + temp[w-1][h+1].rgbtRed) / 6);
                int averagegreen = round((temp[w][h].rgbtGreen + temp[w][h-1].rgbtGreen + temp[w][h+1].rgbtGreen + temp[w-1][h].rgbtGreen + temp[w-1][h-1].rgbtGreen + temp[w-1][h+1].rgbtGreen) / 6);
                int averageblue = round((temp[w][h].rgbtBlue + temp[w][h-1].rgbtBlue + temp[w][h+1].rgbtBlue + temp[w-1][h].rgbtBlue + temp[w-1][h-1].rgbtBlue + temp[w-1][h+1].rgbtBlue) / 6);
                image[w][h].rgbtRed = averagered;
                image[w][h].rgbtGreen = averagegreen;
                image[w][h].rgbtBlue = averageblue;
            }
        }
    }
    return;
}