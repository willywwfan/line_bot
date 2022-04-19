from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import os
import json
import ssl

import psycopg2
from datetime import datetime

# test
def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps("Hello from Lambda!")
  }

# body
class PostgresBaseManager:

    def __init__(self):
        self.database = 'd9r8va4pq94vp5'
        self.user = 'vnnvynpuzipegu'
        self.password = 'e17d5a6ec332f03123b57b0fddd18a7bc5dcbda5908853191d84f293bab4bd3c'
        self.host = 'ec2-52-203-118-49.compute-1.amazonaws.com'
        self.port = '5432'
        self.conn = self.connectServerPostgresDb()

        self.rawlimit = 2000

    def connectServerPostgresDb(self):
        """
        :return: 連接 Heroku Postgres SQL 認證用
        """
        conn = psycopg2.connect(dbname=self.database,user=self.user,password=self.password,host=self.host,port=self.port,sslmode="require")
        return conn

    def closePostgresConnection(self):
        """
        :return: 關閉資料庫連線使用
        """
        self.conn.close()

    def insert(self,text,num,send_user):
        cur = self.conn.cursor()
        date = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        cur.execute("INSERT INTO accounts_table (owner_name, text, amount, date) VALUES (%s, %s, %s, %s);", (send_user, text, num, date))
        self.conn.commit()

        select = "SELECT MAX(record_no) FROM accounts_table"
        cur.execute(select)
        max_record_no = cur.fetchall()[0][0]
        print(max_record_no)

        limit = "DELETE FROM accounts_table WHERE record_no < " + str(max_record_no-19) + " RETURNING *;"
        cur.execute(limit)
        self.conn.commit()
        deleted = cur.fetchall()
        
        cur.execute("SELECT * FROM accounts_table;")
        rows = cur.fetchall()
        self.last3 = [" "," "," "]
        for row in rows:
            datas = ""
            for data in row:
                datas = datas + str(data) + ", "
            self.last3 = self.last3[1:] + [datas]
        
        self.last3 = self.last3[0] + "\n\t\n" + self.last3[1] + "\n\t\n" + self.last3[2]
    
    def select(self, interval):
        cur = self.conn.cursor()
        if interval == "月":select_input = "month"
        elif interval == "周" or "週":select_input = "week"
        elif interval == "日":select_input = "day"
        query = "SELECT * FROM accounts_table WHERE DATE_PART('" + select_input + "', date) = DATE_PART('" + select_input + "', NOW());"
        cur.execute(query)
        rows = cur.fetchall()
        self.selected = ""
        for row in rows:
            datas = ""
            for data in row:datas = datas + str(data) + ", "
            self.selected += datas + "\n\t\n"
        self.selected = self.selected[:-3]

postgres_manager = PostgresBaseManager()


line_bot_api = LineBotApi(os.environ['Channel_access_token'])
handler = WebhookHandler(os.environ['Channel_secret'])

def getnum(text):
    seps = text.split()
    nums = []
    for sep in seps:
        num = "0"
        for string in sep:
            if string.isdigit():num += string
            else:num = "0"
        nums += [int(num)]
    return max(nums)

def lambda_handler(event, context):
    @handler.add(MessageEvent, message=TextMessage)
    def handle_message(event):
        if "記帳" in event.message.text:
            text = event.message.text
            text_message = ''.join([i for i in text if not i.isdigit() and i != " "]).replace("記帳","") #in
            num = getnum(text) #in
            send_user = event.source.user_id
            profile = line_bot_api.get_profile(send_user)
            display_user = profile.display_name #in
            
            postgres_manager.insert(text_message,num,display_user)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="記帳成功！上三筆資料:\n" + postgres_manager.last3))
                # TextSendMessage(text=event.message.text))
        if "查詢本" in event.message.text:
            postgres_manager.select(event.message.text[-1])
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=postgres_manager.selected))
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=event.message.text))

    # get X-Line-Signature header value
    signature = event['headers']['x-line-signature']

    # get request body as text
    body = event['body']

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return {
            'statusCode': 502,
            'body': json.dumps("Invalid signature. Please check your channel access token/channel secret.")
            }
    return {
        'statusCode': 200,
        'body': json.dumps("Hello from Lambda!")
        }