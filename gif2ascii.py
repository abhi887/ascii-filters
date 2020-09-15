'''
This program cannot save the gif converted to ascii to an actual gif file
instead it'll print the output to the console. If you have an idea about 
exporting the converted art please open a issue or create a pull request.
'''
import cv2
import sys, random, argparse 
import numpy as np 
import math 
import os
from PIL import Image
import time
from imutils.video import FileVideoStream,FPS
 
gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
gscale2 = '@%#*+=-:. '

def getAverageL(image):
    """
    Given PIL Image, return average value of grayscale value 
    """
    im = np.array(image)
    w,h = im.shape
    return np.average(im.reshape(w*h)) 

def covertImageToAscii(fileName, cols, scale, moreLevels): 
    """ 
    Given Image and dims (rows, cols) returns an m*n list of Images 
    """
    global gscale1, gscale2
    image = cv2.cvtColor(fileName, cv2.COLOR_BGR2GRAY)
    image = Image.fromarray(image.astype('uint8'))
    W, H = image.size[0], image.size[1] 
    # print("input image dims: %d x %d" % (W, H)) 
    w = W/cols
    h = w/scale 
    rows = int(H/h) 
	
    # print("cols: %d, rows: %d" % (cols, rows)) 
    # print("tile dims: %d x %d" % (w, h))
    if cols > W or rows > H: 
        print("Image too small for specified cols!") 
        exit(0)
        
    aimg = [] 
	 
    for j in range(rows): 
        y1 = int(j*h) 
        y2 = int((j+1)*h) 
 
        if j == rows-1: 
            y2 = H 
        aimg.append("") 
        for i in range(cols): 
            x1 = int(i*w) 
            x2 = int((i+1)*w)
            if i == cols-1: 
                x2 = W 
            img = image.crop((x1, y1, x2, y2))
            avg = int(getAverageL(img))
            if moreLevels: 
                gsval = gscale1[int((avg*69)/255)] 
            else: 
                gsval = gscale2[int((avg*9)/255)] 
            aimg[j] += gsval
    return aimg


def main_SingleThreaded():
    try:
        clrscr()
        descStr = "This program converts an gif into ASCII art ~by Abhishek Vyas"
        parser = argparse.ArgumentParser(description=descStr)
        parser.add_argument('--file', dest='gifFile', required=True) 
        parser.add_argument('--scale', dest='scale', required=False)
        parser.add_argument('--cols', dest='cols', required=False) 
        parser.add_argument('--morelevels',dest='moreLevels',action='store_true') 
        args = parser.parse_args() 
        gifFile = args.gifFile
        scale = 0.45 if args.scale == None else float(args.scale) 
        cols = 80 if args.cols == None else int(args.cols) 
        moreLevels = False if args.moreLevels == None else args.moreLevels
        print('gif with ASCII filter ... press CTRL+C to stop') 

        vc = cv2.VideoCapture(gifFile)
        if vc.isOpened(): # try to get the first frame
            rval, frame = vc.read()
        else:
            rval = False
        fps = FPS().start()
        while rval:
            try:
                rval, frame = vc.read()
                aimg = covertImageToAscii(frame, cols, scale,moreLevels)
            except:
                pass
            clrscr()
            print("\n".join(aimg),end="")
            fps.update()
        fps.stop()
        print(f"\n[*] FPS ==> {fps.fps()}")
    except KeyboardInterrupt:
        exit(1)

# same as main_SingleThreaded but with imutil multi-threaded video stream wrapper applied (for a litle better FPS)
def main_MultiThreaded():
    try:
        clrscr()
        descStr = "This program converts an gif into ASCII art ~by Abhishek Vyas"
        parser = argparse.ArgumentParser(description=descStr)
        parser.add_argument('--file', dest='gifFile', required=True) 
        parser.add_argument('--scale', dest='scale', required=False)
        parser.add_argument('--cols', dest='cols', required=False) 
        parser.add_argument('--morelevels',dest='moreLevels',action='store_true') 
        args = parser.parse_args() 
        gifFile = args.gifFile
        scale = 0.45 if args.scale == None else float(args.scale) 
        cols = 80 if args.cols == None else int(args.cols) 
        moreLevels = False if args.moreLevels == None else args.moreLevels
        print('gif with ASCII filter ... press CTRL+C to stop') 

        file_path=gifFile
        fvs = FileVideoStream(file_path).start()
        time.sleep(1)
        fps = FPS().start()
        while fvs.more():
            frame=fvs.read()
            try:
                aimg = covertImageToAscii(frame, cols, scale, moreLevels)
            except:
                aimg="0"
            clrscr()
            print("\n".join(aimg),end="")
            fps.update()
        fps.stop()
        print(f"\n[*] FPS ==> {fps.fps()}")
    except KeyboardInterrupt:
        exit(1)

def clrscr():
    if os.name == "nt":
        error=os.system("cls")
    else:
        os.system("clear")

if __name__ == '__main__':
	main_MultiThreaded()
    # try this one too for FPS comparison
    # main_SingleThreaded()