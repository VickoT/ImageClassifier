import pandas 
import os, os.path
import cv2
import numpy as np
from PIL import Image

def image_separator(path_raw):

    raw_folder_path = path_raw

    try:
        os.chdir(raw_folder_path)
    except:
        print(f'{raw_folder_path} not found')
