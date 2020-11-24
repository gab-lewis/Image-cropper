import os

import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

def backgroundRemover(source_path):
    """
    This function takes an image with a white background and extracts the object within it, producing a transparent background png that is put into the objects folder

    Args:
    source_path : str = white background image path
    """
    #read image
    img = cv.imread(source_path)

    #detecting edges and smoothening 
    edges = cv.Canny(img, 80,150)
    kernel = np.ones((5,5), np.uint8)
    closing = cv.morphologyEx(edges, cv.MORPH_CLOSE, kernel, iterations=3)
    erosion = cv.morphologyEx(closing, cv.MORPH_ERODE, kernel, iterations=1)

    mask = np.zeros(img.shape[:2], np.uint8)
    mask[:] = 2
    mask[erosion == 255] = 1

    bgdmodel = np.zeros((1, 65), np.float64)
    fgdmodel = np.zeros((1, 65), np.float64)

    out_mask = mask.copy()
    out_mask, _, _ = cv.grabCut(img,out_mask,None,bgdmodel,fgdmodel,1,cv.GC_INIT_WITH_MASK)
    out_mask = np.where((out_mask==2)|(out_mask==0),0,1).astype('uint8')
    out_img = img*out_mask[:,:,np.newaxis]

    b,g,r = cv.split(out_img)
    ROI = cv.merge([b,g,r])

    tmp = cv.cvtColor(ROI, cv.COLOR_BGR2GRAY)
    _,alpha = cv.threshold(tmp,0,255,cv.THRESH_BINARY)
    b, g, r = cv.split(ROI)
    rgba = [b,g,r, alpha]
    dst = cv.merge(rgba)

    tmp = cv.cvtColor(dst, cv.COLOR_BGR2GRAY)
    _,alpha = cv.threshold(tmp,0,255,cv.THRESH_BINARY)
    b, g, r, _ = cv.split(dst)
    rgba = [b,g,r, alpha]
    dst = cv.merge(rgba,4)

    output_name = source_path.split("/")[3].split(".")[0]

    output_folder = './images/objects'

    cv.imwrite(f"{output_folder}/{output_name}_nobg.png", dst)

if __name__ == "__main__":
    SOURCE_PATH = "./images/white_images/"
    for image in os.listdir(SOURCE_PATH):
        backgroundRemover(f'{SOURCE_PATH}{image}')
