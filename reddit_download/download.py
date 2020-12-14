import wget
import praw
import logging
from configuration import constants
from reddit_download.youtube import youtube_download


class RedditDownloader:
    save_list = []
    r = None

    def __init__(self, client_id, client_secret, password, user_agent, username):
        self.r = praw.Reddit(client_id=client_id,
                             client_secret=client_secret,
                             password=password,
                             user_agent=user_agent,
                             username=username)
        self.save_list = self.r.user.me().saved(limit=None)

    def download(self):
        logging.info('RedditDownloader.download - Start')
        is_save_list_empty = True
        for post in self.save_list:
            if is_save_list_empty:
                is_save_list_empty = False
            is_downloaded = False
            if hasattr(post, 'url') and post.url.endswith(('.jpg', '.png', '.jpeg', '.tif', '.tiff', '.bmp')):
                logging.info('RedditDownloader.download - {} is an image'.format(post.title))
                is_downloaded = self.get_image(post.url, constants.destination_folder)
            elif hasattr(post, 'url'):
                logging.info('RedditDownloader.download - {} is a video'.format(post.title))
                is_downloaded = self.get_video(post.url)
            if is_downloaded:
                self.clean_reddit_post(post)
            else:
                logging.warning('RedditDownloader.download - {} cannot be downloaded'.format(post))
        if is_save_list_empty:
            logging.info('RedditDownloader.download - Nothing found')
        logging.info('RedditDownloader.download - End')
    
    def clean_reddit_post(self, post):
        logging.info('RedditDownloader.download - {} downloaded'.format(post.title))
        self.r.submission(id=post.id).hide()
        logging.info('RedditDownloader.download - {} moved to hidden posts'.format(post.title))
        self.r.submission(id=post.id).unsave()
        logging.info('RedditDownloader.download - {} unsaved'.format(post.title))

    @staticmethod
    def get_image(url, directory):
        return wget.download(url, directory)

    @staticmethod
    def get_video(url):
        return youtube_download(url)
