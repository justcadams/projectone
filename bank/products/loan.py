'''The loan class contains the model for all loans required by the Loan Approval System'''
# Built-in Modules
import json
from datetime import datetime
# External Modules
from uuid import uuid4
# Internal Modules
from bank.data.logger import get_logger

_LOG = get_logger(__name__)

class Loan:
    '''Bank.product.loan.Loan class'''
    def __init__(self, _id='', product_type='', cosigner='', collateral='', manager=''):
        '''Bank.product.loan.Loan constructor'''
        _LOG.info('Entering the Bank.product.loan.Loan constructor.')
        if _id:
            self._id = _id
        else:
            self._id = uuid4()
        if product_type:
            self.product_type = product_type
        else:
            self.product_type = self.__class__.__name__
        self.cosigner = cosigner
        self.collateral = collateral
        self.manager = manager
        _LOG.info('Exiting the Bank.product.loan.Loan constructor.')

    def __str__(self):
        '''Class to string method.'''
        _LOG.info('Entering the Bank.product.loan.Loan.__str__ method.')
        string = 'Loan id: ' + self._id + ' is a ' + self.product_type + '.\n'
        if self.cosigner:
            string += self.cosigner + ' is the co-signer for this loan.\n'
        if self.collateral:
            string += self.collateral + ' is being used as collateral.\n'
        if self.manager:
            string += self.manager + ' is the manager assigned to this loan.\n'
        _LOG.info('Entering the Bank.product.loan.Loan.__str__ method.')
        return string

    def __repr__(self):
        '''Class representation method.'''
        _LOG.info('Entering the Bank.product.loan.Loan.__repr__ method.')
        _LOG.info('Exiting the Bank.product.loan.Loan.__repr__ method.')
        return self.__str__()

    def to_dict(self):
        '''Creates and returns a dictionary representation of instance'''
        _LOG.info('Entering the Bank.product.loan.Loan.to_dict method.')
        _LOG.info('Exiting the Bank.product.loan.Loan.to_dict method.')
        return self.__dict__

    @classmethod
    def from_dict(cls, input_dict):
        '''Creates an instance of the class from a dictionary input'''
        _LOG.info('Entering the Bank.product.loan.Loan.from_dict method.')
        # Create a new movie
        loan = cls()
        # Take the input_dict data and put it inside of the Loan
        loan.__dict__.update(input_dict)
        # Return the Loan
        _LOG.info('Exiting the Bank.product.loan.Loan.from_dict method.')
        return loan

class Mortgage(Loan):
    '''Bank.product.loan.Mortgage(Loan) class'''
    def __init__(self, _id='', product_type='', cosigner='', collateral='', manager=''):
        '''Bank.product.loan.Mortgage(Loan) constructor'''
        _LOG.info('Entering the Bank.product.loan.Mortgage(Loan) constructor.')
        super().__init__(_id='', product_type='', cosigner='', collateral='', manager='')
        _LOG.info('Exiting the Bank.product.loan.Mortgage(Loan) constructor.')

class CarLoan(Loan):
    '''Bank.product.loan.CarLoan(Loan) class'''
    def __init__(self, _id='', product_type='', cosigner='', collateral='', manager=''):
        '''Bank.product.loan.CarLoan(Loan) constructor'''
        _LOG.info('Entering the Bank.product.loan.CarLoan(Loan) constructor.')
        super().__init__(_id='', product_type='', cosigner='', collateral='', manager='')
        _LOG.info('Exiting the Bank.product.loan.CarLoan(Loan) constructor.')

class PersonalLoan(Loan):
    '''Bank.product.loan.PersonalLoan(Loan) class'''
    def __init__(self, _id='', product_type='', cosigner='', collateral='', manager=''):
        '''Bank.product.loan.PersonalLoan(Loan) constructor'''
        _LOG.info('Entering the Bank.product.loan.PersonalLoan(Loan) constructor.')
        super().__init__(_id='', product_type='', cosigner='', collateral='', manager='')
        _LOG.info('Exiting the Bank.product.loan.PersonalLoan(Loan) constructor.')

class StudentLoan(Loan):
    '''Bank.product.loan.StudentLoan(Loan) class'''
    def __init__(self, _id='', product_type='', cosigner='', collateral='', manager=''):
        '''Bank.product.loan.StudentLoan(Loan) constructor'''
        _LOG.info('Entering the Bank.product.loan.StudentLoan(Loan) constructor.')
        super().__init__(_id='', product_type='', cosigner='', collateral='', manager='')
        _LOG.info('Exiting the Bank.product.loan.StudentLoan(Loan) constructor.')

class ProductEncoder(json.JSONEncoder):
    ''' Allows us to serialize our objects as JSON '''
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.__str__()
        return o.to_dict()
