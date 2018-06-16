#!/usr/bin/env python

'''

push.py: example of how to push image to nginx upload server!

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

from __future__ import print_function
from requests_toolbelt.streaming_iterator import StreamingIterator
from requests_toolbelt import (
    MultipartEncoder,
    MultipartEncoderMonitor
)

import requests
import argparse
import hashlib
import sys
import os


def get_parser():
    parser = argparse.ArgumentParser(description="Dinosaur Nginx Upload Example")

    description = 'example push client to upload files to nginx upload endpoint'

    parser.add_argument("--host", dest='host', 
                        help="the host where the server is running", 
                        type=str, default='127.0.0.1')

    parser.add_argument("--port", "-p", dest='port', 
                        help="the port where the server is running", 
                        type=str, default='')

    parser.add_argument("--schema", "-s", dest='schema', 
                        help="http:// or https://", 
                        type=str, default='http://')

    parser.add_argument("file", nargs=1,
                        help="full path to file to push", 
                        type=str)

    return parser



def main():
    '''the main entrypoint for pushing!
    '''

    parser = get_parser()

    # If the user didn't provide any arguments, show the full help
    if len(sys.argv) == 1:
        parser.print_help()
    try:
        args = parser.parse_args()
    except:
        sys.exit(0)

    # Assemble host / port url
    url = assemble_url(args.schema, args.host, args.port)

    # Pass on to the correct parser
    return_code = 0
    try:
        push(path=args.file[0], url=url)
        sys.exit(return_code)
    except UnboundLocalError:
        return_code = 1


def assemble_url(schema, host, port):
    if port:
        port = ':%s' % port
    return '%s%s%s/upload' %(schema, host, port)


def push(path, url):
    '''push an image to the dinosaur nginx upload server!

       Parameters
       ==========
       path: the full path to the image.

    '''

    path = os.path.abspath(path)
    image = os.path.basename(path)
    print("PUSH %s" % path)

    if not os.path.exists(path):
        print('ERROR: %s does not exist.' %path)
        sys.exit(1)

    image_size = os.path.getsize(path) >> 20

    upload_to = os.path.basename(path)

    encoder = MultipartEncoder(fields={'name': upload_to,
                                       'terminal': "yes",
                                       'file1': (upload_to, open(path, 'rb'), 'text/plain')})

    progress_callback = create_callback(encoder)
    monitor = MultipartEncoderMonitor(encoder, progress_callback)
    headers = {'Content-Type': monitor.content_type }

    try:
        r = requests.post(url, data=monitor, headers=headers)
        message = r.json()['message']
        print('\n[Return status {0} {1}]'.format(r.status_code, message))
    except KeyboardInterrupt:
        print('\nUpload cancelled.')
    except Exception as e:
        print(e)

    sys.stdout.write("\n")


def create_callback(encoder):
    encoder_len = int(encoder.len / (1024*1024.0))
    sys.stdout.write("[0 of %s MB]" % (encoder_len))
    sys.stdout.flush()
    def callback(monitor):
        sys.stdout.write('\r')
        bytes_read = int(monitor.bytes_read / (1024*1024.0))
        sys.stdout.write("[%s of %s MB]" % (bytes_read, encoder_len))
        sys.stdout.flush()
    return callback


if __name__ == '__main__':
    main()
