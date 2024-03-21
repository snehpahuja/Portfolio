#include "helpers.h"
#include <math.h>
#include <stdio.h>


// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    double avg;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            avg = round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0);
            image[i][j].rgbtBlue = avg;
            image[i][j].rgbtGreen = avg;
            image[i][j].rgbtRed = avg;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    float originalBlue;
    float originalGreen;
    float originalRed;
    float temp;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //storing original values
            originalBlue = image[i][j].rgbtBlue;
            originalGreen = image[i][j].rgbtGreen;
            originalRed = image[i][j].rgbtRed;
            // converting blue
            temp = round((.272 * originalRed) + (.534 * originalGreen) + (.131 * originalBlue));
            if (temp <= 255 && temp >= 0)
            {
                image[i][j].rgbtBlue = round((.272 * originalRed) + (.534 * originalGreen) + (.131 * originalBlue));
            }
            else if (temp > 255)
            {
                image[i][j].rgbtBlue = 255;
            }
            else if (temp < 0)
            {
                image[i][j].rgbtBlue = 0;
            }

            // coverting green
            temp = round((.349 * originalRed) + (.686 * originalGreen) + (.168 * originalBlue));
            if (temp <= 255 &&  temp > 0)
            {
                image[i][j].rgbtGreen = round((.349 * originalRed) + (.686 * originalGreen) + (.168 * originalBlue));
            }
            else if (temp > 255)
            {
                image[i][j].rgbtGreen = 255;
            }
            else if (temp < 0)
            {
                image[i][j].rgbtGreen = 0;
            }

            // converting red
            temp = round((.393 * originalRed) + (.769 * originalGreen) + (.189 * originalBlue));
            if (temp <= 255 && temp > 0)
            {
                image[i][j].rgbtRed = round((.393 * originalRed) + (.769 * originalGreen) + (.189 * originalBlue));
            }
            else if (temp >= 255)
            {
                image[i][j].rgbtRed = 255;
            }
            else if (temp < 0)
            {
                image[i][j].rgbtRed = 0;
            }
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    int compare = width - 1;
    int half;
    if (width % 2 == 1)
    {
       half = (width + 1) / 2;
    }
    else
    {
       half = width / 2;
    }
    RGBTRIPLE temp[1][1];
    int j;
    for (int i = 0; i < height; i++)
    {
        j = 0;
        do
        {
            temp[0][0] = image[i][j];
            image[i][j] = image[i][compare - j];
            image[i][compare - j] = temp[0][0];
            j++;
        }
        while (j < half);
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{

    RGBTRIPLE copy[height][width];
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            copy[h][w].rgbtRed = image[h][w].rgbtRed;
            copy[h][w].rgbtBlue = image[h][w].rgbtBlue;
            copy[h][w].rgbtGreen = image[h][w].rgbtGreen;
        }
    }

    int totalred;
    int totalblue;
    int totalgreen;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
          // first pixel
            if (i == 0 && j == 0)
            {
                totalred = copy[0][0].rgbtRed + copy[1][0].rgbtRed + copy[0][1].rgbtRed + copy[1][1].rgbtRed;
                totalblue = copy[0][0].rgbtBlue + copy[1][0].rgbtBlue + copy[0][1].rgbtBlue+ copy[1][1].rgbtBlue;
                totalgreen = copy[0][0].rgbtGreen + copy[1][0].rgbtGreen + copy[0][1].rgbtGreen + copy[1][1].rgbtGreen;
                image[i][j].rgbtRed = round( totalred / 4.00);
                image[i][j].rgbtBlue = round(totalblue / 4.00);
                image[i][j].rgbtGreen = round(totalgreen / 4.00);
          }
          // last pixel
            else if (i == (height-1) && j == (width - 1))
            {
                totalred =  copy[height - 1][width - 1].rgbtRed + copy[height - 2][width - 1].rgbtRed + copy[height - 2][width - 2].rgbtRed +
                            copy[height - 1][width - 2].rgbtRed;
                totalblue = copy[height - 1][width - 1].rgbtBlue + copy[height - 2][width - 1].rgbtBlue + copy[height - 2][width - 2].rgbtBlue +
                            copy[height - 1][width - 2].rgbtBlue;
                totalgreen = copy[height - 1][width - 1].rgbtGreen + copy[height - 2][width - 1].rgbtGreen + copy[height - 2][width - 2].rgbtGreen +
                             copy[height - 1][width - 2].rgbtGreen;
                image[i][j].rgbtRed = round(totalred / 4.00);
                image[i][j].rgbtBlue = round(totalblue / 4.00);
                image[i][j].rgbtGreen = round(totalgreen / 4.00);
            }
          //first row excluding first cell and last cell
            else if (i == 0 && j > 0 && j < (width - 1) )
            {
                totalred = copy[i][j - 1].rgbtRed + copy[i][j].rgbtRed + copy[i][j + 1].rgbtRed + copy[i + 1][j - 1].rgbtRed + copy[i + 1][j].rgbtRed +
                           copy[i + 1][j + 1].rgbtRed;
                totalblue = copy[i][j - 1].rgbtBlue + copy[i][j].rgbtBlue + copy[i][j + 1].rgbtBlue + copy[i + 1][j - 1].rgbtBlue + copy[i + 1][j].rgbtBlue +
                            copy[i + 1][j + 1].rgbtBlue;
                totalgreen = copy[i][j - 1].rgbtGreen + copy[i][j].rgbtGreen + copy[i][j + 1].rgbtGreen + copy[i + 1][j - 1].rgbtGreen + copy[i + 1][j].rgbtGreen +
                             copy[i + 1][j + 1].rgbtGreen;
                image[i][j].rgbtRed = round(totalred / 6.00);
                image[i][j].rgbtBlue = round(totalblue / 6.00);
                image[i][j].rgbtGreen = round(totalgreen / 6.00);
            }

           // last row excluding first and last cell
            else if (i == (height -1) && j > 0 && j <(width - 1))
            {
               totalred = copy[i][j - 1].rgbtRed + copy[i][j].rgbtRed + copy[i][j + 1].rgbtRed + copy[i - 1][j - 1].rgbtRed + copy[i - 1][j].rgbtRed +
                          copy[i - 1][j + 1].rgbtRed;
               totalblue = copy[i][j - 1].rgbtBlue + copy[i][j].rgbtBlue + copy[i][j + 1].rgbtBlue + copy[i - 1][j - 1].rgbtBlue +copy[i - 1][j].rgbtBlue +
                           copy[i - 1][j + 1].rgbtBlue;
               totalgreen = copy[i][j - 1].rgbtGreen + copy[i][j].rgbtGreen + copy[i][j + 1].rgbtGreen + copy[i - 1][j - 1].rgbtGreen+copy[i - 1][j].rgbtGreen +
                            copy[i - 1][j + 1].rgbtGreen;
               image[i][j].rgbtRed = round(totalred / 6.00);
               image[i][j].rgbtBlue = round(totalblue / 6.00);
               image[i][j].rgbtGreen = round(totalgreen / 6.00);
            }
           // first column excluding first and last
            else if (i > 0 && i < (height - 1) && j == 0)
            {
                totalred = copy[i][j].rgbtRed + copy[i - 1][j].rgbtRed + copy[i + 1][j ].rgbtRed + copy[i + 1][j + 1].rgbtRed + copy[i - 1][j + 1].rgbtRed +
                           copy[i][j + 1].rgbtRed;
                totalblue = copy[i][j].rgbtBlue + copy[i - 1][j].rgbtBlue + copy[i + 1][j].rgbtBlue + copy[i + 1][j + 1].rgbtBlue + copy[i - 1][j + 1].rgbtBlue +
                            copy[i][j + 1].rgbtBlue;
                totalgreen = copy[i][j].rgbtGreen + copy[i - 1][j].rgbtGreen + copy[i + 1][j].rgbtGreen + copy[i + 1][j + 1].rgbtGreen + copy[i - 1][j + 1].rgbtGreen +
                             copy[i][j + 1].rgbtGreen;
                image[i][j].rgbtRed = round(totalred / 6.00);
                image[i][j].rgbtBlue = round(totalblue / 6.00);
                image[i][j].rgbtGreen = round(totalgreen / 6.00);
            }
             //last column ecluding first and last cell
             else if (i > 0 && i < (height - 1) && j == (width - 1))
             {
                 totalred = copy[i][j].rgbtRed + copy[i - 1][j].rgbtRed + copy[i + 1][j ].rgbtRed + copy[i + 1][j - 1].rgbtRed + copy[i - 1][j - 1].rgbtRed +
                            copy[i][j - 1].rgbtRed;
                 totalblue = copy[i][j].rgbtBlue + copy[i - 1][j].rgbtBlue + copy[i + 1][j].rgbtBlue + copy[i + 1][j - 1].rgbtBlue + copy[i - 1][j - 1].rgbtBlue +
                             copy[i][j - 1].rgbtBlue;
                 totalgreen = copy[i][j].rgbtGreen + copy[i - 1][j].rgbtGreen + copy[i + 1][j].rgbtGreen + copy[i + 1][j - 1].rgbtGreen + copy[i - 1][j - 1].rgbtGreen +
                              copy[i][j - 1].rgbtGreen;
                 image[i][j].rgbtRed = round(totalred / 6.000);
                 image[i][j].rgbtBlue = round(totalblue / 6.00);
                 image[i][j].rgbtGreen = round(totalgreen / 6.00);
             }
          // upper corner right cell
             else if ( i == 0 && j ==(width - 1))
             {
                 totalred = copy[i + 1][j].rgbtRed + copy[i][j].rgbtRed + copy[i][j - 1].rgbtRed + copy[i + 1][j - 1].rgbtRed;
                 totalblue = copy[i + 1][j].rgbtBlue + copy[i][j].rgbtBlue + copy[i][j - 1].rgbtBlue + copy[i + 1][j - 1].rgbtBlue;
                 totalgreen = copy[i + 1][j].rgbtGreen + copy[i][j].rgbtGreen + copy[i][j - 1].rgbtGreen + copy[i + 1][j - 1].rgbtGreen;
                 image[i][j].rgbtRed = round(totalred / 4.00);
                 image[i][j].rgbtBlue = round(totalblue / 4.00);
                 image[i][j].rgbtGreen = round(totalgreen / 4.00);
             }
           // lower corner left cell
             else if (i == (height - 1) && j == 0)
             {
                 totalred = copy[i - 1][j].rgbtRed + copy[i][j].rgbtRed + copy[i][j + 1].rgbtRed + copy[i - 1][j + 1].rgbtRed;
                 totalblue = copy[i - 1][j].rgbtBlue + copy[i][j].rgbtBlue + copy[i][j + 1].rgbtBlue + copy[i - 1][j + 1].rgbtBlue;
                 totalgreen = copy[i - 1][j].rgbtGreen + copy[i][j].rgbtGreen + copy[i][j + 1].rgbtGreen + copy[i - 1][j + 1].rgbtGreen;
                 image[i][j].rgbtRed = round(totalred / 4.00);
                 image[i][j].rgbtBlue = round(totalblue / 4.00);
                 image[i][j].rgbtGreen = round(totalgreen / 4.00);
             }
          // middle cells
          else
          {
              totalred = copy[i][j].rgbtRed + copy[i - 1][j].rgbtRed + copy[i + 1][j ].rgbtRed + copy[i + 1][j - 1].rgbtRed + copy[i - 1][j - 1].rgbtRed +
                         copy[i][j - 1].rgbtRed + copy[i + 1][j + 1].rgbtRed + copy[i - 1][j + 1].rgbtRed + copy[i][j + 1].rgbtRed;
              totalblue = copy[i][j].rgbtBlue + copy[i - 1][j].rgbtBlue + copy[i + 1][j].rgbtBlue + copy[i + 1][j - 1].rgbtBlue + copy[i - 1][j - 1].rgbtBlue +
                          copy[i][j - 1].rgbtBlue + copy[i + 1][j + 1].rgbtBlue + copy[i - 1][j + 1].rgbtBlue+ copy[i][j + 1].rgbtBlue;
              totalgreen = copy[i][j].rgbtGreen + copy[i - 1][j].rgbtGreen + copy[i + 1][j].rgbtGreen + copy[i + 1][j - 1].rgbtGreen + copy[i - 1][j - 1].rgbtGreen +
                           copy[i][j - 1].rgbtGreen + copy[i + 1][j + 1].rgbtGreen + copy[i - 1][j + 1].rgbtGreen + copy[i][j + 1].rgbtGreen;
              image[i][j].rgbtRed = round(totalred / 9.00);
              image[i][j].rgbtBlue = round(totalblue / 9.00);
              image[i][j].rgbtGreen = round(totalgreen / 9.00);
          }
        }
    }
}





