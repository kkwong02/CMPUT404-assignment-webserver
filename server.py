#  coding: utf-8
import socketserver
from pathlib import Path

from response import Response, NotFound
from response import ENCODING, Status

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
            response = Response(
                self.request,
                status=Status.METHOD_NOT_ALLOWED
                )
        
        else:
            if request_info[1].endswith('/'):
                response = self.getFileResponse(Path(WWW + request_info[1] + "index.html"))

            else:
                path = Path(WWW + request_info[1])
                    
                if Path(WWW).resolve() not in path.resolve().parents:
                    response = NotFound(request=self.request)

                elif path.is_dir():
                    response = Response(
                        request=self.request,
                        status=Status.MOVED_PERMANENTLY,
                        headers={
                            "Location": request_info[1] + '/'
                        }
                    )

                elif path.is_file():
                    response = self.getFileResponse(path)
                    
                else:
                    response = NotFound(request=self.request)

        response.send()

    def getFileResponse(self, path):
        try:
            contents = path.open()

        except FileExistsError:
            return NotFound(self.request)

        return Response(
            self.request,
            status=Status.OK,
            content=contents.read(),
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
