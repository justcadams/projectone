''' Maps requests to dispatcher '''
import bank.products.handler as products
import bank.personnel.handler as users
_MAP = {
    'loans': products.LoanDispatcher(),
    'users': users.UserDispatcher()
}
_CONTENT = {
    'home': ['static', 'home.html'],
    'login': ['static', 'login.html'],
    'loanlist': ['static', 'loans.html'],
    'mortgages':['static', 'mortgages.html'],
    'carloans': ['static', 'carloans.html'],
    'studentloans': ['static', 'studentloans.html'],
    'personalloans': ['static', 'personalloans.html'],
    'editloan': ['static', 'editloan.html'],
    'edituser': ['static', 'edituser.html']
}

def get_dispatcher(context: str):
    '''This function takes in a string "context" and returns the dispatcher associated with it.'''
    if context in _MAP:
        return _MAP[context]
    else:
        return None

def get_static_location(context: str):
    ''' This function takes in a string "context" and returns the file associated with it.'''
    if context in _CONTENT:
        return _CONTENT[context]
    else:
        return None
