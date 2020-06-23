'''Logging configuration file.'''
# Built in imports
import logging
import logging.config
from os import path

# Resolve the log configuration file location.
log_file_path = path.join(path.dirname(path.abspath(__file__)), 'log.conf')
print(path.dirname(path.abspath(__file__)))
# Configure the logger for the dealership application.
logging.config.fileConfig(log_file_path)
# Creates an instance of the logging class and names the instance after the current file name.
LOGGER = logging.getLogger(__name__)
'''Sets the logging level to INFO so that all logs greater than or equal
   to INFO in priority are recorded during runtime.'''
LOGGER.setLevel(level=logging.INFO)
# Creates an instance of the HANDLER method, which creates a file output named log.txt.
HANDLER = logging.FileHandler('bank.log')
# Adds the HANDLER static variable to the logger object.
LOGGER.addHandler(HANDLER)
# Creates a string format for all logs that are recorded by the LOGGER instance.
FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# Sets the string format for the file output HANDLER.
HANDLER.setFormatter(FORMATTER)
# Creates the first log in this program's run time.
logging.info('this is the root logger')


# A function that returns a pointer to the active instance of the logging class object.
def get_logger(name):
    '''returns a logger for the module that called the function'''
    return logging.getLogger(name)
