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

from upload.main.models import ImageFile
from upload.settings import MEDIA_ROOT
import shutil
import uuid
import json
import os


def move_upload_to_storage(source, name):
    '''moving an uploaded file (from nginx module) to storage means.
         1. create a folder for the collection, if doesn't exist
         2. an image in storage pointing to the moved file

         Parameters
         ==========
         collection: the collection the image will belong to
         source: the source file (under /var/www/images/_upload/{0-9}
         dest: the destination filename
    '''
    new_path = os.path.join(MEDIA_ROOT, os.path.basename(name))
    shutil.move(source, new_path)
    return new_path


def upload_file(name, version, path, size=None):
    '''save an uploaded container, usually coming from an ImageUpload

       Parameters
       ==========
       path: the path to the file uploaded
       name: the requested name for the container
       version: the md5 sum of the file
       size: the file size. if not provided, is calculated

    '''

    if os.path.exists(path):
        new_path = move_upload_to_storage(path, name)
        image = ImageFile.objects.create(file=new_path,
                                         size=size,
                                         version=version,
                                         filename=os.path.basename(new_path))

        image.save()
        return image
