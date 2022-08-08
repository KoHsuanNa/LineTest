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
from linebot.models import TextSendMessage

from datetime import datetime, date,timezone,timedelta
import time
import re
app = Flask(__name__)

a = 2
dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
dt2 = dt1.astimezone(timezone(timedelta(hours=8)))
timenow = dt2.strftime("%Y-%m-%d %H:%M:%S")
time_2 = '2022-08-08 15:45:00'                                      #設定預計抵達時間
time_1_struct = datetime.strptime(timenow, "%Y-%m-%d %H:%M:%S")     #現在時間
time_2_struct = datetime.strptime(time_2, "%Y-%m-%d %H:%M:%S")      #預計抵達時間
seconds = (time_2_struct - time_1_struct).seconds                   #相差的秒數

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('YzA8hOYnlQrI+qd9xViyd/RdrPTN4B1Y9HZ9Q97mZEcdA0wS9kvJ4flUpMpXjHPJG4Wh+ntbAKUH2VMHU06QTG/dQWoIOZNXsmVX5MlXbBv5MvJUnXZi/xDC3jTVDu318pg+EY9Z4GRKSKBXhtfoRQdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('b42fb349160d45f84b0126873126a340')
# 請填入您的ID
yourID = 'Uad6ef6c5ff973a4fdbce4101732f1be8'


# line_bot_api.push_message('Uad6ef6c5ff973a4fdbce4101732f1be8', TextSendMessage(text='可以開始了'))


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
    if re.match('一分鐘',message):
        #line_bot_api.reply_message(event.reply_token,TextSendMessage('收到！'))
        time.sleep(60)
        line_bot_api.reply_message(event.reply_token,TextSendMessage('一分鐘到了！'))
    elif re.match('5分鐘後提醒我',message):
        time.sleep(300)
        line_bot_api.reply_message(event.reply_token,TextSendMessage('5分鐘到了！'))
    if re.match('設定到站提醒',message):
         flex_message = TextSendMessage(text='請選擇時間',
                                quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label= "2分鐘", text="2分鐘後提醒我"))]))
         line_bot_api.reply_message(event.reply_token, flex_message)
    elif re.match('2分鐘後提醒我',message):
        time.sleep(a*60)
        line_bot_api.reply_message(event.reply_token,TextSendMessage('2分鐘到了！'))
    if re.match('告訴我秘密',message):
         image_carousel_template_message = TemplateSendMessage(
             alt_text='路線',
             template=ImageCarouselTemplate(
                 columns=[
                     ImageCarouselColumn(
                         image_url='https://github.com/KoHsuanNa/LineTest/blob/main/resource/IMG_5568.jpg?raw=true',
                         action=PostbackAction(
                             label='開始設定到站提醒',
                             display_text='到站提醒',
                         ))]))
    elif re.match('到站提醒',message):
        time.sleep(seconds-120)
        line_bot_api.reply_message(event.reply_token,TextSendMessage('2分鐘後即將到站！請準備下車~'))
    
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage('呵呵'))

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)