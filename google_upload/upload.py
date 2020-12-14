# -*- coding: utf-8 -*-

import os
import mimetypes
import logging
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from configuration import constants


class GoogleUploader:

    DRIVE = None

    def __init__(self):
        SCOPES = 'https://www.googleapis.com/auth/drive'
        store = file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(constants.gdrive_api_credentials, SCOPES)
            creds = tools.run_flow(flow, store)
        self.DRIVE = build('drive', 'v3', http=creds.authorize(Http()))

    def upload(self, files):
        logging.info('GoogleUploader.upload - Start')
        for file in files:
            mimeType = mimetypes.MimeTypes().guess_type(file)[0]
            formattedFilename = file.split("/")[-1]
            logging.info('GoogleUploader.upload - Uploading {}'.format(formattedFilename))
            metadata = {
                'name': formattedFilename,
                'mimeType': mimeType,
                'parents': [constants.gdrive_folder_id]
            }
            res = self.DRIVE.files().create(body=metadata, media_body=file, fields='id').execute()
            if res:
                logging.info('GoogleUploader.upload - {} has been uploaded'.format(formattedFilename))
                os.remove(file)
                logging.info('GoogleUploader.upload - {} has been deleted in local folder'.format(formattedFilename))
        logging.info('GoogleUploader.upload - End')
