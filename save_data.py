
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np

import dicom 
import os 
import cv2
import matplotlib.pyplot as plt 
import h5py

IMG_SIZE = 150
curr_dir = os.getcwd()

path = os.path.join("data/CT_data_batch1")
_, patients, _ = next(os.walk(path))
data = []
labels = []

for patient in patients: 
    data_dir = os.path.join(path, patient, "DICOM_anon")
    gt_dir = os.path.join(path, patient, "Ground")
    
    imgs = os.listdir(data_dir)
    gts = os.listdir(gt_dir)
    list.sort(imgs)
    list.sort(gts)
    
    #read the dicom metadata
    dicom_refs = dicom.read_file(os.path.join(data_dir, imgs[1]))
    #figure out how big each slice is and how many slices 
    pixel_dims = (int(dicom_refs.Rows), int(dicom_refs.Columns), len(imgs))
    
    ct_img = np.zeros(pixel_dims, dtype=np.float64)
    ct_gt = np.zeros(pixel_dims, dtype=np.float64)
    
    for idx, filenameDCM in enumerate(imgs):
        ds = dicom.read_file(os.path.join(data_dir, filenameDCM))
        ct_img[:, :, idx] = ds.pixel_array
    
    for idx, gt_name in enumerate(gts):
        ct_gt[:,:,idx] = plt.imread(os.path.join(gt_dir, gt_name))

    tmp = (ct_img - np.min(ct_img)) / (np.max(ct_img) - np.min(ct_img))
    data.append(tmp)
    labels.append(ct_gt)

#resize and stack all the 2
for num,img in enumerate(data):
    tmp = cv2.resize(img, (IMG_SIZE, IMG_SIZE))        
    if num==0:
        x = tmp

    else:
        x = np.dstack((x,tmp))

for num,img in enumerate(data):
    tmp = cv2.resize(img, (IMG_SIZE, IMG_SIZE))        
    if num==0:
        x = tmp

    else:
        x = np.dstack((x,tmp))

'''
# VISUALIZATION
i = np.random.randint(0,len(patients))
sli = np.random.randint(0,70)
x = data[2]
plt.figure()
plt.imshow(x[:,:,sli])
plt.title('DATA - Patient ' + patients[i] + ' Slice ' + str(sli))

plt.figure()
y = labels[2]
plt.imshow(y[:,:,sli])
plt.title('GT - Patient ' + patients[i] + ' Slice ' + str(sli))
plt.show()



with h5py.File('ct-data.h5', 'w') as hf:
    hf.create_dataset('imgs', data=data)
    hf.create_dataset('gt', data=labels)
'''