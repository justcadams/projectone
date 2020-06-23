''' A handler serving as the front controller of our application '''
# Built-in Modules
from os import path
# External Modules
from http.server import SimpleHTTPRequestHandler
# Internal Modules
from bank.data.logger import get_logger
from bank.web.mapper import get_dispatcher, get_static_location


_FILE_PATH = path.dirname(path.abspath(__file__))
_STATIC_PATH = path.join(path.dirname(_FILE_PATH), ('static'))
_MIME_DICT = {
    'css': 'text/css',
    'js': 'text/javascript',
    'json': 'application/json'
}

_LOG = get_logger(__name__)

class ServerError(Exception):
    '''Server error handler.'''
    def __init__(self, value):
        super().__init__()
        self.value = value
    def __str__(self):
        return repr(self.value)

class AppHandler(SimpleHTTPRequestHandler):
    '''A handler for http methods on our server'''
    def do_get(self):
        '''Handles a GET request to the server'''
        _LOG.debug('Handling a GET request')
        self.do_controller('GET')
    def do_post(self):
        '''Handles a POST request to the server'''
        _LOG.debug('Handling a POST request')
        self.do_controller('POST')
    def do_put(self):
        '''Handles a PUT request to the server'''
        _LOG.debug('Handling a PUT request')
        self.do_controller('PUT')
    def do_delete(self):
        '''Handles a DELETE request to the server'''
        _LOG.debug('Handling a DELETE request')
        self.do_controller('DELETE')
    def do_controller(self, method):
        '''Handles a Get request to the server'''
        _LOG.debug(self.path) #self.path represents a URI that was requested from the server.
        destination = self.path[1:].split('/')
        if not destination[-1]:
            destination = destination[:-1]
        if len(destination) > 0:
            context = destination[0]
            dispatcher = get_dispatcher(context)
            _LOG.debug(dispatcher)
            if dispatcher:
                # rfile is the input from the client (body of the request)
                # destination is the path of the request
                req_string = None
                response_tuple = None
                if 'Content-Length' in self.headers:
                    try:
                        req_string = self.rfile.read(int(self.headers['Content-Length']))
                    except ServerError(self.send_error(400, b'Request not understood by server.'
                                                       )) as error:
                        _LOG.exception('Could not read request body, %s', error)
                        self.custom_send_response(400, b'Request not understood by server.')
                    else:
                        response_tuple = dispatcher.dispatch(destination, method, r_body=req_string)
                else:
                    response_tuple = dispatcher.dispatch(destination, method)

                # If dispatcher returns 3
                if len(response_tuple) == 3:
                    self.custom_send_response(response_tuple[0],
                                              response_tuple[1], response_tuple[2])
                # If dispatcher returns 2
                elif len(response_tuple) == 2:
                    self.custom_send_response(response_tuple[0], response_tuple[1])
                else:
                    self.custom_send_response(400, b'Request not understood by server.')
            # If dispatcher doesn't pick up a non-get
            elif method != 'GET':
                self.custom_send_response(405, b'Method not allowed')
            # Static Locations
            elif get_static_location(context):
                #grabs static location if html
                self.retrieve_static_resource(get_static_location(context))
            # Static Content
            elif context == 'static':
                #grabs static location if css or js
                self.retrieve_static_resource(destination)
                _LOG.debug("why")
            else:
                self.custom_send_response(404, bytes('Resource not found', 'utf-8'))
                return

    def custom_send_response(self, status: int, body: bytes, content_type='text/html'):
        '''Takes in a status code and a request body and writes them to the response'''
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.end_headers()
        self.wfile.write(body)

    def retrieve_static_resource(self, destination: list):
        '''Takes in a list of paths and writes the resulting static file to the response'''
        file_path = _STATIC_PATH
        for part in destination[1:]:
            file_path = path.join(file_path, part)
        if destination[1] in _MIME_DICT:
            self.send_file(file_path, text_type=_MIME_DICT[destination[1]])
        else:
            self.send_file(file_path)

    def send_file(self, file_path: str, text_type='text/html'):
        '''Takes in a file_path as a string, checks to see if it's valid,
           writes the file to response or sends 404 if not valid '''
        if path.exists(file_path):
            value = open(file_path, 'rb').read()
            _LOG.debug(text_type)
            self.custom_send_response(200, value, content_type=text_type)
        else:
            self.custom_send_response(404, bytes('File not found'))

if __name__ == '__main__':
    _LOG.debug(_file_path)
    _file_path = path.join(path.dirname(_file_path), ('static'))
    _LOG.debug(_file_path)
    _LOG.debug(path.exists(_file_path))
