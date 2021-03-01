import os

from django.conf import settings
from django.utils.module_loading import import_string
from storages.backends.s3boto3 import S3Boto3Storage


def get_storage(upload_to=''):
    storage_class = import_string(settings.DEFAULT_FILE_STORAGE)
    if storage_class is S3Boto3Storage:
        # aws s3
        return storage_class(location=upload_to)
    else:
        # django default FileSystemStorage
        return storage_class()


def storage_save(upload_to, name, file):
    fs = get_storage(upload_to)
    if not isinstance(fs, S3Boto3Storage):
        name = os.path.join(upload_to.strip('/'), name.strip('/'))

    filename = fs.save(name, file)
    return filename, fs.url(filename)
