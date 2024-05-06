import os
import pandas as pd
import joblib

import shutil



def run_svm(raw_dir):
    # Path to current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Path to model and scaler
    model_path = os.path.join(script_dir, 'svm_model.joblib')
    scaler_path = os.path.join(script_dir, 'scaler.joblib')

    try:
       os.chdir(raw_dir)
       raw_folder_path = os.getcwd()
    except:
        print(f'Error:  {raw_dir} not found')

    folder = raw_folder_path.split('/')[-1]
    csv_file = folder+'.csv'

    # Load dataset
    df = pd.read_csv(csv_file)
    # Load pre-trained model
    svm_model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)

    # Remove unwanted columns
    rm1 = ['Particle ID', 'Capture X', 'Capture Y', 'Date', 'Elapsed Time', 'Image File', 'Source Image', 'Time', 'Timestamp','Image X','Image Y']
    rm2 = ['Diameter (ABD)','Convex Perimeter', 'Diameter (ESD)', 'Compactness', 'Geodesic Length', 'Geodesic Aspect Ratio']
    df2 = df.drop(columns = rm1+rm2)
    df2 = df2.drop(columns=[col for col in df2.columns if df2[col].nunique() == 1])

    features = df2.select_dtypes(include=['number']).columns
    df2_scaled = scaler.transform(df2[features])

    # Use the loaded model to make predictions
    predictions = svm_model.predict(df2_scaled)

    # Attach predictions to df2 for visibility
    df2['Predictions'] = predictions

    # Define paths for predicted images
    parent_dir = os.path.dirname(raw_folder_path)
    output_dir = os.path.join(parent_dir,'Output_'+folder)
    prediction_dir = os.path.join(output_dir, )
    print(output_dir)
    os.makedirs

    #extracted_images = os.path.join('Output_'+folder,'Extracted_images')
    #path_imgs = os.path.join(parent_dir, extracted_images)

    path_junk = '/Users/vt2/Documents/Bioinf_LUND/Classifier/SVM_classifier/Predicted_images/Junk'
    path_protist = '/Users/vt2/Documents/Bioinf_LUND/Classifier/SVM_classifier/Predicted_images/Protist'