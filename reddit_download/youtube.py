import youtube_dl
from configuration.constants import destination_folder


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)


success = False


def my_hook(d):
    global success
    if d['status'] == 'finished':
        print('\nVideo: ' + d['filename'] + " has been downloaded!\n")
        success = True
    if d['status'] == 'downloading':
        print(d['filename'], d['_percent_str'], d['_eta_str'])


ytdl_opts = {
    'logger': MyLogger(),
    'outtmpl': destination_folder + '/%(title)s.%(ext)s',
    'progress_hooks': [my_hook],
    'ignoreerrors': 'True'
}


def youtube_download(url):
    global success
    with youtube_dl.YoutubeDL(ytdl_opts) as ytdl:
        ytdl.download([url])
        download_status = success
        reset_success_value()
        return download_status


def reset_success_value():
    global success
    success = False
