
'''
CHECK IF RAW_DIR EXISTS. IF NOT QUIT
'''
import pandas 
import os, os.path
import cv2

def image_separator(path_raw, path_extracted_imgs):

    # Set directory to the path of the raw data files
    try:
       os.chdir(path_raw)
    except:
        print(f'Error: {path_raw} not found')

    # Only inside one directory, unnecessary to walk through dirs
    for filename in [f for f in os.listdir(path_raw) if f.endswith(".lst")]:
        sample_name = os.path.splitext(filename)[0]
        sample_outpath = path_extracted_imgs
        fp = os.path.join(path_raw, filename)
        header = pandas.read_csv(fp, sep='|', skiprows=1, nrows=65)
        hd = list(header["num-fields"])
        meta = pandas.read_csv(fp, sep='|', skiprows=67, header=None)
        meta.columns = hd
        loaded_cp = "not_loaded"
        for id in meta["id"]:
            i = id - 1
            # Extracing the name of the collage file
            collage_filename = meta["collage_file"][i]
            cp = os.path.join(path_raw, collage_filename)
            
            if not cp == loaded_cp:
                collage = cv2.imread(cp)
                loaded_cp = cp
            img_sub = collage[meta["image_y"][i]:(meta["image_y"][i] + meta["image_h"][i]), meta["image_x"][i]:(meta["image_x"][i] + meta["image_w"][i])]

            vp = os.path.join(sample_outpath, sample_name + "_" + meta["image_id"][i] + ".png")
            cv2.imwrite(vp, img_sub)
    print("Images extracted from collage files")



