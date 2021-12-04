import os
import logging
import requests
from googleapiclient.discovery import build #pip install google-api-python-client
from google_auth_oauthlib.flow import InstalledAppFlow #pip install google-auth-oauthlib
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import config
import src.utils as utils

TOKEN_NAME = "token1.json" # Don't change
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]
client_secrets_file = "googleAPI.json"

class APIHandler:
    @staticmethod
    def get_yt_playlist_size(playlist_id: str) -> int:
        logging.info("Getting amount of playlist items")
        try:
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

            googleAPI = build('youtube', 'v3', credentials=creds)

            resp = googleAPI.playlistItems().list(part="contentDetails", playlistId=playlist_id).execute()
            return resp["pageInfo"]["totalResults"]
        except AttributeError:
            logging.warning(
                f"No YT_API_KEY provided in config.py -> return playlist_size of 0")
            logging.warning(f"Status Code: 400")
            logging.warning(f"Check if you inserted a correct PlayListID in your metadata_config -> return playlist_size of 0")
            return 0

    @staticmethod
    def get_new_twitch_token() -> str:
        logging.info("Getting new token from server")
        url = "https://id.twitch.tv/oauth2/token"
        payload = {"client_id": config.CLIENT_ID, "client_secret": config.CLIENT_SECRET,
                   "grant_type": "client_credentials"}
        resp = requests.post(url, params=payload, headers={"Client-ID": config.CLIENT_ID})
        if resp.status_code == 200:
            with open("token", "w") as outfile:
                outfile.write(resp.json()["access_token"])
            return resp.json()["access_token"]
        else:
            logging.warning(f"Status Code: {resp.status_code}, {resp.json()}")

    @staticmethod
    def get_twitch_game_id(name: str) -> int:
        url = f"https://api.twitch.tv/helix/games"
        payload = {"name": name}
        resp = requests.get(url, params=payload, headers=utils.get_headers())
        if resp.status_code == 200:
            try:
                return resp.json()["data"][0]["id"]
            except (IndexError, KeyError):
                raise NameError("Game not found. Please provide a valid game name.")
        else:
            logging.warning(f"Status Code: {resp.status_code}, {resp.json()}")
