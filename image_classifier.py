#!/usr/bin/env python3

try:
    import pandas as pd
    import argparse
    from dir_setup import dir_setup
    from image_separator import image_separator
    from image_run_svm import run_svm
except ModuleNotFoundError as e:
    print(f"Error: {e}. \nPlease ensure the correct Python environment is activated. Run: 'conda activate image_classifier'")
    exit(1)

def main():
    parser = argparse.ArgumentParser(description="Separate images based on directory path.")
    parser.add_argument('-raw_dir', '--raw_directory', type=str, required=True,
                        help='The path to the directoyr containing the raw data diles (csv, tif)')
    args = parser.parse_args()
    raw_directory = args.raw_directory

    # Extract various path
    paths = dir_setup(raw_directory) 
    path_raw = paths[0]
    path_extracted_imgs = paths[1]
    path_pred_junk = paths[2]
    path_pred_protist = paths[3]
    path_scaler = paths[4]
    path_model = paths[5]

    # Separat individual images from FlowCam collage tif files
    image_separator(path_raw, path_extracted_imgs)
    # Prediction of images based on pretrained model
    run_svm(path_raw, path_scaler, path_model, path_extracted_imgs, path_pred_junk, path_pred_protist)

if __name__ == "__main__":
    main()

