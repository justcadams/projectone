''' A handler for Media operations in our server '''
# External Modules
import json
import urllib.parse
# Internal Modules
import bank.web.dispatch as dispatch
from bank.products.loan import ProductEncoder, Loan, Mortgage, CarLoan, PersonalLoan, StudentLoan
from bank.data.logger import get_logger
from loan_approval_system import _SERVER

_LOG = get_logger(__name__)

class AbstractDispatcher(dispatch.Dispatcher):
    ''' Abstract class for handling requests'''
    def dispatch(self, web_path: list, method, r_body=None):
        ''' Takes in path and rfile and returns status code and body as tuple'''
        if method == 'GET':
            return self.get_operations(web_path)
        if method == 'POST':
            return self.post_operations(web_path, r_body)
        if method == 'PUT':
            return self.put_operations(web_path, r_body)
        if method == 'DELETE':
            return self.delete_operations(web_path, r_body)
    def put_operations(self, web_path: list, r_body):
        ''' Abstract bank.web.handler.AbstractDispatcher.put_opertions method.'''

    def get_operations(self, web_path: list):
        ''' Abstract bank.web.handler.AbstractDispatcher.get_opertions method.'''

    def delete_operations(self, web_path: list, r_body):
        ''' Abstract bank.web.handler.AbstractDispatcher.delete_opertions method.'''

    def post_operations(self, web_path: list, r_body):
        ''' Abstract bank.web.handler.AbstractDispatcher.post_opertions method.'''

    def convert_loan(self, product):
        if product.product_type == 'Loan':
            loan = Loan().from_dict(product.to_dict())
            return loan
        if product.product_type == 'Mortgage':
            loan = Mortgage().from_dict(product.to_dict())
            return loan
        if product.product_type == 'Car Loan':
            loan = CarLoan().from_dict(product.to_dict())
            return loan
        if product.product_type == 'Personal Loan':
            loan = PersonalLoan().from_dict(product.to_dict())
            return loan
        if product.product_type == 'Student Loan':
            loan = StudentLoan().from_dict(product.to_dict())
            return loan

    def init_loan(self, r_body):
        loan = Loan.from_dict(json.loads(r_body))
        converted_loan = self.convert_loan(loan)
        return converted_loan

class UserDispatcher(AbstractDispatcher):
    ''' Custom Dispatcher for Users '''
    def dispatch(self, web_path: list, method, r_body=None):
        '''dispatch takes in path and request body
           returns status code and responee body as tuple '''
        _LOG.debug(r_body)
        if len(web_path) == 1 and method == 'POST':
            _LOG.debug(r_body.decode('utf-8').split('='))
            user = _SERVER.login(r_body.decode('utf-8').split('=')[1])
            value = bytes(json.dumps(user, cls=UserEncoder), 'utf-8')
            return (200, value, 'json')
        else:
            return (401, b'Unauthorized')

class ProductDispatcher(AbstractDispatcher):
    ''' Custom Dispatcher for Products '''
    def put_operations(self, path: list, r_body):
        _LOG.debug('Put received on product dispatcher')
        if len(path) == 2:
            # Update a product: PUT to /loan/:id
            b_id = int(path[1])
            loan = Loan.from_dict(json.loads(r_body))
            if loan._id != b_id:
                return (400, b'Bad request')
            _SERVER.update_book(loan)
            return (200, bytes(json.dumps(loan, cls=ProductEncoder), 'utf-8'))
        else:
            return (405, b'Method not allowed')
    def post_operations(self, path: list, r_body):
        _LOG.debug('POST request recieved')
        if len(path) == 1:
            loan = Loan.from_dict(json.loads(r_body))
            _SERVER.insert_media(loan)
            return (201, bytes(json.dumps(book, cls=ProductEncoder), 'utf-8'))
        elif len(path) == 3 and path[2] == 'borrower':
            b_id = int(path[1])
            borrower = User().from_dict(json.loads(r_body))
            book = _SERVER.get_loan_by_id(b_id)
            if book is None or not isinstance(borrower, User):
                return (400, b'Bad request')
            _SERVER.checkout_media(book, borrower)
            return (201, bytes(json.dumps(book, cls=ProductEncoder), 'utf-8'))
        else:
            return (405, b'Method not allowed')
    def delete_operations(self, path: list, r_body):
        _LOG.debug('Delete received on book dispatcher')
        if len(path) == 2:
            b_id = int(path[1])
            self.convert_loan(r_body)
            if converted_loan._id != b_id:
                return (400, b'Bad request')
            _SERVER.remove_loan(converted_loan)
            return (204, b'')
        elif len(path) == 3:
            self.convert_loan(r_body)
            if book._id != int(path[1]) and 'borrower' == path[2]:
                return (400, b'Bad request')
            _SERVER.checkin_media(book)
            return (200, bytes(json.dumps(book, cls=ProductEncoder), 'utf-8'))
        else:
            return (405, b'Method not allowed')
    def get_operations(self, path: list):
        _LOG.debug('GET received on book dispatcher')
        if len(path) == 1:
            # Room 3: See all books: GET to /books
            loans_list = _SERVER.get_loans()
            return (200, bytes(json.dumps(loans_list, cls=ProductEncoder), 'utf-8'))
        # Find by title: GET to /books/search?title=:title
        # Find by author: GET to /books/search?author=:author
        elif len(path) == 2:
            query = path[1].split('?', maxsplit=1)
            if len(query) == 1:
                # GET by id: /loans/:id
                book = _SERVER.get_loan_by_id(int(query[0]))
                return (200, bytes(json.dumps(book, cls=ProductEncoder), 'utf-8'))
            _LOG.debug(query)
            query = query[1].split('=', maxsplit=1)
            search_str = urllib.parse.unquote(query[1])
            book = None
            if query[0] == 'title':
                book = _SERVER.get_book_by_title(search_str)
                if book:
                    return (200, bytes(json.dumps(book, cls=ProductEncoder), 'utf-8'), 'json')
                return (404, b'Book not found')
            if query[0] == 'author':
                pass
            return (400, b'Bad Request')
        return (405, b'Method not allowed')
