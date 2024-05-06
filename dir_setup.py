import os
import shutil

def dir_setup(raw_dir):
    path_current = os.getcwd()
    # sample name
    sample_name = raw_dir

    # Output dir
    output_dir = 'Output_' + sample_name
    path_output = os.path.join(path_current, output_dir)

    path_extracted_imgs = os.path.join(path_output, 'Extracted_images')

    path_predicted_imgs = os.path.join(path_output,'Predicted_images')
    path_predicted_junk = os.path.join(path_predicted_imgs, 'Junk')
    path_predicted_protist = os.path.join(path_predicted_imgs, 'Protist')

    if os.path.exists(path_output): shutil.rmtree(path_output)

    os.mkdir(path_output)
    os.mkdir(path_extracted_imgs)
    os.mkdir(path_predicted_imgs)
    os.mkdir(path_predicted_junk)
    os.mkdir(path_predicted_protist)

