'''
    The Mongo.py module handles all Mongo Database operations using the pymongo library.

    The MongoServer class handles all MongoDB operations from the command line.
    Requires:   nothing
    Optional:   uri (str): A string specifying the url location with username and password.
    Modifies:   client (MongoClient): An instance of a MongoDB server connection.
                database (Database): Access to a specific databse on a MongoDB cluster.
                collection (Document): A document within a specific database on a MongoDB cluster.
    Effects:    Creates a MongoDB server connection if the uri is valid.
'''
# Built-in Modules
import socket
# External Modules
from pymongo import MongoClient
from decouple import config
# Internal Modules
from bank.data.logger import get_logger

_LOG = get_logger(__name__)

class MongoServer:
    '''MongoServer Class'''
    def __init__(self):
        # Logging entrance to the MongoServer class constructor.
        _LOG.info('Entering dealership.data.mongo.MongoServer object instance class constructor.')
        # MongoDB client cursor member variable.
        # Establish a connection with an administrative account.
        self.client = MongoClient(config('MONGO_URI'))
        # Database member variable.
        # Select the dealership database
        self.database = self.client['bank']
        # Collection names variable.
        # Select the cars collection.
        self.collection_names = None
        # Collection member variable.
        self.collection = self.database['loans']
        # Host name of the current computer
        self.hostname = None
        # IP Address of the current computer
        self.ip_address = None
        # Logging exit of the MongoServer class constructor
        _LOG.info('Exiting dealership.data.mongo.MongoServer object instance class constructor.')

    def create_user(self, query: dict):
        '''Creates a user on the selected MongoDB database.'''
        _LOG.info('Entering the dealership.data.MongoServer.create_user method.')
        query.update(query)
        self.database.add_user(query)
        _LOG.info('Exiting the dealership.data.MongoServer.create_user method.')

    def login(self, username, password, query):
        '''MongoDB login method.'''
        _LOG.info('Entering the dealership.data.MongoServer.login method.')
        database = self.client['users']
        collection = database['users']
        user = collection.find_one(query)
        if user:
            self.client = MongoClient(config('EMPTY_URI') % (username, password))
        _LOG.info('Exiting the dealership.data.MongoServer.login method.')
        return user

    def create_database(self, name):
        '''Creates a database stores the client within the MongoServer object.'''
        _LOG.info('Entering dealership.data.MongoServer.create_database method.')
        self.database = self.client[name]
        sel = input('Would you like to use this database now? Y/N: ')
        if sel in ('y', 'Y'):
            self.database = self.client[name]
        else:
            pass
        _LOG.info('Exiting dealership.data.MongoServer.create_database method.')

    def select_database(self, name):
        '''Selects the specified database and stores the database within the MongoServer object.'''
        _LOG.info('Entering dealership.data.MongoServer.select_database method.')
        self.database = self.client[name]
        _LOG.info('Exiting dealership.data.MongoServer.select_database method.')
        return self.database

    def remove_database(self, name):
        '''Removes the specified database.'''
        _LOG.info('Entering dealership.data.MongoServer.remove_database method.')
        self.client.drop_database(name)
        _LOG.info('Exiting dealership.data.MongoServer.remove_database method.')

    def get_collection_names(self):
        '''Returns all of the collections within the currently selected database.'''
        _LOG.info('Entering dealership.data.MongoServer.get_collection_names method.')
        if self.database is None:
            _LOG.error('No database selected.')
            return 'No collections found.'
        _LOG.info('Exiting dealership.data.MongoServer.get_collection_names method')
        return self.database.list_collection_names()

    def select_collection(self, name):
        '''Selects the specified collection and stores it within the MongoServer object.'''
        _LOG.info('Entering dealership.data.MongoServer.select_collection method.')
        self.collection = self.database[name]
        _LOG.info('Exiting dealership.data.MongoServer.select_collection method.')
        return self.collection


    def get_collection(self, name):
        '''Returns the entire specified collection.'''
        _LOG.info('Entering dealership.data.MongoServer.get_collection method.')
        _LOG.info('Exiting dealership.data.MongoServer.get_collection method.')
        return self.collection[name].find()

    def get_address(self):
        '''Ip address retrieval for the client or host.'''
        _LOG.info('Entering the dealership.data.MongoServer.get_address method.')
        self.hostname = socket.gethostname()
        self.ip_address = socket.gethostbyname()
        _LOG.info('Your Computer Name is: %s', self.hostname)
        _LOG.info('Your Computer IP Address is: %s', self.ip_address)
        _LOG.info('Exiting the dealership.data.MongoServer.get_address method.')
        return self.ip_address
