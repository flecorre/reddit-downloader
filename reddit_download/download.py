import wget
import praw
import logging
from configuration.constants import destination_folder
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
        logging.info('Iterating through saved posts...')
        for post in self.save_list:
            if post.url.endswith(('.jpg', '.png', '.jpeg', '.tif', '.tiff', '.bmp')):
                is_downloaded = self.get_image(post.url, destination_folder)
            else:
                is_downloaded = self.get_video(post.url)
            if is_downloaded:
                self.r.submission(id=post.id).hide()
                self.r.submission(id=post.id).unsave()
                logging.info(f'{post.title} has been downloaded and moved to hidden posts')
            else:
                logging.warning(f'{post.title} cannot be downloaded')

    @staticmethod
    def get_image(url, directory):
        image = wget.download(url, directory)
        return image

    @staticmethod
    def get_video(url):
        return youtube_download(url)
