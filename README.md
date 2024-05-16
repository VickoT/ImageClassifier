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
conda install pandas scikit-learn opencv
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
    └── Predicted_images
        ├── Junk
        └── Protist
```
