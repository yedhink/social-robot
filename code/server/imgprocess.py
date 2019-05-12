import cv2

# bins for histogram
bins = 8


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
