import json
import os
import pymysql
from datetime import datetime as dt
from dotenv import load_dotenv
load_dotenv()

postWeight=int(os.getenv("POSTWEIGHT"))
commWeight=int(os.getenv("COMMWEIGHT"))

def connectToDb():
    connection = pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        port=int(os.getenv("DB_PORT")),
        password=os.getenv("DB_PASS"),
        database="tankieWatch"
    )
    print("Connected to db: tankieWatch")
    return connection

def fetchSubreddits():
    try:
        subreddits={}
        connection.ping(reconnect=True)
        with connection.cursor() as cursor:
            cursor.execute("SELECT name,weight FROM subreddits")
            result = cursor.fetchall()
        for i in result:
            subreddits[i[0]] = i[1]
        return subreddits
    except pymysql.Error as e:
	    print(e)
    return False

def fetchActivityData():
    try:
        connection.ping(reconnect=True)
        with connection.cursor() as cursor:
            cursor.execute("SELECT author_id, activity FROM activity")
            result = cursor.fetchall()
            return result
    except pymysql.Error as e:
        print(e)
    

def gradeAuthor(authorData, subreddits):
    #print(type(authorData))
    postscore=0
    commscore=0
    
    authorId = authorData[0]
    try:
        authorActivity = json.loads(authorData[1])
    except ValueError as e:
        print(authorData[1])
        print(json.loads(authorData[1]["comments"]))
        print(e)
        exit()

    if "posts" in authorActivity.keys():
        for i in authorActivity['posts'].keys():
            if i.lower() in subreddits:
                weight = subreddits[i.lower()]
                instances = authorActivity['posts'][i]
                postscore = postscore + ((instances * weight) * postWeight)
    #            print(postscore)
    #else:
    #    print("No posts found!")

    if "comments" in authorActivity.keys():
        for i in authorActivity['comments'].keys():
            if i.lower() in subreddits:
                weight = subreddits[i.lower()]
                instances = authorActivity['comments'][i]
                commscore = commscore + ((instances * weight) * commWeight)
    #            print(commscore)
    #else:
    #    print("No comments found!")
    grade = postscore + commscore
    saveAuthorGrade(authorId, grade, postscore, commscore)

def saveAuthorGrade(author_id, grade, postscore, commscore):
    connection.ping(reconnect=True)
    with connection.cursor() as cursor:
        try:
            query = '''
            INSERT INTO authorGrades (author_id, grade, postscore, commscore, updated) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP) 
            ON DUPLICATE KEY UPDATE grade=%s, postscore=%s, commscore=%s, updated=CURRENT_TIMESTAMP
            '''
            updated = dt.today().timestamp()
            cursor.execute(query, (author_id, grade, int(postscore), int(commscore), grade, int(postscore), int(commscore)))
            connection.commit()
            result = cursor.rowcount

            if (result == 0):
                print("Something went wrong. Query was:")
                print(query)
                exit()
            else:
                print(f'Graded author_id: {author_id}, grade: {grade} ({postscore}/{commscore}). {result} rows affected.')
        except pymysql.Error as e:
            print(e)
            print(query)

connection = connectToDb()
subreddits = fetchSubreddits()
activityData = fetchActivityData()

n=0
for i in activityData:
    gradeAuthor(i, subreddits)
    #n = n + 1
    #if n > 10:
    #    break