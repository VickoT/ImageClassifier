import pandas as pd
import argparse
from dir_setup import dir_setup
from image_separator import image_separator
from image_run_svm import run_svm



def main():
    parser = argparse.ArgumentParser(description="Separate images based on directory path.")
    parser.add_argument('-raw_dir', '--raw_directory', type=str, required=True,
                        help='The path to the directoyr containing the raw data diles (csv, tif)')
    args = parser.parse_args()
    raw_directory = args.raw_directory


    dir_setup(raw_directory)

    #image_separator(raw_directory)
    #run_svm(raw_directory)

if __name__ == "__main__":
    main()

