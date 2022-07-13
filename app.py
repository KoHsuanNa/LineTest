# -*- coding: utf-8 -*-

"""
Created on Wed Jun  2 21:16:35 2021
@author: Ivan
版權屬於「行銷搬進大程式」若有疑問可聯絡ivanyang0606@gmail.com

Line Bot聊天機器人
第一章 Line Bot申請與串接
Line Bot機器人串接與測試
"""
#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

from linebot.models import TextSendMessage
import time
# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('YzA8hOYnlQrI+qd9xViyd/RdrPTN4B1Y9HZ9Q97mZEcdA0wS9kvJ4flUpMpXjHPJG4Wh+ntbAKUH2VMHU06QTG/dQWoIOZNXsmVX5MlXbBv5MvJUnXZi/xDC3jTVDu318pg+EY9Z4GRKSKBXhtfoRQdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('b42fb349160d45f84b0126873126a340')
# 請填入您的ID
yourID = 'Uad6ef6c5ff973a4fdbce4101732f1be8'


# line_bot_api.push_message('Uad6ef6c5ff973a4fdbce4101732f1be8', TextSendMessage(text='你可以開始了'))


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

 
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

 
#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = text=event.message.text
    if re.match('1分鐘後提醒我',message):
        line_bot_api.reply_message(event.reply_token,TextSendMessage('收到！'))
        time.sleep(60)
        line_bot_api.reply_message(event.reply_token,TextSendMessage('1分鐘到了！'))
        
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)