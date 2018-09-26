#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sunday September 23 2018
@author: FLMBP
"""

import praw
from configuration.config import client_id
from configuration.config import client_secret
from configuration.config import password
from configuration.config import user_agent
from configuration.config import username
from file_download.main import download_reddit_post


def unsave(postList, reddit):
    for post in postList:
        reddit.submission(id=post).unsave()


r = praw.Reddit(client_id=client_id,
                client_secret=client_secret,
                password=password,
                user_agent=user_agent,
                username=username)

save_list = r.user.me().saved(limit=None)
downloaded_list = []


download_reddit_post(save_list, downloaded_list)

print ("\n")
print('**** DONE ****')
print ("\n")
