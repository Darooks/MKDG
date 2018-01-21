from django.core.files.storage import FileSystemStorage

from skimage.color.adapt_rgb import adapt_rgb, each_channel, hsv_value
from skimage.exposure import rescale_intensity
from skimage import filters
from PIL import Image
from numpy import*

import matplotlib.pyplot as plt

@adapt_rgb(each_channel)
def sobel_each(image):
    return filters.sobel(image)

def sobel(myfile):
    myfile.name = "image.jpg"
    fs = FileSystemStorage()
    filename = fs.save(myfile.name, myfile)
    image = asarray(Image.open('media/' + myfile.name))
    fig = plt.figure(figsize=(14, 9))
    ax_each = fig.add_subplot(111)
    ax_each.imshow(rescale_intensity(1 - sobel_each(image)))
    ax_each.set_xticks([]), ax_each.set_yticks([])
    ax_each.set_title("Sobel filter computed\n on individual RGB channels")

    plt.savefig('media/' + myfile.name)

    return fs.url(filename)