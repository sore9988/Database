import pymysql
import os
import json
import pandas as pd
from sqlalchemy import create_engine
pymysql.install_as_MySQLdb()
import MySQLdb

# 載入 mysql data
with open("dish_db.json", "r",encoding="utf-8") as f:
        db_json = json.loads(f.read())

user = db_json["user"]
passwd = db_json["passwd"]
host = db_json["host"]
port = db_json["port"]
db_name = db_json["db_name"]
engine = create_engine('mysql://{0}:{1}@{2}:{3}/{4}?charset=utf8'.format(user,passwd,host,port,db_name))

# sqlalchemy.create_engine方式
# 搜尋店家所有評論
def store_text_id(store_id):
	sql = "SELECT * FROM Store_db.reviews WHERE `store_id`='{0}'".format(store_id)
	df = pd.read_sql_query(sql, engine)
	return df
# print(store_text_id(10))

# 搜尋該區所有店家資料
def store_find(city, district):
	store_list = []
	sql = "SELECT * FROM Store_db.stores WHERE `city`='{0}' and `district`='{1}'".format(city, district)
	df = pd.read_sql_query(sql, engine)
	for i in range(len(df)) :
		store_list = store_list + [(df.loc[i, "city"], df.loc[i, "district"], df.loc[i, "store_id"], df.loc[i, "name"], store_text_id(df.loc[i, "store_id"]))]
	return store_list
# x = store_find('台北市', '中山區')
# print(len(x),x)

# 關鍵字及情緒更新
def sentiment_update(text_id, sentiment):
	sql = "UPDATE Store_db.reviews SET `dish`=%s, `service`=%s, `environment`=%s, \
	`cp`=%s, `traffic`=%s, `general`=%s, `food`=%s WHERE `id`=%s"
	engine.execute(sql, (sentiment[0], sentiment[1], sentiment[2], sentiment[3], sentiment[4], sentiment[5], sentiment[6], text_id))
	print("已完成更新")
# sentiment_list = ["dish", "service", "environment", "cp", "traffic", "general", "food"]
# sentiment = ["炸豆腐,1", None, None, None, None, None, None]
# sentiment_update('2', sentiment)

# 更新圖片
def image_update(store_id, image_path):
	sql = "UPDATE Store_db.stores SET `img`=%s WHERE `store_id`=%s"
	engine.execute(sql, (image_path, store_id))
	print("已完成更新")
# image_update('3', "https://ai.enadv.idv.tw/images/3.png")

# 依店名路名提供API所需 json檔
def store_json(name, road):
	sql = "SELECT * FROM Store_db.stores WHERE `name`='{0}' and `road`='{1}'".format(name, road)
	df = pd.read_sql_query(sql, engine)
	json_file = {}
	for i in list(df):
		json_file[i] = df.loc[0, i]
	return json_file
y = store_json("勁喝呷熱炒", "長春路119-9號")
print(y)
