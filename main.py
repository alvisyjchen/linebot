#!venv/bin/python

# 載入需要的模組
import os
import sys
from argparse import ArgumentParser
from flask import Flask, request, abort
from flask.logging import create_logger
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
import configparser
import psycopg2
import def_add_profile
import count_tdee

# 設定應用程式
app = Flask(__name__)
LOG = create_logger(app)
config = configparser.ConfigParser()
config.read('config.ini')

# 認證
line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))

# 根路由，測試用
@ app.route("/")
def hello():
    return "hello world"

# callback路由，和line連線
@ app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    LOG.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("400 error")
        abort(400)
    return "OK"

# 文字訊息事件
@ handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    # 定義常用變數
    text = event.message.text
    user_id = event.source.user_id

    # 開啟資料庫連線
    DATABASE_URL = os.environ['heroku config:get DATABASE_URL -a alvislinebot']
    conn = psycopg2.connect(DATABASE_URL, sslmode="require")

    # 首先要在登錄 tdee 時就 insert userid 到 activities 表，就不用每次判斷 activities 表裡面有沒有這個 user
    print("user_id:", user_id)
    cursor = conn.cursor()
    SQL_order = f'''
    select status from userinfo where userid = '{user_id}'
    '''
    cursor.execute(SQL_order)
    status = cursor.fetchone()[0]
    print(f"SQL搜尋成功，user的狀態: {status}")
    cursor.close()

    # 開始使用
    if user_id is None:
        line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text="請輸入[開始使用]"))

    elif text == "[開始使用]":
        def_add_profile.prfile_record(line_bot_api, conn, event, user_id, text, status)

    elif status == "記錄個人資料":
        def_add_profile.add_gender(line_bot_api, conn, event, user_id, text, status)
    
    elif status == "記錄性別":
        def_add_profile.add_high(line_bot_api, conn, event, user_id, text, status)

    elif status == "記錄身高":
        def_add_profile.add_weight(line_bot_api, conn, event, user_id, text, status)
    
    elif status == "記錄體重":
        def_add_profile.add_age(line_bot_api, conn, event, user_id, text, status)

    elif status == "記錄年齡":
        def_add_profile.add_activity(line_bot_api, conn, event, user_id, text, status)

    elif status == "記錄活動量":
        count_tdee.count_tdee(line_bot_api, conn, event, user_id, text, status)

if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage="Usage: python " + __file__ + " [--port <port>] [--help]"
    )
    arg_parser.add_argument("-p", "--port", default=5000, help="port")
    arg_parser.add_argument("-d", "--debug", default=False, help="debug")
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)