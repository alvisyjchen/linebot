#!venv/bin/python
# -*- coding: utf-8 -*-

import csv
import os
import psycopg2
from sqlalchemy import create_engine
import pandas as pd

# 連線到 heroku postgreSQL
DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a linebotforkal').read()[:-1]
conn = psycopg2.connect(DATABASE_URL, sslmode = 'require')

# 讀取 csv 檔，匯入資料庫
with open('/Users/Yoyo/linebot/food_calories.csv', newline = '', encoding = 'utf-8') as csvfile:
    df = pd.read_csv(csvfile)
    # print(df)
    engine = create_engine('postgres://noxojznwmspygx:95c0794901a73aa667bd1d72d8edda7a60e5b75f1ac0fedc47816bbaaf6b49b5@ec2-54-160-73-231.compute-1.amazonaws.com:5432/d4m7u8qr4fprcd')
    print(engine)
    df.to_sql('food_caloriess', engine, if_exists='replace')
    print('done')