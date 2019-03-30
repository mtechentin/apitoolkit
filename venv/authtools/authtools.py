from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient, TokenExpiredError


def get_access_token(**kwargs):
    '''
    Retrieve stored token, refresh if expired, store and output updated token

    Parameters
    ----------
    client_id: str
    client_secret: str
    token_url: str
    protected_url: str
        Any API endpoint to test existing access token

    Returns
    -------
    token: str
        Access Token
    '''
    client_id = kwargs['client_id']
    client_secret = kwargs['client_secret']
    token_url = kwargs['token_url']
    protected_url = kwargs['token_url']

    # Retrieve and test old token.  Refresh if non-existent or expired and save updated token.
    try:
        token = retrieve_token()
        client = OAuth2Session(client_id, token=token)
        probe = client.get(protected_url)
    except TokenExpiredError as error:
        token = new_token(client_id, client_secret, token_url)
        save_token(token)
    except ValueError as error:
        token = new_token(client_id, client_secret, token_url)
        save_token(token)

    return token['token']


def save_token(token):
    '''
    Store token

    Parameters
    ----------
    token: dict
    '''
    try:
        file = open('token.py', 'w')
        file.write(token)
        file.close()
    except SaveError as error:
        print(error.message)


def retrieve_token():
    '''
    Retrieve token if present

    Returns
    -------
    token: dict
    '''
    try:
        file = open('token.py', 'r')
        token = file.read()
        file.close()
        return token
    except:
        raise ValueError


def new_token(client_id, client_secret, token_url):
    '''
    Generate and return new token dict

    Parameters
    ----------
    client_id: str
    client_secret: str
    token_url: str

    Returns
    -------
    token: dict
    '''
    try:
        client = BackendApplicationClient(client_id=client_id)
        oauth = OAuth2Session(client=client)
        token = oauth.fetch_token(token_url=token_url, client_id=client_id,
                                  client_secret=client_secret)
    except TokenError as error:
        print(error.message)

    return token


class SaveError(Exception):
    '''Token save exception stub'''
    def __init__(self, message):
        self.message = 'Error. Unable to save token.'


class TokenError(Exception):
    '''Token generation exception stub'''
    def __init__(self, message):
        self.message = 'Error. Unable to generate token'
