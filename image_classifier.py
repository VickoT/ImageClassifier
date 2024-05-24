#!/usr/bin/env python3


def report_file(path_raw, path_output, path_pred_junk, path_pred_protist):
    import os
    from datetime import datetime
    # List comprehension to get the file ending with "_summary.csv"
    summary_files = [file for file in os.listdir(path_raw) if file.endswith("_summary.csv")]

    for summary_file in summary_files:
        with open(os.path.join(path_raw, summary_file), 'r') as file:
            for line in file:
                if 'Sample Volume Imaged ml' in line:
                    # Extract the numeric value from the line
                    volume_imaged = float(line.split(',')[1].strip())

    sample = os.path.basename(os.path.normpath(path_raw))
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    count_junk = len(os.listdir(path_pred_junk))
    count_protist = len(os.listdir(path_pred_protist))

    report_content = [
        f" Report - {sample} \t ({current_time})",
        "=========================",
        f"Sample Volume Imaged (ml): {volume_imaged}",
        "\nCategories",
        f"Junk: {count_junk}",
        f"Protist: {count_protist}",
        f"\nEstimated conc. (protists/ml): {count_protist/volume_imaged:.2f}"
    ]

    with open (os.path.join(path_output, 'report.txt'), 'w') as report_file:
        for line in report_content:
            report_file.write(line + '\n')
    print(f'Estimated conc. (protists/ml): {count_protist/volume_imaged:.2f}')
    print("Report created in 'Output' directory")

try:
    import pandas as pd
    import argparse
    from dir_setup import dir_setup
    from image_separator import image_separator
    from image_run_svm import run_svm

except ModuleNotFoundError as e:
    print(f"Error: {e}. \nPlease ensure the correct Python environment is activated. Ex run: 'conda activate image_classifier'")
    exit(1)

def main():
    parser = argparse.ArgumentParser(description="Separate images based on directory path.")
    parser.add_argument('-raw_dir', '--raw_directory', type=str, required=True,
                        help='The path to the directoyr containing the raw data diles (csv, tif)')
    args = parser.parse_args()
    raw_directory = args.raw_directory

    # Extract various path (use dict instead)
    paths = dir_setup(raw_directory) 

    path_raw = paths['path_raw']
    path_output = paths['path_output']
    path_extracted_imgs = paths['path_extracted_imgs']
    path_pred_junk = paths['path_predicted_junk']
    path_pred_protist = paths['path_predicted_protist']
    path_scaler = paths['path_scaler']
    path_model = paths['path_model']


    # Separat individual images from FlowCam collage tif files
    image_separator(path_raw, path_extracted_imgs)
    # Prediction of images based on pretrained model
    run_svm(path_raw, path_scaler, path_model, path_extracted_imgs, path_pred_junk, path_pred_protist)

    report_file(path_raw, path_output, path_pred_junk, path_pred_protist)


if __name__ == "__main__":
    main()

