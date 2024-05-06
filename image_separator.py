import pandas 
import os, os.path
import cv2
import numpy as np
import shutil
from PIL import Image

def image_separator(raw_dir):

    # Set directory to the path of the raw data files
    try:
       os.chdir(raw_dir)
       raw_folder_path = os.getcwd()
    except:
        print(f'Error:  {raw_dir} not found')

    # Extract the name of the directory
    folder = raw_folder_path.split('/')[-1]
    output_dir = f"Output_{folder}"
    # Extract the name of the parent directory
    parent_dir_path = os.path.dirname(raw_folder_path)

    output_folder_path = os.path.join(parent_dir_path,output_dir)
    extract_folder_path= os.path.join(output_folder_path, "Extracted_images")

    # If Outputfolder exists: remove and create a new one
    if os.path.exists(output_folder_path):
        shutil.rmtree(output_folder_path)
        
    os.mkdir(output_folder_path)

    if not os.path.exists(extract_folder_path):
        os.mkdir(extract_folder_path)
        print(f"Output directory created: {extract_folder_path}")

    for dirpath, dirnames, filenames in os.walk(raw_folder_path):
        for filename in [f for f in filenames if f.endswith(".lst")]:
            sample_name = os.path.splitext(filename)[0]
            sample_outpath = extract_folder_path
            fp = os.path.join(dirpath, filename)
            header = pandas.read_csv(fp, sep='|', skiprows=1, nrows=65)
            hd = list(header["num-fields"])
            meta = pandas.read_csv(fp, sep='|', skiprows=67, header=None)
            meta.columns = hd
            loaded_cp = "not_loaded"
            for id in meta["id"]:
                i = id - 1
                # Extracing the name of the collage file
                collage_filename = meta["collage_file"][i]
                cp = os.path.join(dirpath, collage_filename)
                
                if not cp == loaded_cp:
                    collage = cv2.imread(cp)
                    loaded_cp = cp
                img_sub = collage[meta["image_y"][i]:(meta["image_y"][i] + meta["image_h"][i]), meta["image_x"][i]:(meta["image_x"][i] + meta["image_w"][i])]

                vp = os.path.join(sample_outpath, sample_name + "_" + meta["image_id"][i] + ".png")
                cv2.imwrite(vp, img_sub)
        print("Images extracted from collage files")



