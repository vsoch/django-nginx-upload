'''

Copyright (C) 2018 Vanessa Sochat.

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''

from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.db import models
import uuid
import time
import hashlib
import os



################################################################################
# Storage

def get_upload_to(instance, filename):
    filename = os.path.join(settings.UPLOAD_PATH, instance.upload_id + '.simg')
    return time.strftime(filename)


class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name



################################################################################
# Models 



class ImageFile(models.Model):
    ''' a base image upload to hold a file temporarily during upload
        based off of django-chunked-uploads BaseChunkedUpload model
    '''

    file = models.FileField(upload_to=get_upload_to, storage=OverwriteStorage())
    filename = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    size = models.BigIntegerField()
    created_on = models.DateTimeField(auto_now_add=True)

    def get_label(self):
        return "imagefile"

    def get_abspath(self):
        return os.path.join(settings.MEDIA_ROOT, self.datafile.name)

    @property
    def md5(self):
        '''calculate the md5 sum of the file'''
        if getattr(self, '_md5', None) is None:
            md5 = hashlib.md5()
            for chunk in self.file.chunks():
                md5.update(chunk)
            self._md5 = md5.hexdigest()
        return self._md5


    def delete(self, delete_file=True, *args, **kwargs):
        '''delete the file and make sure to also delete from storage'''
        if self.file:
            storage, path = self.file.storage, self.file.path
        super(ImageFile, self).delete(*args, **kwargs)
        if self.file and delete_file:
            storage.delete(path)

    class Meta:
        app_label = 'main'
