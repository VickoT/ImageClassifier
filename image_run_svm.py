import os
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler
import shutil

def run_svm(path_raw, path_scaler, path_model, path_extracted_imgs, path_pred_junk, path_pred_protist):

    # Remove trailing slash and get the last component in one line
    folder = os.path.basename(os.path.normpath(path_raw))
    csv_file = folder+'.csv'

    # Load dataset
    df = pd.read_csv(csv_file)
    # Load pre-trained model
    svm_model = joblib.load(path_model)
    scaler = joblib.load(path_scaler)

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

    # Loop through files in the source directory
    for file in os.listdir(path_extracted_imgs):
        path_file = os.path.join(path_extracted_imgs, file)

        # Assuming ID is correctly extracted from file name
        ID = file.split('_')[1].split('.')[0]
        # Extract prediction for the current ID
        prediction_series = df2.loc[df2['Original Reference ID'] == ID, "Predictions"]

        # Check if there is at least one prediction
        if not prediction_series.empty:
            prediction = prediction_series.iloc[0]  # Take the first prediction if there are multiple

            # Decide the destination path based on the prediction
            if prediction == 'Protist':
                dest_path = os.path.join(path_pred_protist, file)
            elif prediction == 'Junk':
                dest_path = os.path.join(path_pred_junk, file)
            else:
                continue  # Skip if the prediction is not recognized

            # Copy the file to the destination
            shutil.move(path_file, dest_path)


    # Remove the directory from where the images were moved
    os.rmdir(path_extracted_imgs)
    print("Images predicted and sorted in 'Prediction' directory.")

    print(df2['Predictions'].value_counts())
