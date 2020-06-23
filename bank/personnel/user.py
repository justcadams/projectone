'''
User(), User(type)

The user class is a modular parent base class that may be inherited to provide extensibility for
creating custom user accounts. Custom user classes inherit the user base class and define the
functionality of virtual functions, while standard user functions are provided to all users.
Specific fields are only available to specific users on MongoDB. This ensures that the Principle
of Least Privilege is enforced at the application, session, network, and hardware layer. When data
is at rest the personal information is encrypted and obfuscated. Getter and setter functions allow
the system to service user requests for personal information.

Requires: Default Constructor: Nothing
          Custom User Constructor: String type - Type of user.
          (Uses dictionary to look up acceptable user types).
Modifies: User parameters in accordance with Principle of Least Privilege.
Effects: Creates a user of the specified type. If type is not specified,
         then the user is added as a customer.
'''

# External Modules
from uuid import uuid4

# Internal Modules
from bank.products.loan import Loan
from bank.data.logger import get_logger

_LOG = get_logger(__name__)
INSTANCE_ATTRIBUTES = ['_id', 'account_type', 'user_name', 'first_name',
                       'last_name', 'address', 'city', 'state', 'zip_code']

class User():
    '''User class.'''
    def __init__(self, input_dict: dict):
        '''User class default constructor.'''
        _LOG.info('Entering the bank.personnel.User constructor.')
        if input_dict['_id']:
            self._id = input_dict['_id']
        else:
            self._id = uuid4()
        self.account_type = ''
        self.user_name = ''
        self.first_name = ''
        self.last_name = ''
        self.address = ''
        self.city = ''
        self.state = ''
        self.zip_code = ''
        for attr in INSTANCE_ATTRIBUTES:
            self.attr = input_dict[attr]
        if 'loans' in input_dict:
            self.loans = input_dict['loans']
        else:
            self.loans = list()
        _LOG.info('Exiting the bank.personnel.User constructor.')

    def __str__(self):
        '''Constructs a string that represents the user's personally identifiable information.'''
        _LOG.info('Entering the bank.personnel.User.__str__ built-in virtual method override.')
        string = ''
        if self.account_type == 'guest':
            string = 'This user is a guest.'
        else:
            string = self.account_type + ': ' + self.first_name + ' ' + self.last_name + ' alias '
            string += self.user_name + ' is a(n) ' + self.account_type + ' lives at ' + self.address
            string += ' in ' + self.city + ' ' + self.state + ' with zip code: ' + self.zip_code
        _LOG.info('Exiting the bank.personnel.User.__str__ built-in virtual method override.')
        return string

    def __repr__(self):
        '''Returns a string representation of the object.'''
        _LOG.info('Entering the bank.personnel.User.__repr__ built-in virtual method override.')
        _LOG.info('Exiting the bank.personnel.User.__repr__ built-in virtual method override.')
        return self.__str__()

    def to_dict(self):
        '''Returns the dictionary representation of the SecureEntity class.'''
        _LOG.info('Entering the bank.personnel.User.to_dict method.')
        _LOG.info('Exiting the bank.personnel.User.to_dict method.')
        return self.__dict__

    @classmethod
    def from_dict(cls, input_dict: dict):
        '''Creates an instance of the class from a dictionary.'''
        _LOG.info('Entering the bank.personnel.User.from_dict method.')
        user = cls(input_dict)
        _LOG.info('Exiting the bank.personnel.User.from_dict method.')
        return user

    def add_loan(self, loan: Loan):
        '''Adds a loan to the user's account.'''
        self.loans.append(loan)

    def view_loans(self):
        '''Prints the loans in the user's account.'''
        for loan in self.loans:
            print(loan)


class Employee(User):
    '''Employee class inherits from User Class.'''
    def __init__(self, input_dict: dict):
        '''Employee class default constructor.'''
        _LOG.info('Entering bank.personnel.Employee class constructor.')
        super().__init__(input_dict)
        _LOG.info('Exiting bank.personnel.Employee class constructor.')


class Customer(User):
    '''Customer class inherits from User class.'''
    def __init__(self, input_dict: dict):
        _LOG.info('Entering bank.personnel.Customer class constructor.')
        super().__init__(input_dict)
        _LOG.info('Exiting bank.personnel.Customer class constructor.')
