# defining constants
ENCODING = "utf-8"  # encoding
VERSION = "HTTP/1.1"  # HTTP version


class Status:
    METHOD_NOT_ALLOWED = "405 Method Not Allowed"
    NOT_FOUND = "404 Not Found"
    OK = "200 OK"
    MOVED_PERMANENTLY = "301 Moved Permanently" # need Location header


# Response
# A class representing a HTTP 1.1 response.
# Attributes
# status: status code and text. as a string
# content: Content to be sent in response
# request: the origin request
# headers: a dictionary containing general header, response header and entity
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
        self.status = kwargs.get("status", Status.OK)
        self.content = kwargs.get("content", '')
        self.headers = (kwargs.get("headers"), {})

    # getHeader()
    # creates header of HTTP response
    # combines status and headers into a bytearray that can be sent
    def getHeader(self):
        return bytearray("%s %s \r\n\r\n" % (VERSION, self.status), ENCODING)
    
    # getContent()
    # returns message-body of response as bytearray
    def getContent(self):
        return bytearray(self.content, ENCODING)

    # send()
    # combines headers and content and sends response.
    def send(self):
        self.request.sendall(self.getHeader())
        if self.content:
            self.request.sendall(self.getContent())


# Subclasses of Response for error messages
class NotFound(Response):
    status = Status.NOT_FOUND


class MethodNotAllowed(Response):
    status = Status.METHOD_NOT_ALLOWED
    headers = {"Allow": "GET"}