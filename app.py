# -*- coding: utf-8 -*-
#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
from linebot.models import TextSendMessage

from linebot.exceptions import LineBotApiError

from datetime import datetime, date,timezone,timedelta
import time
import re

from DB import *
app = Flask(__name__)

a = 2
dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
dt2 = dt1.astimezone(timezone(timedelta(hours=8)))
timenow = dt2.strftime("%Y-%m-%d %H:%M:%S")
time_2 = '2022-08-15 17:20:00'                                      #設定預計抵達時間
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
    if re.match('開始設定到站提醒',message):
         image_carousel_template_message = TemplateSendMessage(
             alt_text='路線1',
             template=ImageCarouselTemplate(
                 columns=[
                     ImageCarouselColumn(
                         image_url='https://raw.githubusercontent.com/KoHsuanNa/LineTest/main/resource/IMG_5568.jpg',
                         action=PostbackTemplateAction(
                             label='開始設定到站提醒',
                             text='提醒我',
                             #data='action=提醒測試'
                         ))]))
         line_bot_api.reply_message(event.reply_token, image_carousel_template_message)
    if re.match('欸欸提醒我',message):
        #time.sleep(seconds-120)
        line_bot_api.reply_message(event.reply_token,TextSendMessage('不要'))
    
    if re.match('使用者',message):
        user_id = event.source.user_id
        line_bot_api.reply_message(event.reply_token,[TextSendMessage('你的user id是：'),TextSendMessage(user_id)])
    if re.match('是誰',message):
        content = "{}: {}".format("我是", event.source.user_id)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
    if re.match('使用說明',message):
        line_bot_api.reply_message(event.reply_token,TextSendMessage('基本上以圖文選單操作  \n*輸入：一分鐘-->1分鐘後回傳：一分鐘到了！  \n*輸入：5分鐘後提醒我-->5分鐘後回傳：5分鐘到了！  \n*輸入：設定到站提醒-->出現2分鐘選項-->按下會自動發送2分鐘後提醒我-->2分鐘後回傳：2分鐘到了！  \n*輸入：使用者 -->回傳：userid'))
        
    if re.match('紀錄',message):
        try:
            record_list = prepare_record(message)
            result = insert_record(record_list)

            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=result))
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="資料上傳失敗"))
    elif re.match('查詢',message):
         result = select_record()
         line_bot_api.reply_message(event.reply_token,TextSendMessage(text=result))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage('呵呵'))


#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)