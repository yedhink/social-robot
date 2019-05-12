# -----------------------------------
# TRAINING OUR MODEL
# -----------------------------------

# import the necessary packages
import constants
import h5py
import numpy as np
from sklearn.externals import joblib
import glob
import cv2
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV


def svc_param_selection(X, y, nfolds, svc):
    Cs = [0.001, 0.01, 0.1, 1, 10]
    gammas = [0.001, 0.01, 0.1, 1, 10]
    param_grid = {'C': Cs, 'gamma': gammas}
    grid_search = GridSearchCV(svc, param_grid, cv=nfolds, verbose=10)
    grid_search.fit(X, y)
    # grid_search.best_params_
    with open('best_svm_params.txt', 'a') as file:
        file.write("score : {}\nC : {}\nKernel : {}\nGamma : {}".format(grid_search.best_score_,
                                                                        grid_search.best_estimator_.C,
                                                                        grid_search.best_estimator_.kernel,
                                                                        grid_search.best_estimator_.gamma))
    return grid_search


# variables to hold the results and names
results = []
names = []
scoring = "accuracy"

# import the feature vector and trained labels
h5f_data = h5py.File('output/data.h5', 'r')
h5f_label = h5py.File('output/labels.h5', 'r')

global_features_string = h5f_data['dataset_1']
global_labels_string = h5f_label['dataset_1']

global_features = np.array(global_features_string)
global_labels = np.array(global_labels_string)

h5f_data.close()
h5f_label.close()

# verify the shape of the feature vector and labels
print("[STATUS] features shape: {}".format(global_features.shape))
print("[STATUS] labels shape: {}".format(global_labels.shape))

print("[STATUS] training started...")

# split the training and testing data
(trainDataGlobal, testDataGlobal, trainLabelsGlobal, testLabelsGlobal) = train_test_split(
    np.array(global_features),
    np.array(
        global_labels),
    test_size=constants.test_size,
    random_state=constants.seed)


# save test data for calc accuracy
h5f_data = h5py.File('output/test_data.h5', 'w')
h5f_data.create_dataset('dataset_1', data=np.array(testDataGlobal))

print("[STATUS] splitted train and test data...")
print("Train data  : {}".format(trainDataGlobal.shape))
print("Test data   : {}".format(testDataGlobal.shape))
print("Train labels: {}".format(trainLabelsGlobal.shape))
print("Test labels : {}".format(testLabelsGlobal.shape))

# -----------------------------------
# TESTING OUR MODEL
# -----------------------------------

# to visualize results

filename = './svmmodel.joblib.pkl'

svc = SVC(kernel='rbf', verbose=True)
clf = svc_param_selection(trainDataGlobal, trainLabelsGlobal, 5, svc)

joblib.dump(clf, filename, compress=9)
