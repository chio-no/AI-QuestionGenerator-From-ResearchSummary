# -*- coding: utf-8 -*-

import datetime
import random
import requests as req
from requests_oauthlib import OAuth1
import deepl
import openai
import requests
import csv
import re
import os


# Deepl APIによる翻訳（日→英）
def TranslateJatoEnbyDeepL(text):
    KEY = "DeepLのAPIキーを設定してください"
    target_text = "EN-US"
    translate = deepl.Translator(KEY)
    result = translate.translate_text(text, target_lang=target_text)
    # EN-US もしくは EN-GBにしろって
    return result


# Deepl APIによる翻訳（英→日）
def TranslateEntoJabyDeepL(text):
    KEY = str(os.getenv("DeepLのAPIキーを設定してください"))
    target_text = "JA"
    translate = deepl.Translator(KEY)
    result = translate.translate_text(text, target_lang=target_text)
    return str(result)


# GPT-3による質問を生成する
# abst→処理対象文字列, user→使用するユーザのID

def DQuestionbyOpenAI(abst, user):
    API_KEY = "Open AIのAPIキーを設定してください"
    openai.api_key = API_KEY

    # OpenAIが提供しているModeration Endpointに入力文章をチェックさせる
    if ModerateCheck(abst) == True:
        return "An inappropriate entry was made. Abort processing. Abort the process."
    else:
        # 英語入力の方が高精度なため、入力文書を日英翻訳にかける
        abst = TranslateJatoEnbyDeepL(abst)

        # プロンプト設定
        prompt = "Abstract of paper: " + "'" + str(
            abst) + "'" + "\n\nGenerate five difficult questions so that the discussion heats up for the paper with the abstract cited:"
        response = openai.Completion.create(
            # パラメータ設定　各パラメータの詳細はhttps://platform.openai.com/docs/api-reference/files にあります
            model="text-davinci-003",
            prompt=prompt,
            temperature=1.0,
            max_tokens=400,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            user=user
        )
        ja_return = TranslateEntoJabyDeepL(response["choices"][0]["text"])

        # OpenAIが提供しているModeration Endpointに出力文章をチェックさせ、問題なければユーザに送信
        if ModerateCheck(response["choices"][0]["text"]) == True:
            return "sorry, please try agein."
        else:

            return ja_return


# Open AIのModeration Endpointを使う処理
def ModerateCheck(text):
    checkModerate = openai.Moderation.create(
        input=text
    )
    return checkModerate["results"][0]["flagged"]


# Slack Botのメッセージ送受信に関する処理
# UserID→使用ユーザのID, channelID→メッセージを送受信するチャンネルのID, inputtext→ユーザからの入力, BOT_TOKEN→ボットレベルトークン
def QSlackInterface(UserID, channelID, inputtext, BOT_TOKEN):
    TOKEN = BOT_TOKEN
    SENT_CHANNEL = channelID
    sent_url = "https://slack.com/api/chat.postMessage"

    # メンション部分とスペースを削除
    inputtext = re.sub('<.*>', '', str(inputtext))
    inputtext = re.sub('(\s|　)', '', str(inputtext))

    full_ai_review = DQuestionbyOpenAI(inputtext, UserID)
    for i in range(5):
        # 「1.1．」のように出力されることがあるので、それを「1.」のようにする処理（なくてもいい）
        check_text = str(i + 1) + '.'
        full_ai_review = re.sub(check_text * 2, check_text, full_ai_review)

    # 出力された質問を送信する
    headers = {"Authorization": "Bearer " + TOKEN}
    data = {
        'channel': SENT_CHANNEL,
        'text': full_ai_review
    }
    r = requests.post(sent_url, headers=headers, data=data)
