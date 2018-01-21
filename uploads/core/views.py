from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from uploads.core.models import Document
from uploads.core.forms import DocumentForm

from imagekit import ImageSpec
from imagekit.processors import ResizeToFill

from skimage.color import rgb2gray
from skimage.color.adapt_rgb import adapt_rgb, each_channel, hsv_value
from skimage.exposure import rescale_intensity
from skimage import data
from skimage import filters
from PIL import Image
from numpy import*

import os
import matplotlib.pyplot as plt

class Thumbnail(ImageSpec):
    processors = [ResizeToFill(800, 600)]
    format = 'JPEG'
    options = {'quality': 100}

def as_gray(image_filter, image, *args, **kwargs):
    gray_image = rgb2gray(image)
    return image_filter(gray_image, *args, **kwargs)

@adapt_rgb(each_channel)
def sobel_each(image):
    return filters.sobel(image)

@adapt_rgb(as_gray)
def sobel_gray(image):
    return filters.sobel(image)

def home(request):
    documents = Document.objects.all()
    return render(request, 'core/simple_upload.html', { 'documents': documents })


def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        if os.path.isfile(os.path.join(settings.MEDIA_ROOT, 'image.jpg')):
            os.remove(os.path.join(settings.MEDIA_ROOT, 'image.jpg'))
        myfile = request.FILES['myfile']
        myfile.name = "image.jpg"
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        #image_generator = Thumbnail(source=myfile)
        temp = asarray(Image.open('media/'+myfile.name))
        image = temp
        fig = plt.figure(figsize=(14, 7))
        ax_each = fig.add_subplot(121, adjustable='box-forced')
        ax_each.imshow(rescale_intensity(1 - sobel_each(image)))
        ax_each.set_xticks([]), ax_each.set_yticks([])
        ax_each.set_title("Sobel filter computed\n on individual RGB channels")

        plt.savefig('media/'+myfile.name)
        uploaded_file_url = fs.url(filename)
        return render(request, 'core/simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'core/simple_upload.html')


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'core/model_form_upload.html', {
        'form': form
    })