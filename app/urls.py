from django import urls
from django.urls import path
from .views import *
urlpatterns = [
    # path('upload_file',upload_file, name="upload_file"),
    path('',file,name="file"),
    path('Inc_upload',Inc_upload_file, name="Inc_upload"),
    
]
