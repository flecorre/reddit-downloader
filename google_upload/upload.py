# -*- coding: utf-8 -*-

import os
import mimetypes
import logging
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from configuration.constants import gdrive_api_credentials
from configuration.constants import gdrive_folder_id


class GoogleUploader:

    DRIVE = None

    def __init__(self):
        SCOPES = 'https://www.googleapis.com/auth/drive'
        store = file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(gdrive_api_credentials, SCOPES)
            creds = tools.run_flow(flow, store)
        self.DRIVE = build('drive', 'v3', http=creds.authorize(Http()))

    def upload(self, files):
        for file in files:
            mimeType = mimetypes.MimeTypes().guess_type(file)[0]
            formattedFilename = file.split("/")[-1]
            metadata = {
                'name': formattedFilename,
                'mimeType': mimeType,
                'parents': [gdrive_folder_id]
            }
            res = self.DRIVE.files().create(body=metadata, media_body=file, fields='id').execute()
            if res:
                logging.info(f'{formattedFilename} has been uploaded')
                os.remove(file)
                logging.info(f'{formattedFilename} has been deleted in local folder')
