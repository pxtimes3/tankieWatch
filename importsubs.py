import os
from mysql.connector import connect, Error
from datetime import datetime as dt
from dotenv import load_dotenv
load_dotenv()

try:
	with connect(
		host=os.getenv("DB_HOST"),
		user=os.getenv("DB_USER"),
		port=os.getenv("DB_PORT"),
		password=os.getenv("DB_PASS"),
		database="tankieWatch"
	) as connection:
		print("Connected to db: tankieWatch")
		with open('startsubs.txt') as f:
			for line in f:
				query = f'INSERT INTO subreddits (name, updated) VALUES ("{line}", from_unixtime({int(dt.today().timestamp())})) ON DUPLICATE KEY UPDATE id=id;'
				with connection.cursor() as cursor:
					cursor.execute(query)
					connection.commit()
except Error as e:
	print(e)
