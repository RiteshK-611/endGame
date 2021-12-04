import os
import shutil
import time
import datetime
from googleapiclient.discovery import build #pip install google-api-python-client
from google_auth_oauthlib.flow import InstalledAppFlow #pip install google-auth-oauthlib
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload
from src.utils import get_valid_game_name

TOKEN_NAME = "token2.json" # Don't change
SCOPES = ['https://www.googleapis.com/auth/drive']
client_secrets_file = 'googleAPI.json'
today = datetime.date.today()


def DriveUploader(game: str):
    game_name = get_valid_game_name(game)
    media_path = f"TwitchClips/media/{game_name}/{str(today)}/compilation/"

    print("Handling GoogleAPI")
    creds = None

    if os.path.exists(TOKEN_NAME):
        creds = Credentials.from_authorized_user_file(TOKEN_NAME, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
            creds = flow.run_console()
        # Save the credentials for the next run
        with open(TOKEN_NAME, 'w') as token:
            token.write(creds.to_json())

    googleAPI = build('drive', 'v3', credentials=creds)

    try:
        # delete folder from drive
        folder = open('folder_id.txt', 'r+')
        id = folder.read()
        googleAPI.files().delete(fileId=id).execute()


        # erase all data from file
        folder.seek(0)
        folder.truncate()
        folder.close()
    except:
        pass


    # create folder in drive
    name = game_name.capitalize() + " [" + str(today) + "]"
    file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    file = googleAPI.files().create(body=file_metadata, fields='id').execute()
    # print('Folder ID: %s' % file.get('id'))
    folder_id = file.get('id')


    # inserting files in folder
    for file in os.listdir(media_path):
        print(f"\n{file}")
        file_metadata = {
            'name': file,
            'parents': [folder_id]
        }
        file_path = media_path + file
        media = MediaFileUpload(file_path, resumable=True)
        file = googleAPI.files().create(body=file_metadata, media_body=media, fields='id').execute()
        # print("\nDone...........")
        # print('File ID: %s' % file.get('id'))


    # write folder id in file
    folder = open('folder_id.txt', 'w')
    folder.write(folder_id)
    folder.close()

    return "Uploaded to your Drive!"