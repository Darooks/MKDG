from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

class TransformImage():
    def transform(imagePath):
        fs = FileSystemStorage()
        image = fs.open(imagePath)

