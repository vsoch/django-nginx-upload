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

from django.http import JsonResponse
from django.shortcuts import ( redirect, render )
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from upload.main.utils import upload_file
from upload.main.models import ImageFile



@csrf_exempt
def upload_complete(request):
    '''view called on /upload/complete after nginx upload module finishes.

       1. nginx module uses /upload
       2. callback comes here with multipart form fields below!

    '''
    print(request)

    if request.method == "POST":

        path = request.POST.get('file1.path')
        size = request.POST.get('file1.size')
        filename = request.POST.get('file1.name')
        terminal = request.POST.get('terminal') # is the request from terminal?
        version = request.POST.get('file1.md5')

        # You should implement some sort of authorization check here!

        # Expected params are upload_id, name, md5, and cid
        upload_file(version = version,
                    path = path,
                    name = filename,
                    size = size)

        # Redirect to main view if not terminal
        if terminal == "no":
            print('Terminal is no!')
            return redirect('table')

        return JsonResponse({"message":"Upload Complete"})

    return redirect('table')



class TableView(TemplateView):
    template_name = 'main/table.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['uploads'] = ImageFile.objects.all()
        return context

class UploadView(TemplateView):
    template_name = 'main/index.html'
