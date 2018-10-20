import wget
import praw
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
        for post in self.save_list:
            if post.url.endswith(('.jpg', '.png', '.jpeg', '.tif', '.tiff', '.bmp')):
                downloaded_post = self.get_image(post.title, post.url, destination_folder)
            else:
                downloaded_post = self.get_video(post.url)
            if not downloaded_post:
                self.r.submission(id=post.id).hide()
                print(post.id + " has been moved to hidden\n")
            self.r.submission(id=post.id).unsave()
            print(post.id + " has been unsaved\n")


    @staticmethod
    def get_image(title, url, directory):
        image = wget.download(url, directory)
        print("\nImage: " + title + " has been downloaded successfully\n")
        return image

    @staticmethod
    def get_video(url):
        return youtube_download(url)
