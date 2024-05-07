# Right now the script have to be run at the same level as the raw dir.
# Otherwise the sample name will be weird 

import os
import shutil

def dir_setup(raw_dir):
    # Setting up names for directories to be created
    sample_name = raw_dir # sample name
    output_dir = 'Output_' + sample_name # output dir name
    # Creating paths
    path_current = os.getcwd() # get current path
    path_raw = os.path.join(path_current, raw_dir)
    path_output = os.path.join(path_current, output_dir) # output dir path
    path_extracted_imgs = os.path.join(path_output, 'Extracted_images') # path separated images
    path_predicted_imgs = os.path.join(path_output,'Predicted_images') # path predicted images 
    path_predicted_junk = os.path.join(path_predicted_imgs, 'Junk') # path predicted junk
    path_predicted_protist = os.path.join(path_predicted_imgs, 'Protist') # path predicted protists
    path_script = os.path.dirname(os.path.abspath(__file__))
    path_scaler = os.path.join(path_script, 'scaler.joblib')
    path_model = os.path.join(path_script, 'svm_model.joblib')

    # Remove previous output directory if it exists 
    if os.path.exists(path_output): 
        shutil.rmtree(path_output)
        print("Previous output directory is replaced.")

    # Create output directories
    os.mkdir(path_output)
    os.mkdir(path_extracted_imgs)
    os.mkdir(path_predicted_imgs)
    os.mkdir(path_predicted_junk)
    os.mkdir(path_predicted_protist)

    return path_raw, path_extracted_imgs, path_predicted_junk, path_predicted_protist, path_scaler, path_model

