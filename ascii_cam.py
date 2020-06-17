import cv2
import sys, random, argparse 
import numpy as np 
import math 
import os

from PIL import Image 

# gray scale level values from: 
# http://paulbourke.net/dataformats/asciiart/ 

# 70 levels of gray 
gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

# 10 levels of gray 
gscale2 = '@%#*+=-:. '
#gscale2='@#=-. '

def getAverageL(image): 

    """ 
    Given PIL Image, return average value of grayscale value 
    """
    # get image as numpy array 
    im = np.array(image)
    # im=image
    # get shape 
    w,h = im.shape 
    # get average 
    return np.average(im.reshape(w*h)) 

def covertImageToAscii(fileName, cols, scale, moreLevels): 
    """ 
    Given Image and dims (rows, cols) returns an m*n list of Images 
    """
    # declare globals 
    global gscale1, gscale2 
    
    # open image and convert to grayscale 
    # image = Image.open(fileName).convert('L')
    image = cv2.cvtColor(fileName, cv2.COLOR_BGR2GRAY)
    image = Image.fromarray(image.astype('uint8'))
    # print(image.size)
    
    # store dimensions 
    W, H = image.size[0], image.size[1] 
    # print("input image dims: %d x %d" % (W, H)) 
    # compute width of tile 
    w = W/cols 
    # compute tile height based on aspect ratio and scale 
    h = w/scale 
    # compute number of rows 
    rows = int(H/h) 

    # print("cols: %d, rows: %d" % (cols, rows)) 
    # print("tile dims: %d x %d" % (w, h)) 
    # check if image size is too small 
    if cols > W or rows > H: 
        print("Image too small for specified cols!") 
        exit(0) 
    # ascii image is a list of character strings 
    aimg = [] 
    # generate list of dimensions 
    for j in range(rows): 
        y1 = int(j*h) 
        y2 = int((j+1)*h) 
        # correct last tile 
        if j == rows-1: 
            y2 = H 
        # append an empty string 
        aimg.append("") 
        for i in range(cols): 
            # crop image to tile 
            x1 = int(i*w) 
            x2 = int((i+1)*w) 
            # correct last tile 
            if i == cols-1: 
                x2 = W 
            # crop image to extract tile 
            img = image.crop((x1, y1, x2, y2)) 
            # get average luminance 
            avg = int(getAverageL(img)) 
            # look up ascii char 
            if moreLevels: 
                gsval = gscale1[int((avg*69)/255)] 
            else: 
                gsval = gscale2[int((avg*9)/255)] 
            # append ascii char to string 
            aimg[j] += gsval 

    # return txt image 
    return aimg 

# main() function 
def main(): 
    cv2.namedWindow("preview")
    vc = cv2.VideoCapture(0)

    if vc.isOpened(): # try to get the first frame
        rval, frame = vc.read()
    else:
        rval = False
    
    #counter=0
    while rval:
        cv2.imshow("preview", frame)
        rval, frame = vc.read()
        #if(counter%2==0):
        aimg = covertImageToAscii(frame, 100, 0.45, False)
        os.system('cls')
        #if(counter>100):
             #   counter=0
        for row in aimg:
            print(row)
        key = cv2.waitKey(20)
        if key == 27: # exit on ESC
            break
        #counter+=1
    cv2.destroyWindow("preview")

# call main 
if __name__ == '__main__': 
	main()
