import os.path
from pathlib import Path
from typing import Union
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# [*] If modifying the scopes after first run, delete the file token.json!
# [*] Default is set to readonly to prevent potential disaster... only change if you fully understand what you are doing!

# Read all resources and their metadata - no write operations.
#SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Full access to the account's mailboxes, including permanent deletion of threads and messages.
SCOPES = ['https://mail.google.com/']


def get_credentials(credentials: Union[Path, str] = None, token: Union[Path, str] = None) -> Credentials:
    """Gets valid user credentials.

    If there is no token.json, or if token.json is invalid, the OAuth2 flow is completed to obtain new credentials. Must provide credentials.json!

    Args:
        credentials: file path to 'credentials.json' (required for first run)
        token: file path to 'token.json'

    Returns:
        Credentials, the obtained credential
    """
    creds = None
    if token and os.path.exists(token):
        creds = Credentials.from_authorized_user_file(token, SCOPES)
    # if there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            try:
                flow = InstalledAppFlow.from_client_secrets_file(credentials, SCOPES)
                creds = flow.run_local_server(port=0)
            except TypeError:
                raise "[*] You must provide credentials.json as client_secrets_file!"
        # save the credentials for the next run
        if not token:
            with open('token.json', 'w') as t:
                t.write(creds.to_json())
        else:
            with open(token, 'w') as t:
                t.write(creds.to_json())

    return creds


class GoogleClient:
    def __init__(self, credentials_filepath: Union[Path, str] = None, token_filepath: Union[Path, str] = None):
        """
        Constructor for GoogleClient object which calls Gmail API.

        Args:
            credentials_filepath: file path to 'credentials.json' (required for first run)
            token_filepath: file path to 'token.json'
        """
        self.credentials = get_credentials(credentials_filepath, token_filepath)
        self.service = build("gmail", "v1", credentials=self.credentials)
