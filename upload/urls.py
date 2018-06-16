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

from django.views.generic.base import TemplateView
from upload.main import views
from django.contrib import admin
from django.urls import path, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^complete?/$', views.upload_complete, name='upload_complete'),
    path('robots\.txt/',TemplateView.as_view(template_name='main/robots.txt', 
                                               content_type='text/plain')),

    re_path(r'^$', views.UploadView.as_view(), name="index"),
    re_path(r'^table?/$', views.TableView.as_view(), name="table"),

]



