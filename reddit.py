#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sunday September 23 2018
@author: FLMBP
"""

import os
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
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def list_all_downloaded_files(folder):
        filelist = os.listdir(folder)
        return [x for x in filelist
                if not (x.startswith('.') or not (x.endswith('.part')))]


def clean_folder(folder):
    for f in os.listdir(folder):
        os.remove(f)

def fetch_reddit():
        reddit = RedditDownloader(reddit_client_id, reddit_client_secret, reddit_password, reddit_user_agent, reddit_username)
        reddit.download()


def upload_gdrive(downloaded_files):
        gdrive = GoogleUploader()
        gdrive.upload(downloaded_files)
        clean_folder(destination_folder)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def start(bot, update):
        bot.send_message(telegram_chatid, text='...starting to fetch')  
        fetch_reddit()
        downloaded_files = list_all_downloaded_files(destination_folder)
        if downloaded_files:
                sentence = "%s files fetched" % (len(downloaded_files))
                bot.send_message(telegram_chatid, text=sentence)
                upload_gdrive(downloaded_files)
                bot.send_message(telegram_chatid, text='...all done!')
        else:
                bot.send_message(telegram_chatid, text='...nothing found')


def main():
    print('Reddit bot starting...')
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
