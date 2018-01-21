from django.core.files.storage import FileSystemStorage

from skimage.color.adapt_rgb import adapt_rgb, each_channel, hsv_value
from skimage.exposure import rescale_intensity
from skimage import filters
from PIL import Image
from numpy import*
from django.conf import settings
import os
import PIL
import scipy.misc

import matplotlib.pyplot as plt

@adapt_rgb(each_channel)
def sobel_each(image):
    return filters.sobel(image)


def sobel(myfile):
    image = asarray(Image.open(myfile))

    new_image_arr = rescale_intensity(1 - sobel_each(image))
    file_url = os.path.join(settings.MEDIA_ROOT) + "/image_transformed.jpg"
    scipy.misc.imsave(file_url, new_image_arr)

    return "/media/image_transformed.jpg"