import os
import numpy as np
import cv2
from numpy import save

#reads image directory from user and validates input
while True:
    print("Enter image directory with extension:")
    imagePath = str(input())
    if os.path.isfile(imagePath):
        break
    else:
        print("Invalid image path, Please make sure you're entering valid data")

#reads window size and validates it
while True:
    print("Enter sliding window size:")
    sliding_window = int(input())
    if sliding_window > 0:
        break
    else:
        print("Invalid sliding window size, Please make sure you're entering positive integer")

#reads look-ahead size and validates it
while True:
    print("Enter look-ahead buffer size: ")
    look_ahead = int(input())
    if 0 < look_ahead < sliding_window:
        break
    else:
        print("Invalid look-ahead buffer size, Please make sure you're entering"
              " positive integer less than sliding window size")

#main global variables to be reached by any function
search_buffer_length = sliding_window-look_ahead

Pixels = []

back_length = []
pattern_length = []
next_pixel = []

#checks directionaries of all patterns and return index of best pattern length
def checkDicrionary(dic_pattern_length):

    maxLength = max(dic_pattern_length)
    for index_of_max in range(len(dic_pattern_length)):
        if dic_pattern_length[index_of_max] == maxLength:
            return index_of_max

#holds encoding algorithm of LZ77
def Encode_LZ77():

    current_pointer = 0

    #checks if flatten image not finished
    while current_pointer < len(Pixels) :
        back_pointer = current_pointer-1

        #following arrays holds all posibile dictionaries could be generated for pattern
        arr_possible_back_length = []
        arr_possible_pattern_length = []
        arr_possible_next_pixel = []

        #checks that back pointer in it's specific limits(search buffer)
        while back_pointer>=0 and back_pointer >= current_pointer-search_buffer_length :

            #checks if pattern is found
            if Pixels[current_pointer] == Pixels[back_pointer] and back_pointer>=0 and back_pointer >= current_pointer-search_buffer_length:
                end_back_pointer = current_pointer-1
                end_current_pointer=current_pointer+look_ahead-1
                current_pattern_length = 1

                #checks for longer pattern length could be generated
                while back_pointer != end_back_pointer and current_pointer != end_current_pointer and current_pointer+1 < len(Pixels):
                    if Pixels[back_pointer+1] == Pixels[current_pointer+1] :
                        current_pattern_length += 1
                        back_pointer += 1
                        current_pointer += 1
                    else:
                        break

                #add possibility to arrays
                arr_possible_pattern_length.append(current_pattern_length)
                arr_possible_back_length.append(current_pointer-back_pointer)
                if current_pointer+1 >= len(Pixels):
                    arr_possible_next_pixel.append(0)
                else:
                    arr_possible_next_pixel.append(Pixels[current_pointer+1])
                current_pointer -= (current_pattern_length-1)
                back_pointer -= current_pattern_length
            else:
                back_pointer -= 1

        #checks if there's not any possibility is found for any pattern
        if len(arr_possible_next_pixel) == 0:
            back_length.append(0)
            pattern_length.append(0)
            next_pixel.append(Pixels[current_pointer])
            current_pointer += 1
        #checks if pattern is found, then add to dirctionary the best pattern found
        else:
            best_index = checkDicrionary(arr_possible_pattern_length)
            back_length.append(arr_possible_back_length[best_index])
            pattern_length.append(arr_possible_pattern_length[best_index])
            next_pixel.append(arr_possible_next_pixel[best_index])
            current_pointer += (pattern_length[-1] + 1)


def main():

    imageFile = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)
    print("Wait few moments")

    # read image resolution
    rows, cols = imageFile.shape

    #flattens image into list
    for i in range(rows):
        for j in range(cols):
            Pixels.append(imageFile[i, j])

    Encode_LZ77()

    #store image dimensions
    arrInfo = [cols, rows]

    #checks resolution to make suitable datetype
    if rows > 255 or cols>255:
        npyArr_info = np.array(arrInfo, dtype=np.uint16)
    else:
        npyArr_info = np.array(arrInfo, dtype=np.uint8)

    #store lists in numpy arrays
    npyArr_next_pixel = np.array(next_pixel, dtype= np.uint8)

    #checks serach & look-ahead buffers length to make suitable files
    if search_buffer_length>255:
        npyArr_back_length = np.array(back_length, dtype=np.uint16)
    else:
        npyArr_back_length = np.array(back_length, dtype=np.uint8)

    if look_ahead>255:
        npyArr_pattern_length = np.array(pattern_length, dtype= np.uint16)
    else:
        npyArr_pattern_length = np.array(pattern_length, dtype= np.uint8)

    #save all numpy arrays in its file
    save('npyArr_Width_Height.npy', npyArr_info)
    save('npyArr_back_length.npy',npyArr_back_length)
    save('npyArr_repeated_length.npy',npyArr_pattern_length)
    save('npyArr_next_pixel.npy',npyArr_next_pixel)

    print("Done")

if __name__ == "__main__":
    main()