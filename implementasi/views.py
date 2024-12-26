from django.shortcuts import render
from google.cloud import storage
from django.core import files
from django.core.files.uploadedfile import UploadedFile

# Create your views here.
def index(request):
    return render(request, 'index.html')

def create_cloud_bucket(request):
    if request.method == 'POST':
        storage_client = storage.Client()
        
        bucket_name = request.POST.get('bucket_name')
        if not bucket_name:
            return render(request, 'create.html', {'error': 'Bucket name is required.'})

        storage_class = 'STANDARD'
        location = 'us-central1'
        
        try:
            bucket = storage_client.bucket(bucket_name)
            bucket.storage_class = storage_class
            bucket = storage_client.create_bucket(bucket, location=location)
        except Exception as e:
            return render(request, 'create.html', {'error': f'Error creating bucket: {e}'})
        
        return render(request, 'create.html', {'message': f'Bucket {bucket.name} successfully created.'})
    
    return render(request, 'create.html')  # Render the form for GET requests.

def list_cloud_files(request):
    from google.cloud import storage

    if request.method == 'POST':
        bucket_name = request.POST.get('bucket_name')
        
        if not bucket_name:
            return render(request, 'list_file.html', {'error': 'Bucket name is required.'})

        storage_client = storage.Client()

        try:
            blobs = storage_client.list_blobs(bucket_name)
            file_list = [blob.name for blob in blobs]
            if not file_list:
                file_list = []  # Ensure empty list if no files are present
        except Exception as e:
            return render(request, 'list_file.html', {'error': f'Error retrieving files: {e}'})

        return render(request, 'list_file.html', {'bucket_name': bucket_name, 'file_list': file_list})

    return render(request, 'list_file.html', {'error': 'Invalid request method. Only POST is allowed.'})

def upload_cloud_file(request):
    if request.method == 'POST':
        bucket_name = request.POST.get('bucket_name')
        uploaded_file = request.FILES.get('file')
        destination_file_name = request.POST.get('destination_file_name', uploaded_file.name if uploaded_file else None)

        if not bucket_name or not uploaded_file:
            return render(request, 'insert_file.html', {'error': 'Bucket name and file are required.'})

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)

        blob = bucket.blob(destination_file_name)

        try:
            blob.upload_from_file(uploaded_file.file)
        except Exception as e:
            return render(request, 'insert_file.html', {'error': f'File upload failed: {e}'})

        return render(request, 'insert_file.html', {'message': f'File {uploaded_file.name} successfully uploaded to {destination_file_name} in bucket {bucket_name}.'})

    return render(request, 'insert_file.html', {'error': 'Invalid request method.'})

def download_cloud_file(request):
    from google.cloud import storage

    if request.method == 'GET':
        # Step 1: Display a form to input bucket name and retrieve file list
        return render(request, 'get_bucket_files.html')

    elif request.method == 'POST':
        if 'bucket_name' in request.POST:
            # Step 2: Retrieve files from the specified bucket
            bucket_name = request.POST.get('bucket_name')

            if not bucket_name:
                return render(request, 'get_bucket_files.html', {'error': 'Bucket name is required.'})

            storage_client = storage.Client()

            try:
                blobs = storage_client.list_blobs(bucket_name)
                file_list = [blob.name for blob in blobs]
            except Exception as e:
                return render(request, 'get_bucket_files.html', {'error': f'Error retrieving files: {e}'})

            return render(request, 'choose_file.html', {'bucket_name': bucket_name, 'file_list': file_list})

        elif 'file_name' in request.POST:
            # Step 3: Download the selected file
            bucket_name = request.POST.get('bucket_name')
            file_name = request.POST.get('file_name')
            destination_file_name = request.POST.get('destination_file_name')

            if not bucket_name or not file_name or not destination_file_name:
                return render(request, 'choose_file.html', {
                    'error': 'Bucket name, file name, and destination file name are required.',
                    'bucket_name': bucket_name,
                    'file_list': request.POST.getlist('file_list')
                })

            storage_client = storage.Client()
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(file_name)

            try:
                blob.download_to_filename(destination_file_name)
            except Exception as e:
                return render(request, 'choose_file.html', {
                    'error': f'File download failed: {e}',
                    'bucket_name': bucket_name,
                    'file_list': request.POST.getlist('file_list')
                })

            return render(request, 'download_file.html', {'message': f'File {file_name} downloaded to {destination_file_name}.'})

    return render(request, 'index.html', {'error': 'Invalid request method.'})
