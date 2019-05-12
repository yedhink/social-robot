import storage as st
import numpy as np
from sklearn.externals import joblib
import cv2
from imgprocess import histogram_of_oriented_gradients

filename = './svmmodel.joblib.pkl'

fixed_size = ((100, 100))

global_prediction = None


def feat_extract(image):
    hog_feat = histogram_of_oriented_gradients(image)
    ###################################
    # Concatenate global features
    ###################################
    global_feature = np.hstack([hog_feat])
    return global_feature


def predict(fname, labels):
    global global_prediction
    feat = []
    model = joblib.load(filename)
    image = cv2.imread(st.__UPLOADS__+fname)
    # resize the image
    image = cv2.resize(image, fixed_size)
    # convert to grayscale
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gf = feat_extract(image)
    pred = model.predict(gf.reshape(1, -1))[0]
    pred1 = labels[int(pred)]
    feat.append(str(pred1).strip('[]\''))
    if len(feat) != 0:
        global_prediction = feat[0]
    else:
        global_prediction = "Nil"
    print("\n\npredictions = {}".format(feat))
    return feat
