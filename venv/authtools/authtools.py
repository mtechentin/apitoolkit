from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient, TokenExpiredError


def get_access_token(**kwargs):
    '''
    Retrieve stored token, refresh if expired, store and output updated token

    Kwargs:
        client_id: str
        client_secret: str
        token_url: str
        protected_url: str
            Any API endpoint to test existing access token

    Returns:
        token: str
            Access Token

    Notes:
        The 'Bearer ' prefix is omitted from the Access Token and must be
            added post-function-call
        No support for refresh tokens yet.  Stay tuned.
        Error Handling needs work.  I don't think print statements work in Power BI
            without an open console.  Those custom exceptions are really intended to
            get built out to handle some failure modes, tbd.
    '''
    client_id = kwargs['client_id']
    client_secret = kwargs['client_secret']
    token_url = kwargs['token_url']
    protected_url = kwargs['token_url']

    # Retrieve and test old token.  Return if valid.
    try:
        token = retrieve_token()
        client = OAuth2Session(client_id, token=token)
        probe = client.get(protected_url)
    except TokenExpiredError as error:
        print(e)
    except RetrieveError as error:
        print(e)
    finally:
        return token['token']
    # Generate and store new token
    try:
        token = new_token(token_url, client_id, client_secret)
        save_token(token)
    except TokenError as e:
        print('Token Error: ' + e)
    except SaveError as e:
        print(e)
    finally:
        return token['token']


def save_token(token):
    '''
    Store token

    Args:
        token: dict
    Yields:
        file token.py, containing token dict
    '''
    try:
        file = open('token.py', 'w')
        file.write(token)
        file.close()
    except:
        raise SaveError


def retrieve_token():
    '''
    Retrieve token if present

    Returns:
    token: dict
    '''
    try:
        file = open('token.py', 'r')
        token = file.read()
        file.close()
        return token
    except:
        raise RetrieveError


def new_token(token_url, client_id, client_secret):
    '''
    Generate and return new token dict

    Args:
        token_url: str
        client_id: str
        client_secret: str

    Returns:
        token: dict
    '''
    try:
        client = BackendApplicationClient(client_id=client_id)
        oauth = OAuth2Session(client=client)
        token = oauth.fetch_token(token_url=token_url, client_id=client_id,
                                  client_secret=client_secret)
        save_token(token)
    except SaveError as e:
        raise TokenError(e)

    return token


class Error(Exception):
    '''Base class for Custom Exceptions'''
    pass


class RetrieveError(Error):
    '''Raised when token retrieval fails; triggers new token request'''
    def __init__(self, message):
        self.value = 'Error. Unable to retrieve token'


class SaveError(Error):
    '''Raised on Save Failure'''
    def __init__(self, message):
        self.message = 'Error. Unable to save token.'


class TokenError(Error):
    '''Raised on failure to generate new token'''
    def __init__(self, message):
        self.message = message
