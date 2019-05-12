# -----------------------------------
# GLOBAL FEATURE EXTRACTION
# -----------------------------------

# organize imports
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from imutils import paths
import cv2
import os
import h5py

fixed_size = tuple((160, 120))

# path to training data
train_path = "./make_dataset/filtered_dataset/"

# no.of.trees for Random Forests
num_trees = 100

# bins for histogram
bins = 8

# train_test_split size
test_size = 0.15

# seed for reproducing same results
seed = 9


def histogram_of_oriented_gradients(image):
    winSize = (100, 100)
    blockSize = (10, 10)
    blockStride = (5, 5)
    cellSize = (10, 10)
    nbins = 9
    derivAperture = 1
    winSigma = -1.
    histogramNormType = 0
    L2HysThreshold = 0.2
    gammaCorrection = 1
    nlevels = 64
    signedGradients = True
    hog = cv2.HOGDescriptor(winSize, blockSize,
                            blockStride, cellSize,
                            nbins, derivAperture,
                            winSigma, histogramNormType,
                            L2HysThreshold, gammaCorrection,
                            nlevels, signedGradients)
    return hog.compute(image)


# get the training labels
train_labels = os.listdir(train_path)

# sort the training labels
train_labels.sort()
print(train_labels)

# empty lists to hold feature vectors and labels
global_features = []
labels = []

# num of images per class
images_per_class = 3500

# loop over the training data sub-folders
for training_name in train_labels:

    imagePaths = list(paths.list_images(train_path+training_name))

    # get the current training label
    current_label = training_name

    # loop over the images in each sub-folder
    for (i, file) in enumerate(imagePaths):

        # read the image and resize it to a fixed-size
        image = cv2.imread(file)

        # convert to grayscale
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        image = cv2.resize(image, fixed_size)

        ####################################
        # Global Feature extraction
        ####################################
        fv_hog = histogram_of_oriented_gradients(image)

        ###################################
        # Concatenate global features
        ###################################
        global_feature = np.hstack([fv_hog])

        # update the list of labels and feature vectors
        labels.append(current_label)

        # global_features.append(global_feature)
        global_features.append(global_feature)

    print("[STATUS] processed folder: {}".format(current_label))

print("[STATUS] completed Global Feature Extraction...")

print('Type of global feat = {}\n'.format(type(global_features)))
# get the overall feature vector size
print("[STATUS] feature vector size {}".format(
    np.array(global_features).shape))

# get the overall training label size
print("[STATUS] training Labels {}".format(np.array(labels).shape))

global_features = np.array(global_features)
print("shape of global feat = {}".format(np.array(global_features).shape))
nsamples, nx, ny = global_features.shape
global_features = global_features.reshape((nsamples, nx*ny))
print("shape of global feat = {}".format(np.array(global_features).shape))

# encode the target labels
targetNames = np.unique(labels)
le = LabelEncoder()
target = le.fit_transform(labels)
print("[STATUS] training labels encoded...")

# normalize the feature vector in the range (0-1)
scaler = MinMaxScaler(feature_range=(0, 1))

rescaled_features = scaler.fit_transform(global_features)

print("[STATUS] feature vector normalized...")

print("[STATUS] target labels: {}".format(target))
print("[STATUS] target labels shape: {}".format(target.shape))

# save the feature vector using HDF5
h5f_data = h5py.File('output/data.h5', 'w')
h5f_data.create_dataset('dataset_1', data=np.array(rescaled_features))

h5f_label = h5py.File('output/labels.h5', 'w')
h5f_label.create_dataset('dataset_1', data=np.array(target))

h5f_data.close()
h5f_label.close()

print("""
[STATUS] end of data generation for training..
Now you can run:  python3 ./training.py""")
