# A simple python reddit downloader

#### Register reddit api
- Log in reddit
- Go to preferences
- Click on app tab
- Create an app
- Enter reddit credentials in configuration/constants.py

#### Register google api
- Follow that link: https://developers.google.com/drive/api/v3/quickstart/python
- Enter google api credentials in configuration/credentials.json
- The first time you start the script a token.json will be generated

#### Setup google mail
- Create a dummy email account
- Authorize less secure apps to access your gmail account: https://myaccount.google.com/lesssecureapps
- Enter gmail credentials and recipient in configuration/constants.py

#### Getting started
- pip install praw/youtube-dl/smtplib
- Enter download temporary folder and gdrive folder in configuration/constants.py
- Enjoy