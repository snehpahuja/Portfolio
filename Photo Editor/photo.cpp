
#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <iostream>
#include <map>
#include <iomanip>

using namespace cv;
using namespace std;

const map<string, Scalar> colorMap = {
    {"blue", Scalar(255, 0, 0)},
    {"green", Scalar(0, 255, 0)},
    {"red", Scalar(0, 0, 255)},
    {"white", Scalar(255, 255, 255)},
    // Add more colors as needed
};

Mat src, temp, cropped, black_white, black_white_cropped, reflected_image;
Point start_point, end_point, text_position(50, 50);
Rect roi;
int crop_flag = 0;
int black_white_flag = 0;
double text_size = 1.0;
int font_type = FONT_HERSHEY_SIMPLEX;
Scalar text_color(255, 255, 255);
string user_text;

void mouse_start(int event, int x, int y, int flags, void* param);
void mouse_end(int event, int x, int y, int flags, void* param);
void keyboard_input(int key);
void applyClarity(Mat& inputImage, Mat& outputImage, double clarityStrength);
void applySaturation(Mat& inputImage, Mat& outputImage, double saturationFactor);
void modifyTemperature(Mat& image, float temperature);
void printColoredText(const std::string &text);
void printColoredBox(const std::string &text, int width, int height);

int main()
{
    namedWindow("Image Editor", WINDOW_NORMAL);

        printColoredBox("Welcome to Edoba: Your Pixel Playground by Code Busters!", 30, 1);

        cout << endl;
        printColoredBox("Our Story:Code Busters, a spirited team of student developers, embarked on a mission to redefine photo editing. Fueled by passion and driven by pixels, Edoba emerged. A photo editing app that transforms dreams into pixels. ", 30, 1);
        cout << endl;
        printColoredBox("Features: \n Crop & Rotate: Straighten up your shots and give them the perfect frame. \n Temperature & Saturation: Adjust the vibe with a swipe from icy cool to tropical warmth. \n Brightness & Highlights: Shine bright or embrace the moody ambiance. Your photos, your rules. \n Black & White Magic: Add nostalgia with classic black and white filters. \n Sepia Tones: Turn your photos into timeless classics with our sepia feature. \n Inserting Text: Let your photos speak! Add captions, quotes, or a simple 'Hello world!'", 30, 1);
        cout << endl;
        printColoredBox("Let the editing adventure begin!", 30, 1);
        cout << endl;
        printColoredBox(" The Team: \n Karmandeep Singh \n Laya Lakshminarayanan \n Sindhu Vandakaari \n Sneh Pahuja \n Varsha Gunturu \n Vineesha Vuppala", 30, 1);
        cout << endl;


    cout << "Welcome to the Image Editor!" << endl;
    cout << "1. Left-click and drag to select a region for cropping." << endl;
    cout << "2. Press 'C' key to initiate cropping." << endl;
    cout << "3. Press 'B' key to convert the image or cropped image to black and white." << endl;
    cout << "4. Press 'T' key to add text to the image." << endl;
    cout << "5. Press 'H' key for horizontal reflection." << endl;
    cout << "6. Press 'V' key for vertical reflection." << endl;
    cout << "7. Press 'E' key to apply Clarity." << endl;
    cout << "8. Press 'S' key to apply Saturation." << endl;
    cout << "9. Press 'P' key to apply Temperature." << endl;
    cout << "10. Press 'R' key to rotate the image in a certain angle." << endl;
    cout << "11. Press 'L' key to increase Brightness." << endl;
    cout << "12. Press 'Esc' key to exit." << endl;

    src = imread("/Users/gunturuvarsha/Desktop/Final_code/ProgramsDemo/aaaaaa.jpg");
    if (src.empty())
    {
        cout << "Could not open or find the image" << std::endl;
        return -1;
    }

    imshow("Image Editor", src);

    setMouseCallback("Image Editor", mouse_start, NULL);
    setMouseCallback("Image Editor", mouse_end, NULL);

    while (1)
    {
        int c = waitKey(50);
        if ((char)c == 27) // 'Esc' key to exit
        {
            break;
        }

        keyboard_input(c); // Call the keyboard_input function

        if (crop_flag == 1)
        {
            temp = src.clone();
            rectangle(temp, start_point, end_point, Scalar(0, 255, 0), 1, 8, 0);
            imshow("Image Editor", temp);

            roi = Rect(start_point.x, start_point.y, end_point.x - start_point.x, end_point.y - start_point.y);
            cropped = src(roi);
            imshow("Cropped Image", cropped);

            if (black_white_flag == 1)
            {
                cvtColor(cropped, black_white_cropped, COLOR_BGR2GRAY);
                imshow("Black and White Cropped", black_white_cropped);
                cout << "Cropped image converted to black and white!" << endl;
                black_white_flag = 0;
            }

            cout << "Region cropped successfully!" << endl;
            crop_flag = 0;
        }

        if (black_white_flag == 1)
        {
            cvtColor(src, black_white, COLOR_BGR2GRAY);
            imshow("Black and White", black_white);

            cout << "Image converted to black and white!" << endl;
            black_white_flag = 0;
        }

        // Temperature adjustment
        if (c == 'p' || c == 'P')
        {
            float temperature;
            cout << "Enter temperature adjustment value: ";
            cin >> temperature;

            // Modify the temperature of the image
            modifyTemperature(src, temperature);

            imshow("Image Editor", src);
        }
    }

    cout << "Thank you for using the Image Editor!" << endl;

    return 0;
}

