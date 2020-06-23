'''This module is the start of the loan approval system application.'''
# Import External Modules
import socketserver
# Import Custom Modules
from bank.data.logger import get_logger
from bank.web.controller import AppHandler

# Constants
# Creates an instance of the logging class and names the instance after the current file name.
_LOG = get_logger(__name__)
PORT = 8080

# User interface
with socketserver.TCPServer(('', PORT), AppHandler) as httpd:
    _LOG.info('Serving bank application on port: %s', PORT)
    httpd.serve_forever()
