import os
import json

from django.conf import settings
from django.template.defaultfilters import slugify
from django.core.files.storage import FileSystemStorage


class FileStorage(FileSystemStorage):
    def __init__(self, location=None, base_url=None):
        location = location if location else settings.FILES_ROOT
        base_url = base_url if base_url else settings.FILES_URL
        super(FileStorage, self).__init__(location, base_url)

    def list(self):
        file_list = []
        for f in os.listdir(self.location):
            f_path = os.path.join(self.base_location, f)
            if os.path.isfile(f_path):
                f_size = os.path.getsize(f_path)
                file_list.append({
                    'name': f,
                    'id': slugify(f),
                    'url': self.base_url + f,
                    'size': f_size,
                })
        return file_list

    def delete(self, name):
        assert name, "The name argument is not allowed to be empty."
        name = self.path(name)
        try:
            if os.path.isfile(name):
                os.remove(name)
                return True
        except FileNotFoundError:
            pass
        return False


