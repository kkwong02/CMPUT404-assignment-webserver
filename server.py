#  coding: utf-8
import socketserver
from pathlib import Path

from response import Response, NotFound, MovedPermanently, MethodNotAllowed
from response import ENCODING, Status

from exceptions import NotFoundError, MovedPermanentlyError

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

WWW = "www"  # the www directory


class MyWebServer(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        
        print(self.data.decode(ENCODING))

        request_info = self.data.decode(ENCODING).split()[:2]

        if request_info[0] != "GET":
            response = MethodNotAllowed(self.request)
        
        else:
            try:
                path = self.getPath(request_info[1])
            except NotFoundError:
                response = NotFound(self.request)
            except MovedPermanentlyError as e:
                response = MovedPermanently(self.request, location=e.location)
            else:
                response = self.getResponse(path)

        response.send()

    # getPath(self url)
    # returns a Path object for file to return.
    # checks if the file exists and is in the www directory.
    # raises NotFoundError if the file doesn't exist
    # raises PermanentlyMovedError if path is a directory but does not end in /
    def getPath(self, url):
        www = Path(WWW)
        path = Path(WWW + url)

        # done for compatibility with python 3.5, used on the lab machines.
        # python 3.6 does not throw an error on resolve if path doesn't exist.
        try:
            full_path = path.resolve()
        except FileNotFoundError:
            raise NotFoundError()

        # Check if path is in the www directory
        if www.resolve() not in full_path.parents and path.resolve() != www.resolve():
            print("not in www")
            raise NotFoundError()

        # if the path contains .. but is still in www 
        if '..' in path.parts:
            redirect_url = str(path.resolve().relative_to(Path(WWW).resolve()))

            if redirect_url == ".":
               # it goes to the root directory
                redirect_url = '/'
            else:
                redirect_url = "/" + redirect_url + "/"

            raise MovedPermanentlyError(redirect_url)
     
        # handling directories
        if path.is_dir() and not url.endswith('/'):
            raise MovedPermanentlyError(url + '/')
        elif path.is_dir():
            path = path / Path("index.html")

        # that the file actually exists
        if not path.is_file():
            print("File not found")
            raise NotFoundError()

        return path

    # getResponse(self, path)
    # creates a response object with a Path
    # assumes that the path goes to a file that exists.
    # TODO: catch file read errors
    def getResponse(self, path):
        contents = path.open().read()

        return Response(
            self.request,
            status=Status.OK,
            content=contents,
            headers={
                "Content-Type": "text/" + path.suffix[1:]
                }
            )


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    print("Serving HTTP on %s port %d ..." % (HOST, PORT))

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
