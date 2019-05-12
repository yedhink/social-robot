from skimage import filters, io
from imutils import paths
import matplotlib.pyplot as plt
import os
from shutil import copy2


data_path = "./make_dataset/filtered_dataset/"
if not os.path.exists(data_path):
    os.makedirs(data_path, exist_ok=True)


train_path = "../dataset/train/"
train_labels = os.listdir(train_path)
train_labels.sort()


def apply_filters_and_save(image, save_dir, filename, color_img, dest):

    copy2(color_img, dest+"/")

    plt.imsave(save_dir+"/"+filename+"_unknown_filter.jpg", image)

    hessian_filter = filters.hessian(image)
    plt.imsave(save_dir+"/"+filename+"_hessian.jpg", hessian_filter)

    sobel_edges = filters.sobel(image)
    plt.imsave(save_dir+"/"+filename+"_sobel.jpg", sobel_edges)

    gaussian_filter = filters.gaussian(image)
    plt.imsave(save_dir+"/"+filename+"_gaussian.jpg", gaussian_filter)

    gabor_filter, abc = filters.gabor(image, frequency=0.6)
    plt.imsave(save_dir+"/"+filename+"_gabor.jpg", gabor_filter)

    frangi_filter = filters.frangi(image)
    plt.imsave(save_dir+"/"+filename+"_frangi.jpg", frangi_filter)


for training_name in train_labels:
    save_dir = data_path+training_name
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    imagePaths = list(paths.list_images(train_path+training_name))
    for (i, file) in enumerate(imagePaths):
        image = io.imread(file, as_gray=True)
        print(save_dir+"/"+str(i+1)+".jpg")
        apply_filters_and_save(image, save_dir, str(i+1), file, save_dir)
