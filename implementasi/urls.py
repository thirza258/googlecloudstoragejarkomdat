from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_bucket', views.create_cloud_bucket, name='create_bucket'),
    path('list_files', views.list_cloud_files, name='list_files'),
    path('upload_file', views.upload_cloud_file, name='upload_file'),
    path('download_file', views.download_cloud_file, name='download_file'),
]