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
    df2 = pd.read_csv(csv_file)
    # Load pre-trained model
    model = joblib.load(path_model)

    # Feaures to select according to ANOVA features selection
   # features = ['Aspect Ratio', 'Average Red', 'Circle Fit', 'Circularity (Hu)',
   #             'Edge Gradient', 'Fiber Curl', 'Geodesic Thickness',
   #             'Particles Per Chain', 'Perimeter', 'Ratio Blue/Green',
   #             'Ratio Red/Green', 'Roughness', 'Sigma Intensity', 'Sum Intensity',
   #             'Transparency', 'Width']

    # All features, for GBC with intrinsic feature selection
    features = ['Area (ABD)', 'Area (Filled)', 'Aspect Ratio', 'Average Blue',
                'Average Green', 'Average Red', 'Circle Fit', 'Circularity',
                'Circularity (Hu)', 'Compactness', 'Convex Perimeter', 'Convexity',
                'Diameter (ABD)', 'Diameter (ESD)', 'Diameter (FD)', 'Edge Gradient',
                'Elongation', 'Feret Angle Max', 'Feret Angle Min', 'Fiber Curl',
                'Fiber Straightness', 'Geodesic Aspect Ratio', 'Geodesic Length',
                'Geodesic Thickness', 'Image Height', 'Image Width', 'Intensity',
                'Length', 'Particles Per Chain', 'Perimeter', 'Ratio Blue/Green',
                'Ratio Red/Blue', 'Ratio Red/Green', 'Roughness', 'Sigma Intensity',
                'Sum Intensity', 'Symmetry', 'Transparency', 'Volume (ABD)',
                'Volume (ESD)', 'Width']
    # Use the loaded model to make predictions
    predictions = model.predict(df2[features])

    # Attach predictions to df2 for visibility
    df2['Predictions'] = predictions
    # Create the mapping dictionary
    mapping = {1: 'Protist', 0: 'Junk'}
    df2['Predictions'] = df2['Predictions'].map(mapping) 

    # Loop through image files and move images to class directory
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

            # Move the file to the destination
            shutil.move(path_file, dest_path)


    # Remove the directory from where the images were moved
    os.rmdir(path_extracted_imgs)
    print("Images predicted and sorted in 'Prediction' directory.")

    print(df2['Predictions'].value_counts())
