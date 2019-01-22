from datetime import datetime
import locale

locale.setlocale(locale.LC_TIME, 'en_US.utf-8')

# defining constants
ENCODING = "utf-8"  # encoding
VERSION = "HTTP/1.1"  # HTTP version


class Status:
    METHOD_NOT_ALLOWED = "405 Method Not Allowed"
    NOT_FOUND = "404 Not Found"
    OK = "200 OK"
    MOVED_PERMANENTLY = "301 Moved Permanently"  # need Location header


# Response
# A class representing a HTTP 1.1 response.
# Attributes
# status: status code and text. as a string
# content: Content to be sent in response
# request: the origin request
# header fields.
class Response:
    # content-type
    # Date RFC 1123
    # Expect

    status = None
    content = None
    request = None
    headers = None
 
    def __init__(self, request, **kwargs):
        self.request = request

        if "status" in kwargs:
            self.status = kwargs.get("status")
        
        if "content" in kwargs:
            self.content = kwargs.get("content")
        
        self.headers = kwargs.get("headers", dict())

        self.headers["Server"] = "WebServer/0.0.1"
        self.headers["Date"] = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

    # getHeader()
    # creates header of HTTP response
    # combines status and headers into a bytearray that can be sent
    def getHeader(self):
        status_line = "%s %s\r\n" % (VERSION, self.status)
        headers = ""
        for field, value in self.headers.items():
            headers += "%s: %s\r\n" % (field, value)

        print("%s%s\r\n" % (status_line, headers))
        return "%s%s\r\n" % (status_line, headers)

    # send()
    # combines headers and content and sends response.
    def send(self):
        self.request.sendall(self.getHeader().encode(ENCODING))

        if self.content:
            self.request.sendall(self.content.encode(ENCODING))


# Subclasses of Response for error messages
class NotFound(Response):
    status = Status.NOT_FOUND


class MethodNotAllowed(Response):
    status = Status.METHOD_NOT_ALLOWED
    headers = {"Allow": "GET"}