void mouse_start(int event, int x, int y, int flags, void* param)
{
    if (event == EVENT_LBUTTONDOWN)
    {
        start_point = Point(x, y);
    }
}

void mouse_end(int event, int x, int y, int flags, void* param)
{
    if (event == EVENT_LBUTTONUP)
    {
        end_point = Point(x, y);
        crop_flag = 1;
    }
}

void keyboard_input(int key)
{
    if (key == 'c' || key == 'C')
    {
        crop_flag = 1;
        black_white_flag = 0;
    }
    else if (key == 'b' || key == 'B')
    {
        black_white_flag = 1;
        crop_flag = 0;
    }
    else if (key == 't' || key == 'T')
    {
        cout << "Enter text to add to the image: ";
        cin.ignore();  // Clear the buffer
        getline(cin, user_text);

        // Prompt user for text size
        cout << "Enter text size (default is 1.0): ";
        cin >> text_size;

        // Prompt user for font type
        cout << "Enter font type (0-7, default is FONT_HERSHEY_SIMPLEX): ";
        cin >> font_type;

        // Prompt user for text color
        string color_name;
        cout << "Enter text color (e.g., blue, green, red, white): ";
        cin >> color_name;

        auto color_it = colorMap.find(color_name);
        if (color_it != colorMap.end())
        {
            text_color = color_it->second;
        }
        else
        {
            cout << "Invalid color name. Using default color (white)." << endl;
        }

        // Add text to the image
        putText(src, user_text, text_position, font_type, text_size, text_color, 2);
        imshow("Image Editor", src);
    }
    else if (key == 'h' || key == 'H')
    {
        flip(src, reflected_image, 1);
        imshow("Image Editor", reflected_image);
    }
    else if (key == 'v' || key == 'V')
    {
        flip(src, reflected_image, 0);
        imshow("Image Editor", reflected_image);
    }
    else if (key == 'e' || key == 'E')
    {
        Mat outputImage;
        applyClarity(src, outputImage, 1.5);
        imshow("Image Editor", outputImage);
    }
    else if (key == 's' || key == 'S')
    {
        Mat outputImage;
        applySaturation(src, outputImage, 1.5);
        imshow("Image Editor", outputImage);
    }
    else if (key == 'r' || key == 'R'){
        Point2f src_center(src.cols/2.0F, src.rows/2.0F);
        double angle;

        cout << "Enter the angle of rotation: ";
        cin >> angle;

        double scale = 1.0;

        Mat rot_mat = getRotationMatrix2D(src_center, angle, scale);

        warpAffine(src, src, rot_mat, src.size(), INTER_LINEAR, BORDER_CONSTANT);

        imshow("Rotated Image", src);
    }
    else if (key == 'l' || key == 'L'){
        // Get brightness amount from the user
            double alpha;
            cout << "Enter the brightness factor (e.g., 1.5 for\n increasing brightness, 0.5 for decreasing): ";
            cin >> alpha;

            // Check if the entered value is valid
            if (alpha <= 0) {
                cout << "Invalid brightness factor. It should be greater than 0." << endl;
            }

            // Adjust brightness
            Mat adjustedImage = src * alpha;

            // Display the adjusted image
            imshow("Adjusted Image", adjustedImage);

    }
}

void applyClarity(Mat& inputImage, Mat& outputImage, double clarityStrength)
{
    Mat blurred;
    bilateralFilter(inputImage, blurred, 15, 150, 150);
    addWeighted(inputImage, 1.5, blurred, -0.5, 0, outputImage);
}

void applySaturation(Mat& inputImage, Mat& outputImage, double saturationFactor)
{
    cvtColor(inputImage, outputImage, COLOR_BGR2HSV);

    for (int i = 0; i < outputImage.rows; ++i)
    {
        for (int j = 0; j < outputImage.cols; ++j)
        {
            outputImage.at<Vec3b>(i, j)[1] = saturate_cast<uchar>(outputImage.at<Vec3b>(i, j)[1] * saturationFactor);
        }
    }

    cvtColor(outputImage, outputImage, COLOR_HSV2BGR);
}

void modifyTemperature(Mat& image, float temperature)
{
    // Iterate over each pixel in the image
    for (int i = 0; i < image.rows; ++i)
    {
        for (int j = 0; j < image.cols; ++j)
        {
            // Access the RGB values of the pixel at position (i, j)
            Vec3b& pixel = image.at<Vec3b>(i, j);

            // Modify the individual RGB values based on the temperature
            pixel[0] = saturate_cast<uchar>(pixel[0] - temperature); // Blue channel
            pixel[2] = saturate_cast<uchar>(pixel[2] + temperature); // Red channel
        }
    }
}

void printColoredText(const string &text)
{
   
    cout << text;
}

void printColoredBox(const string &text, int width, int height)
{
    // Print the lines with colored text and background
    for (int i = 0; i < height; ++i)
    {
        cout << setw(width) << left;
        printColoredText(text);
        cout << endl;
    }
}

