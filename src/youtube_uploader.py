from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import os
import random
import http.client
import httplib2
import time


class YoutubeUploader:
    def __init__(self) -> None:
        self.credentials = self.create_credentials()

    def create_credentials(self):
        SCOPES = ['https://www.googleapis.com/auth/youtube']
        YOUTUBE_CREDENTIALS_FILE = 'youtube_credentials.json'
        YOUTUBE_TOKEN_FILE = 'youtube_token.json'
        creds = None

        if os.path.exists(YOUTUBE_TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(
                YOUTUBE_TOKEN_FILE, scopes=SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    YOUTUBE_CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)

            with open(YOUTUBE_TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())

        return creds

    def upload_video(self, video_file, title, description, tags):
        print('initializing upload process...')
        youtube = build('youtube', 'v3', credentials=self.credentials)

        metadata = self.create_request_body(title, description, tags)

        insert_request = youtube.videos().insert(
            part=",".join(metadata.keys()),
            body=metadata,
            media_body=MediaFileUpload(
                video_file, chunksize=-1, resumable=True)
        )

        self.resumable_upload(insert_request)

    def resumable_upload(self, insert_request):
        MAX_RETRIES = 10
        RETRIABLE_STATUS_CODES = [500, 502, 503, 504]
        RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, http.client.NotConnected,
                                http.client.IncompleteRead, http.client.ImproperConnectionState,
                                http.client.CannotSendRequest, http.client.CannotSendHeader,
                                http.client.ResponseNotReady, http.client.BadStatusLine)

        response = None
        error = None
        retry = 0
        while response is None:
            try:
                print("Uploading file...")
                status, response = insert_request.next_chunk()
                if response is not None:
                    if 'id' in response:
                        print("Video id '%s' was successfully uploaded." %
                              response['id'])
                    else:
                        exit(
                            "The upload failed with an unexpected response: %s" % response)
            except HttpError as e:
                if e.resp.status in RETRIABLE_STATUS_CODES:
                    error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status,
                                                                         e.content)
                else:
                    raise
            except RETRIABLE_EXCEPTIONS as e:
                error = "A retriable error occurred: %s" % e

            if error is not None:
                print(error)
                retry += 1
                if retry > MAX_RETRIES:
                    exit("No longer attempting to retry.")

                max_sleep = 2 ** retry
                sleep_seconds = random.random() * max_sleep
                print("Sleeping %f seconds and then retrying..." %
                      sleep_seconds)
                time.sleep(sleep_seconds)

    def create_request_body(self, title, description, tags):
        return {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags
            },
            'status': {
                'privacyStatus': 'public',
                'selfDeclaredMadeForKids': False,
            }
        }
