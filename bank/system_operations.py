'''System operations file handles website automation and secure data handling.'''

# Built-in imports
import base64
from getpass import getpass, getuser

#Third-party imports
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from decouple import config

# Custom imports
from bank.data.logger import get_logger


LOG = get_logger(__name__)
BLOCK_SIZE = config('BLOCK_SIZE', cast=int)
COUNT = config('COUNT', cast=int)
SALT = config('SALT')

def pad(s_st):
    '''Pads the string before encrypting.'''
    LOG.info('Entering dealership.data.pad')
    LOG.info('Exiting dealearship.data.pad')
    return s_st + (BLOCK_SIZE - len(s_st) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s_st) % BLOCK_SIZE)

def unpad(long_string):
    '''Removes string padding after decrypting.'''
    LOG.info('Entering dealership.data.unpad')
    LOG.info('Exiting dealearship.data.unpad')
    return long_string[:-ord(long_string[len(long_string)-1:])]

def encrypt_env_var(env_var, password=''):
    '''Requires an admin password to encrypt environment variables.'''
    LOG.info('Entering dealership.data.encrypt_data')
    var_text = pad(config(env_var))
    plain_text = var_text.encode("utf8")
    cipher_text = ''
    if not password:
        pii_password = getpass('Administrator Password: ')
        pii_confirm = getpass('Confirm Password: ')
        if pii_password == pii_confirm:
            cipher_text = encrypt_env_var_helper(plain_text, pii_password)
        else:
            print('The passwords provided do not match.')
            LOG.info('The passwords provided do not match.')
    else:
        cipher_text = encrypt_env_var_helper(env_var, password)
    LOG.info('Exiting dealership.data.encrypt_data')
    return cipher_text

def encrypt_value(value, password=''):
    '''Requires an admin password to encrypt environment variables.'''
    LOG.info('Entering dealership.data.encrypt_data')
    var_text = pad(value)
    plain_text = var_text.encode("utf8")
    cipher_text = ''
    if not password:
        pii_password = getpass('Administrator Password: ')
        pii_confirm = getpass('Confirm Password: ')
        if pii_password == pii_confirm:
            cipher_text = encrypt_env_var_helper(plain_text, pii_password)
        else:
            print('The passwords provided do not match.')
            LOG.info('The passwords provided do not match.')
    else:
        cipher_text = encrypt_env_var_helper(plain_text, password)
    LOG.info('Exiting dealership.data.encrypt_data')
    return cipher_text

def encrypt_env_var_helper(plain_text, password=''):
    '''Encrypts the specified environment variable.'''
    initialization_vector = get_random_bytes(BLOCK_SIZE)
    key = PBKDF2(password, SALT, BLOCK_SIZE, count=COUNT,
                 hmac_hash_module=SHA256)
    cipher = AES.new(key, AES.MODE_CBC, initialization_vector)
    return base64.b64encode(initialization_vector + cipher.encrypt(plain_text))

def decrypt_env_var(env_var, password=''):
    '''Decrypts the specified environment variable.'''
    LOG.info('Entering dealership.data.decrypt_data')
    cipher_text = base64.b64decode(config(env_var))
    plain_text = ''
    if not password:
        pii_password = getpass('Administrator Password: ')
        pii_confirm = getpass('Confirm Password: ')
        if pii_password == pii_confirm:
            plain_text = decrypt_env_var_helper(cipher_text, pii_password)
        else:
            LOG.info('Passwords do not match.')
            print('The passwords provided do not match.')
    else:
        plain_text = decrypt_env_var_helper(cipher_text, password)
    LOG.info('Exiting dealership.data.decrypt_env_var')
    return plain_text.encode("utf8")

def decrypt_env_var_helper(cipher_text, password=''):
    '''Requires an admin password to decrypt environment variables.'''
    LOG.info('Entering dealership.data.decrypt_env_var_helper.')
    key = PBKDF2(password, SALT, BLOCK_SIZE, count=COUNT, hmac_hash_module=SHA256)
    initialization_vector = cipher_text[:BLOCK_SIZE]
    cipher = AES.new(key, AES.MODE_CBC, initialization_vector)
    LOG.info('Exiting dealership.data.decrypt_env_var_helper.')
    return unpad(cipher.decrypt(cipher_text[BLOCK_SIZE:])).decode('utf-8')

def username_prompt():
    '''Password prompt for the login method.'''
    LOG.info('Entering the dealerhsip.data.MongoServer.password_prompt method.')
    LOG.info('Exiting the dealerhsip.data.MongoServer.password_prompt method.')
    return getuser()

def password_prompt():
    '''Password prompt for the login method.'''
    LOG.info('Entering the dealerhsip.data.MongoServer.password_prompt method.')
    LOG.info('Exiting the dealerhsip.data.MongoServer.password_prompt method.')
    return getpass('Password: ')
