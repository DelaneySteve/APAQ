import io
import os
import os.path
import pickle

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/drive.file']
MODEL_FOLDER_ID = '1zsMUAaFUNvZpNGA-6yvUTHKyZCS49Za6'

def pull_model(**kwargs: str | None) -> bytes:
    download_file_id = kwargs.get('download_file_id')
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
    except HttpError as error:
        print(f' An error occurred trying to connect: {error}')

    # get all files in model drive folder
    results = (
        service.files()
        .list(q = f'"{MODEL_FOLDER_ID}" in parents',
            fields='nextPageToken, files(id, name, createdTime)')
        .execute()
    )

    # if file_id wasnt given find ID for the latest (maximum) uploaded model
    if download_file_id is None:
        times = [item['createdTime'] for item in results.get('files', [])]
        response_latest_time  = (
            service.files()
            .list(q = f'createdTime = "{max(times)}"',
                fields = 'nextPageToken, files(id, name)')
            .execute()
        )
        download_file_id = response_latest_time.get('files')[0].get('id')

    # download the file
    # pylint: disable=maybe-no-member
    request = service.files().get_media(fileId=download_file_id)

    with io.BytesIO() as file:
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(f'Download {int(status.progress() * 100)}.')

        file.seek(0)
        model = pickle.load(file)
        return model
