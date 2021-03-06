import os
import json
import pymysql
from datetime import datetime as dt
from dotenv import load_dotenv
load_dotenv()

subreddits = {}

try:
	with pymysql.connect(
		host=os.getenv("DB_HOST"),
		user=os.getenv("DB_USER"),
		port=int(os.getenv("DB_PORT")),
		password=os.getenv("DB_PASS"),
		database="tankieWatch"
	) as connection:
		print("Connected to db: tankieWatch")
		with connection.cursor() as cursor:
			cursor.execute("SELECT name, weight FROM subreddits")
			result = cursor.fetchall()
		for i in range(len(result)):
			subreddits[result[i][0]] = result[i][1]
		with open('startsubs.json') as f:
			data = json.load(f)
			for i in data:
				
				subreddit=i.strip()
			
				query = f'''
				INSERT INTO subreddits (name, weight, updated) VALUES ("{i}", {data[i]}, from_unixtime({int(dt.today().timestamp())})) 
				ON DUPLICATE KEY 
				UPDATE updated=from_unixtime({int(dt.today().timestamp())}), weight={data[i]}, name="{subreddit}";
				'''

				with connection.cursor() as cursor:
					try:
						cursor.execute(query)
						result = cursor.rowcount
						connection.commit()
					except pymysql.Error as e:
						print(query,e)
except pymysql.Error as e:
	print(e)
