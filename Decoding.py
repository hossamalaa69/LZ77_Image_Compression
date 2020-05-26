import numpy as np
import cv2
from numpy import load

#reads all numpy arrays from files
infoArr = load("npyArr_Width_Height.npy")
arr_back_length = load("npyArr_back_length.npy")
arr_pattern_length = load("npyArr_repeated_length.npy")
arr_next_pixel = load("npyArr_next_pixel.npy")

#retrieve height and width from information array
Width = infoArr[0]
Height = infoArr[1]
Resolution = int(Width)*Height

#global array to store all decoded pixels
Pixels = []

#holds algorithm of LZ77 decoding
def Decode_LZ77(back_pointer, next_pixel_to_add, current_pattern_length):

    #loops for pattern length
    for i in range(current_pattern_length):
        #add each pixel from previous stored using back pointer
        Pixels.append(Pixels[-1 * back_pointer])

    #adds the next pixel stored in dictionary
    if len(Pixels) < Resolution:
        Pixels.append(next_pixel_to_add)

def main():

    print("Wait few moments")

    #apply LZ77 decoding for each dictionary
    for current_index in range(len(arr_pattern_length)):
        Decode_LZ77(arr_back_length[current_index], arr_next_pixel[current_index], arr_pattern_length[current_index])

    #reshape 2D array for generating decoded image
    pixels_npy = np.array(Pixels)
    matrix_pixels = pixels_npy.reshape(Height, Width)
    cv2.imwrite("file_out.png",matrix_pixels)

    print("Done")

if __name__ == "__main__":
        main()