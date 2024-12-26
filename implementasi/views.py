from django.shortcuts import render
from google.cloud import storage

# Create your views here.
def index(request):
    return render(request, 'index.html')

def create_cloud_bucket(request):
    storage_client = storage.Client()
    
    bucket_name = request.POST['bucket_name']
    storage_class = 'STANDARD'
    location = 'us-central1'
    
    bucket = storage_client.bucket(bucket_name)
    
    bucket.storage_class = storage_class
    
    bucket = storage_client.create_bucket(bucket, location=location)
    
    return render(request, 'index.html', {'message': f'Bucket {bucket.name} successfully created.'})

def list_cloud_files(request):
    storage_client = storage.Client()
    
    bucket_name = request.POST['bucket_name']
    
    file_list = storage_client.list_blobs(bucket_name)
    file_list = [file.name for file in file_list]
    
    return render(request, 'index.html', {'file_list': file_list})

def upload_cloud_file(request):
    storage_client = storage.Client()
    
    bucket_name = request.POST['bucket_name']
    source_file_name = request.POST['source_file_name']
    destination_file_name = request.POST['destination_file_name']
    
    bucket = storage_client.bucket(bucket_name)
    
    blob = bucket.blob(destination_file_name)
    blob.upload_from_filename(source_file_name)
    
    return render(request, 'index.html', {'message': f'File {source_file_name} uploaded to {destination_file_name}.'})

def download_cloud_file(request):
    storage_client = storage.Client()
    
    bucket_name = request.POST['bucket_name']
    file_name = request.POST['file_name']
    destination_file_name = request.POST['destination_file_name']
    
    bucket = storage_client.bucket(bucket_name)
    
    blob = bucket.blob(file_name)
    blob.download_to_filename(destination_file_name)
    
    return render(request, 'index.html', {'message': f'File {file_name} downloaded to {destination_file_name}.'})