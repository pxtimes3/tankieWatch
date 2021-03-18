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
				# exists?
				if i in subreddits:
					if data[i] != subreddits[i]:
						print(f'Weight change for {i}. From {subreddits[i]} to {data[i]}')
					
						query = f'''
						INSERT INTO subreddits (name, weight, updated) VALUES ("{i}", {data[i]}, from_unixtime({int(dt.today().timestamp())})) 
						ON DUPLICATE KEY 
						UPDATE updated=from_unixtime({int(dt.today().timestamp())}), weight={data[i]};
						'''

						with connection.cursor() as cursor:
							cursor.execute(query)
							result = cursor.rowcount
							connection.commit()
							if result > 1:
								print(f'Updated {i}, {data[i]}')
							elif result == 1:
								print(f'Added {i}, {data[i]}')
							else:
								print(f'Failed {i}, {data[i]}')
except pymysql.Error as e:
	print(e)
