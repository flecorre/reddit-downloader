#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sunday September 23 2018
@author: FLMBP
"""

import os
import logging.handlers
from configuration.constants import reddit_client_id
from configuration.constants import reddit_client_secret
from configuration.constants import reddit_password
from configuration.constants import reddit_user_agent
from configuration.constants import reddit_username
from configuration.constants import destination_folder
from configuration.constants import telegram_token
from configuration.constants import telegram_chatid
from reddit_download.download import RedditDownloader
from google_upload.upload import GoogleUploader
from telegram.ext import Updater, CommandHandler

formatter = logging.Formatter(logging.BASIC_FORMAT)
handler = logging.FileHandler("./reddit.log", mode="w", encoding='UTF-8', delay=False)
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def list_files(path):
    return [f for f in os.listdir(path) if not f.startswith('.') and not f.endswith('.part')]


def append_folder_path(folder, list):
    new_list = []
    for element in list:
        new_list.append(folder + '/' + element)
    return new_list


def clean_folder(folder):
    for f in os.listdir(folder):
        if not f.startswith('.'):
            os.remove(f)


def fetch_reddit():
    reddit = RedditDownloader(reddit_client_id, reddit_client_secret, reddit_password, reddit_user_agent,
                              reddit_username)
    reddit.download()


def upload_gdrive(downloaded_files):
    gdrive = GoogleUploader()
    gdrive.upload(downloaded_files)
    clean_folder(destination_folder)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def start(bot, update):
    bot.send_message(telegram_chatid, text='...starting to fetch')
    fetch_reddit()
    downloaded_files_relative_path = list_files(destination_folder)
    if downloaded_files_relative_path:
        downloaded_files_abs_path = append_folder_path(destination_folder, downloaded_files_relative_path)
        sentence = "%s files fetched" % (len(downloaded_files_abs_path))
        bot.send_message(telegram_chatid, text=sentence)
        upload_gdrive(downloaded_files_abs_path)
        bot.send_message(telegram_chatid, text='...all done!')
    else:
        bot.send_message(telegram_chatid, text='...nothing found')


def main():
    logger.info('Reddit bot is starting...')
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(telegram_token)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    # log all errors
    dp.add_error_handler(error)
    # Start the Bot
    updater.start_polling()
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
