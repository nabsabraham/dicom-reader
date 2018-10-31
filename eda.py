# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import tensorflow as tf 
import dicom 
import os 
import matplotlib.pyplot as plt 



curr_dir = os.getcwd()

IMG_PATH = os.path.join(curr_dir,"data/CT_data_batch1/8/DICOM_anon")
imgs = os.listdir(IMG_PATH)

# Get ref file
RefDs = dicom.read_file(os.path.join(curr_dir, IMG_PATH, imgs[20]))

# Load dimensions based on the number of rows, columns, and slices (along the Z axis)
ConstPixelDims = (int(RefDs.Rows), int(RefDs.Columns), len(imgs))

# Load spacing values (in mm)
ConstPixelSpacing = (float(RefDs.PixelSpacing[0]), float(RefDs.PixelSpacing[1]), float(RefDs.SliceThickness))

x = np.arange(0.0, (ConstPixelDims[0]+1)*ConstPixelSpacing[0], ConstPixelSpacing[0])
y = np.arange(0.0, (ConstPixelDims[1]+1)*ConstPixelSpacing[1], ConstPixelSpacing[1])
z = np.arange(0.0, (ConstPixelDims[2]+1)*ConstPixelSpacing[2], ConstPixelSpacing[2])

# The array is sized based on 'ConstPixelDims'
ArrayDicom = np.zeros(ConstPixelDims, dtype=RefDs.pixel_array.dtype)

# loop through all the DICOM files
for idx, filenameDCM in enumerate(imgs):
    # read the file
    ds = dicom.read_file(os.path.join(curr_dir, IMG_PATH, filenameDCM))
    # store the raw image data
    ArrayDicom[:, :, idx] = ds.pixel_array  

plt.figure()    
plt.imshow(ArrayDicom[:,:,1], cmap='gray')
plt.title(imgs[20])
#dirName, subdirList, fileList = next(os.walk('/data/CT_data_batch1')) 