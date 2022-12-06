from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


#======這裡是呼叫的檔案內容=====
from message import *
from new import *
from Function import *
#======這裡是呼叫的檔案內容=====

#======python的函數庫==========
import tempfile, os
import datetime
import time
#======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi('EhLXS8j5jb9N3DfAI6vSDq1Pcw4+Z2HwRuzOZl4jJL1URF5L3aQz5vWUgQeMs8R4Z9E+83YEQIzTfVSgvUAXO9fZ5gvuojzNhr1BhCPb/lTII1nYdAapbtgvt15DMj3hVexmPiUnuh7Yb/PcjydOngdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('9b6599c4219cd7734f0bc5418248d18e')


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


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if(event.message.text=="CPU超載"):
        message = []
        message.append(TextSendMessage(text="您只要在您的電腦輸入\"CPU修復碼58126\"，就可正常運行了"))
        line_bot_api.reply_message(event.reply_token, message)
    elif event.message.text=="哈囉":
        message = []
        message.append(TextSendMessage(text="哈囉"))
        line_bot_api.reply_message(event.reply_token, message)
    else:
        msg="我聽不太懂qq，可以再說一次嗎"
        message=[]
        message.append(TextSendMessage(text=msg))
        line_bot_api.reply_message(event.reply_token, message)

@handler.add(PostbackEvent)
def handle_message(event):
    print(event.postback.data)


@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)
        
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
