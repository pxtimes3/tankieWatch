import json
import os
import pymysql
from datetime import datetime as dt
from dotenv import load_dotenv
load_dotenv()

subreddits={}

def fetchSubreddits():
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
                cursor.execute("SELECT name,weight FROM subreddits")
                result = cursor.fetchall()
    except pymysql.Error as e:
	    print(e)
    
    for i in result:
        print(i)

def fetchActivityData(author_id):
    pass

def gradeAuthor(author_id, type):
    pass

def saveAuthorGrade(author_id, grade):
    pass

fetchSubreddits()