#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sunday September 23 2018
@author: FLMBP
"""

import os
import schedule
import time
from configuration.constants import client_id
from configuration.constants import client_secret
from configuration.constants import password_reddit
from configuration.constants import user_agent
from configuration.constants import username_reddit
from configuration.constants import username_gmail
from configuration.constants import password_gmail
from configuration.constants import recipient
from configuration.constants import subject_gmail
from configuration.constants import destination_folder
from configuration.constants import schedule_time
from reddit_download.main import RedditDownloader
from google_upload.main import GoogleUploader
from gmail.main import GoogleMail


def list_all_downloaded_files(folder):
    file_list = []
    for f in os.listdir(folder):
        if not f.startswith('.') or not f.endswith('.part'):
            file_list.append(os.path.join(folder, f))
    return file_list


def clean_folder(folder):
    for f in os.listdir(folder):
        os.remove(f)


def main():
    reddit = RedditDownloader(client_id, client_secret, password_reddit, user_agent, username_reddit)
    reddit.download()

    downloaded_files = list_all_downloaded_files(destination_folder)

    if downloaded_files:
        gdrive = GoogleUploader()
        gdrive.upload(downloaded_files)
        gmail = GoogleMail(username_gmail, password_gmail, recipient, subject_gmail, len(downloaded_files))
        gmail.send_email()
        clean_folder(destination_folder)


schedule.every().day.at(schedule_time).do(main)

while True:
    schedule.run_pending()
    time.sleep(1)

print("****************")
print("***   DONE   ***")
print("****************")
