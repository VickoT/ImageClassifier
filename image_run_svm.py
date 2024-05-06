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
    path_imgs = os.path.join(output_dir,'Extracted_images')
    prediction_dir = os.path.join(output_dir,'Predicted_images')
    path_junk = os.path.join(prediction_dir,'Junk')
    path_protist = os.path.join(prediction_dir,'Protist')
    #os.makedirs(path_junk)
    #os.makedirs(path_protist)

    # Loop through files in the source directory
    for file in os.listdir(path_imgs):
        path_file = os.path.join(path_imgs, file)

        # Assuming ID is correctly extracted from file name
        ID = file.split('_')[1].split('.')[0]
        # Extract prediction for the current ID
        prediction_series = df2.loc[df2['Original Reference ID'] == ID, "Predictions"]

        # Check if there is at least one prediction
        if not prediction_series.empty:
            prediction = prediction_series.iloc[0]  # Take the first prediction if there are multiple

            # Decide the destination path based on the prediction
            if prediction == 'Protist':
                dest_path = os.path.join(path_protist, file)
            elif prediction == 'Junk':
                dest_path = os.path.join(path_junk, file)
            else:
                continue  # Skip if the prediction is not recognized

            # Copy the file to the destination
            shutil.copy(path_file, dest_path)



