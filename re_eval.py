#!/usr/bin/env python

"""
This script is used to re-evaluate the concentration of protists after manual
reclassification of pre-classified images. 

Execute the script inside the 'Output' directory. 
"""

import os
from datetime import datetime

try:
    with open('report.txt', 'r') as file:
        line = file.readlines()
        # fetch the line containing sample volume 
        volume_line = line[2]
        sample_volume_imaged = volume_line.split(':')[1].strip()
        
except FileNotFoundError:
    print(f"The file {file_path} does not exist.")

current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
count_protist = len(os.listdir('Predicted_images/Protist'))
count_junk = len(os.listdir('Predicted_images/Junk'))
sample_volume_imaged = float(sample_volume_imaged)

text_to_append = [
    "\n---------------------------------------------------------------",
    f"Manual reclassification \t ({current_time})",
    "\nCategories",
    f"Junk: {count_junk}",
    f"Protist: {count_protist}",
    f"\nConsentration (protists/ml): {count_protist/sample_volume_imaged:.2f}"
]

with open('report.txt', 'a') as file:
    for line in text_to_append:
        file.write(line + '\n')
        print(line)

