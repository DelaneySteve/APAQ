# pylint: disable=import-error

import logging
import os
import os.path

from google.auth.transport.requests import Request  # type: ignore
from google.oauth2.credentials import Credentials  # type: ignore
from google_auth_oauthlib.flow import InstalledAppFlow  # type: ignore
from googleapiclient.discovery import build  # type: ignore
from googleapiclient.errors import HttpError  # type: ignore
from googleapiclient.http import MediaFileUpload  # type: ignore

logging.basicConfig(level=logging.INFO)

SCOPES = ['https://www.googleapis.com/auth/drive.file']
MODEL_FOLDER_ID = '1zsMUAaFUNvZpNGA-6yvUTHKyZCS49Za6'


def upload_multipart_model(filename: str, filepath: str) -> str:
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES
            )
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token: # pylint: disable=unspecified-encoding
                token.write(creds.to_json())
    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)
        file_metadata = {'name': filename,  'parents': [MODEL_FOLDER_ID]}
        media = MediaFileUpload(filepath, mimetype='model/pickle')
        file = service.files().create(body=file_metadata, media_body=media).execute()
        logging.info(' File uploaded to Google Drive uploaded_models folder under ID: %s.', file.get('id'))

        media = None

    except HttpError as error:
        print(f' An error occurred trying to upload: {error}')
        file = None

    # now remove the file from the local repo
    try:
        os.remove(filepath)
        logging.info(' File: "%s" deleted.', filepath)
    except PermissionError as err:
        logging.error(' Failed to delete local file. Looks like a permission error: %s', err)
    except OSError as err:
        logging.warning(' Failed to delete local file: OS error occurred: %s', err)

    return file.get('id')
