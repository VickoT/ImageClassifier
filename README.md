# ImageClassifier
**Author:** Viktor Törnblom

## Introduction
ImageClassifier is a Python-based application designed for classifying images using a machine-learning classifier algorithm. It is specifically tailored for processing FlowCam output and categorizing images into predefined classes, either "Junk" or "Protists".

## Prerequisites
- Anaconda or Miniconda

## Installation

*  Create and activate the conda environment:

```
conda create -n image_classifier python=3.12
conda activate image_classifier
```
 * Install required modules:

```
conda install pandas scikit-learn
pip install opencv-python
```

## Run ImageClassifier

```
conda activate image_classifier
python \path\to\script\image_classifier.py -raw_dir example_dir
```

'Example dir' should contain the raw FlowCam output data (the script uses the tif files and the metadata csv file).

The following directory will be generated after running the script, where the subdirectories 'Junk' and 'Protist' contains the images sorted into its corresponding class. 
```
└── Output_example_dir
    ├── report.txt
    └── Predicted_images
        ├── Junk
        └── Protist
```

#### Manual reclassification

In case you are unsatisfied with the classification made by the classifier, you may reclassify the images manually. This is done by moving the images in the 'Predicted_images' directory into the folder you find suitable. Then run the script `re_eval.py` inside the **Output_example_dir**. The new stats will be appended to the report file:

```
 Report - 4-LRM1b-day0-1         (2024-05-24 10:00)
=========================
Sample Volume Imaged (ml): 0.02031

Categories
Junk: 347
Protist: 653

Estimated conc. (protists/ml): 32151.65

---------------------------------------------------------------
Manual reclassification          (2024-05-24 10:29)

Categories
Junk: 499
Protist: 501

Estimated conc. (protists/ml): 24667.56
```
