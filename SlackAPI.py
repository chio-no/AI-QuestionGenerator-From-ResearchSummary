# -*- coding: utf-8 -*-
# GPT-3による質問生成を行うslack bot
from functions import *
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os

# Slack APIのアプリレベルトークンとボットレベルトークンを設定します
bot_token = "BOT_TOKEN"
app_token = "APP_TOKEN"

# ボットトークンとソケットモードハンドラーを使ってアプリを初期化します
Qapp = App(token=bot_token)


# Slack Botにメンションされた時に動作
@Qapp.event("app_mention")
def message_hey(event, say):
    QSlackInterface(event["user"], event["channel"])
    print(event["user"])


# アプリを起動します
if __name__ == "__main__":
    SocketModeHandler(Qapp, app_token).start()
