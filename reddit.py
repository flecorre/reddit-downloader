#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sunday September 23 2018
@author: FLMBP
"""

import os
import logging.handlers
from configuration import constants
from reddit_download.download import RedditDownloader
from google_upload.upload import GoogleUploader

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def list_files(path):
    logging.info('Main Method - listing files in {}'.format(path))
    return [f for f in os.listdir(path) if not f.startswith('.') and not f.endswith('.part')]


def append_folder_path(folder, list):
    logging.info('Main Method - appending folder path to file list')
    new_list = []
    for element in list:
        logging.info('Main Method - appending {} and {}'.format(folder, element))
        new_list.append(folder + '/' + element)
    return new_list


def clean_folder(folder):
    for f in os.listdir(folder):
        logging.info('Main Method - deleting {}'.format(f))
        os.remove(f)
        logging.info('Main Method - {} deleted'.format(f))


def reddit_download():
    reddit = RedditDownloader(constants.reddit_client_id, constants.reddit_client_secret, constants.reddit_password, constants.reddit_user_agent,
                              constants.reddit_username)
    reddit.download()


def gdrive_upload(downloaded_files):
    gdrive = GoogleUploader()
    gdrive.upload(downloaded_files)


def main():
    logging.info('Main Method - Start')
    reddit_download()
    downloaded_files = list_files(constants.destination_folder)
    if downloaded_files:
        downloaded_files = append_folder_path(constants.destination_folder, downloaded_files)
        gdrive_upload(downloaded_files)
        clean_folder(constants.destination_folder)
    logging.info('Main Method - End')


if __name__ == '__main__':
    main()
