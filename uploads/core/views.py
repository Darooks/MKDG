from django.shortcuts import render, redirect
from django.conf import settings

from uploads.core.models import Document
from uploads.core.forms import DocumentForm

from imagekit import ImageSpec
from imagekit.processors import ResizeToFill

from uploads.core.sobelTransformation import sobel

import os

class Thumbnail(ImageSpec):
    processors = [ResizeToFill(800, 600)]
    format = 'JPEG'
    options = {'quality': 100}

def home(request):
    documents = Document.objects.all()
    return render(request, 'core/simple_upload.html', { 'documents': documents })


def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        if os.path.isfile(os.path.join(settings.MEDIA_ROOT, 'image.jpg')):
            os.remove(os.path.join(settings.MEDIA_ROOT, 'image.jpg'))
        myfile = request.FILES['myfile']
        uploaded_file_url = sobel(myfile)
        #image_generator = Thumbnail(source=myfile)
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