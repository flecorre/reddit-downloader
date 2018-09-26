#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sunday September 23 2018
@author: FLMBP
"""

import os
import praw
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

r = praw.Reddit(client_id=client_id,
                client_secret=client_secret,
                password=password_reddit,
                user_agent=user_agent,
                username=username_reddit)


def list_all_downloaded_files(folder):
    file_list = []
    for file in os.listdir(folder):
        file_list.append(os.path.join(folder, file))
    return file_list


def main():
    reddit = RedditDownloader(client_id, client_secret, password_reddit, user_agent, username_reddit)
    reddit.download()

    downloaded_files = list_all_downloaded_files(destination_folder)

    gdrive = GoogleUploader()
    gdrive.upload(downloaded_files)

    gmail = GoogleMail(username_gmail, password_gmail, recipient, subject_gmail, len(downloaded_files))
    gmail.send_email()


schedule.every().day.at(schedule_time).do(main)

while True:
    schedule.run_pending()
    time.sleep(1)

print "****************"
print "***   DONE   ***"
print "****************"
