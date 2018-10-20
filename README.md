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

#### Setup telegram api
- Install telegram app on your smartphone
- Open a chatroom with the telegram BotFather and get your Telegram token by typing:
```shell
/newbot
```
- Start a conversation with the bot typing:
```shell
/start
test
```
then follow this link to get your chat id:
```shell
https://stackoverflow.com/questions/32423837/telegram-bot-how-to-get-a-group-chat-id
```

#### Getting started
- pip install -r requirements.txt
- Enter all the previous credentials and other stuff in configuration/constants.py
- Enjoy
