from django.core.files.storage import FileSystemStorage

from skimage.morphology import skeletonize
from skimage.color.adapt_rgb import adapt_rgb, each_channel, hsv_value
from skimage.exposure import rescale_intensity
from skimage import filters, img_as_float, img_as_bool, io, color, morphology, data, exposure
from PIL import Image
from numpy import *
import numpy as np
from django.conf import settings
import os
import scipy.misc
from skimage.util import invert
import matplotlib.pyplot as plt


IMAGE_URL = "/media/image_transformed.jpg"

@adapt_rgb(each_channel)
def sobel_each(image):
    return filters.sobel(image)


def sobel(myfile):
    image = asarray(Image.open(myfile))

    new_image_arr = rescale_intensity(1 - sobel_each(image))
    file_url = os.path.join(settings.MEDIA_ROOT) + "/image_transformed.jpg"
    scipy.misc.imsave(file_url, new_image_arr)

    return IMAGE_URL


def skeletonize(myfile):
    img = img_as_bool(color.rgb2gray(io.imread(myfile)))
    img = morphology.skeletonize(img)

    file_url = os.path.join(settings.MEDIA_ROOT) + "/image_transformed.jpg"
    scipy.misc.imsave(file_url, img)

    return IMAGE_URL

def contrast_log(myfile):
    img = color.rgb2gray(io.imread(myfile))
    # img = img_as_float(img)
    img = exposure.adjust_log(img, 1)

    file_url = os.path.join(settings.MEDIA_ROOT) + "/image_transformed.jpg"
    scipy.misc.imsave(file_url, img)

    return IMAGE_URL