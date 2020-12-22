#!venv/bin/python

# 載入需要的模組
import os
import sys
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
import psycopg2
import json
import flex_search_confirm

'''
參數：
line_bot_api:           line_bot_api物件
conn:                   資料庫連線
event:                  message_api事件
user_id:                使用者ID
text:                   使用者輸入內容
status                  使用者搜尋狀態
tdee                    紀錄tdee
'''

# 計算 tdee
# 辨認是男生或女生
def count_tdee(line_bot_api, conn, event, user_id, text, status, gender, high, weight, age, activity):
    # 紀錄參數 tdee
    tdee = 0
    # 更新使用者搜尋狀態為記錄個人資料
    cursor = conn.cursor()
    print("準備計算 tdee")
    SQL_order = f'''
    update userinfo set status = '計算 tdee' where userid = '{user_id}';
    '''
    cursor.execute(SQL_order)
    conn.commit()

    if gender = "女":
        if activity = "低":
            # 更新使用者搜尋狀態為計算tdee & 將tdee寫入資料庫
            tdee = ((9.6*weight) + (1.8*high) – (4.7*age) + 655)*1.2
            cursor = conn.cursor()
            print(f"紀錄tdee：{gender}{activity}")
            SQL_order = f'''
            update userinfo set tdee = '{tdee}';
            update userinfo set status = '計算tdee' where userid = '{user_id}';
            '''
            cursor.execute(SQL_order)
            conn.commit()
            print("SQL更新userinfo狀態:計算tdee 成功")
            return tdee
        elif activity = "中"：
            # 更新使用者搜尋狀態為計算tdee & 將tdee寫入資料庫
            tdee = ((9.6*weight) + (1.8*high) – (4.7*age) + 655)*1.55
            cursor = conn.cursor()
            print(f"紀錄tdee：{gender}{activity}")
            SQL_order = f'''
            update userinfo set tdee = '{tdee}' where userid = '{user_id};
            update userinfo set status = '計算tdee' where userid = '{user_id}';
            '''
            cursor.execute(SQL_order)
            conn.commit()
            print("SQL更新userinfo狀態:計算tdee 成功")
            return tdee
        else activity = "高"：
            # 更新使用者搜尋狀態為計算tdee & 將tdee寫入資料庫
            tdee = ((9.6*weight) + (1.8*high) – (4.7*age) + 655)*1.9
            cursor = conn.cursor()
            print(f"紀錄tdee：{gender}{activity}")
            SQL_order = f'''
            update userinfo set tdee = '{tdee}' where userid = '{user_id};
            update userinfo set status = '計算tdee' where userid = '{user_id}';
            '''
            cursor.execute(SQL_order)
            conn.commit()
            print("SQL更新userinfo狀態:計算tdee 成功")
            return tdee
    elif：
        if activity = "低":
            # 更新使用者搜尋狀態為計算tdee & 將tdee寫入資料庫
            tdee = ((13.7*weight) + (5*high) – (6.8*age) + 66)*1.2
            cursor = conn.cursor()
            print(f"紀錄tdee：{gender}{activity}")
            SQL_order = f'''
            update userinfo set tdee = '{tdee}' where userid = '{user_id};
            update userinfo set status = '計算tdee' where userid = '{user_id}';
            '''
            cursor.execute(SQL_order)
            conn.commit()
            print("SQL更新userinfo狀態:計算tdee 成功")
            return tdee
        elif activity = "中"：
            # 更新使用者搜尋狀態為計算tdee & 將tdee寫入資料庫
            tdee = ((13.7*weight) + (5*high) – (6.8*age) + 66)*1.55
            cursor = conn.cursor()
            print(f"紀錄tdee：{gender}{activity}")
            SQL_order = f'''
            update userinfo set tdee = '{tdee}' where userid = '{user_id};
            update userinfo set status = '計算tdee' where userid = '{user_id}';
            '''
            cursor.execute(SQL_order)
            conn.commit()
            print("SQL更新userinfo狀態:計算tdee 成功")
            return tdee
        else activity = "高"：
            # 更新使用者搜尋狀態為計算tdee & 將tdee寫入資料庫
            tdee = ((13.7*weight) + (5*high) – (6.8*age) + 66)*1.9
            cursor = conn.cursor()
            print(f"紀錄tdee：{gender}{activity}")
            SQL_order = f'''
            update userinfo set tdee = '{tdee}' where userid = '{user_id};
            update userinfo set status = '計算tdee' where userid = '{user_id}';
            '''
            cursor.execute(SQL_order)
            conn.commit()
            print("SQL更新userinfo狀態:計算tdee 成功")
            return tdee   
    print("SQL更新userinfo狀態:計算tdee 成功")
    cursor.close()
    # 回傳訊息
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=f"計算完成！您的TDEE為{tdee}"))