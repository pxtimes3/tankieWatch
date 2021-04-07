import json
import os
import pymysql
import re
import csv
from datetime import datetime as dt
from cherrypicker import CherryPicker
from dotenv import load_dotenv
load_dotenv()

bannedAuthors = json.load(open('./banned-authors.json'))

authorGrades = {}
authorsJson = {}

def connectToDb():
    try:
        connection = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            port=int(os.getenv("DB_PORT")),
            password=os.getenv("DB_PASS"),
            database="tankieWatch"
        )
        print("Connected to db: tankieWatch")
    except pymysql.Error as e:
        print(e)
        exit()
    return connection

def getAuthorData():
    authorData = {}
    try:
        connection.ping(reconnect=True)
        with connection.cursor() as cursor:
            cursor.execute("""SELECT ag.author_id, au.author, ag.grade, ag.postscore, ag.commscore
                FROM authorGrades ag
                JOIN authors au
                ON au.id = ag.author_id""")
            res = cursor.fetchall()
            for row in res:
                authorData[row[1]] = {
                    "id" : row[0],
                    "authorName" : row[1],
                    "grade" : row[2],
                    "postScore" : row[3],
                    "commScore" : row[4]
                }
                
    except pymysql.Error as e:
        print(e)
        exit()
    return authorData

def getUsersPerFile():
    directory = r'./json'
    uniqueAuthors = {}
    for entry in os.scandir(directory):
        if (entry.path.endswith(".json")):
            file = entry.path
            if "comments" in entry.path:
                type = "comments"
            else:
                type = "posts"

            # setup authorsJson
            match = re.search(r'\d{8}', entry.path)
            if match:
                date = dt.strptime(match.group(), "%Y%m%d").strftime("%Y-%m")
                if date not in authorsJson.keys():
                    authorsJson[date] = {}
            if "metadata" not in authorsJson[date].keys():
                authorsJson[date]["metadata"] = {}
            if type not in authorsJson[date].keys():
                authorsJson[date][type] = {}

            with open(file) as f:
                data = json.loads(f.read())
                authors = data['author']
                
                for key in authors:
                    author = authors[key]
                    if author not in bannedAuthors:
                        if author not in authorsJson[date][type].keys(): 
                            authorsJson[date][type][author] = 1
                        else: 
                            authorsJson[date][type][author] = authorsJson[date][type][author] + 1
                authorsJson[date]['metadata'][type] = {f"num{type}" : len(authorsJson[date][type])}
                    # if author not in bannedAuthors and not in uniqueAuthors:
                    #     uniqueAuthors[author] = 1
                    # else:
                    #     uniqueAuthors[author] = uniqueAuthors[author] + 1

def gradeDates():
    for date in authorsJson:
        for type in authorsJson[date]:
            score = 0
            if type == "posts" or type == "comments":
                for author in authorsJson[date][type]:
                    if author in authorData:
                        authorGrade = authorData[author]["grade"]
                        score = score + authorGrade
                authorsJson[date]["metadata"][type]["totalScore"] = score

def calcMetaData():
    for date in authorsJson:
        for type in authorsJson[date]["metadata"]:
            if type == "posts" or type == "comments":
                md = authorsJson[date]["metadata"][type]
                md['avg'] = round(float(md["totalScore"]) / float(md[f'num{type}']), 2)
            
        authorsJson[date]["metadata"]["totals"] = authorsJson[date]["metadata"]["posts"]["totalScore"] + authorsJson[date]["metadata"]["comments"]["totalScore"]
        authorsJson[date]["metadata"]["avg"] = authorsJson[date]["metadata"]["posts"]["avg"] + authorsJson[date]["metadata"]["comments"]["avg"] 

def convertToCsv():
    csvContent = {}

    f = open('mycsv.csv', 'w')
    with f as file:
            file.write('"month", "totals", "avg", "numPosts", "postTotal", "postAvg", "numComments", "commentsTotal", "commentsAvg"\n')
    for date in authorsJson.keys():
        md = authorsJson[date]['metadata']
        csvContent = {date:{}}
        csvContent[date]['totals'] = md['totals']
        csvContent[date]['avg'] = md['avg']
        for type in md:
            if type == "posts" or type == "comments":
                if type == "posts":
                    for data in md[type]:
                        csvContent[date]['numPosts'] = md[type]['numposts']
                        csvContent[date]['postTotal'] = md[type]['totalScore']
                        csvContent[date]['postAvg'] = md[type]['avg']
                if type == "comments":
                    for data in md[type]:
                        csvContent[date]['numComments'] = md[type]['numcomments']
                        csvContent[date]['commentsTotal'] = md[type]['totalScore']
                        csvContent[date]['commentsAvg'] = md[type]['avg']
    
        for n in csvContent:
            month = n
            totals = csvContent[n]['totals']
            avg = csvContent[n]['avg']
            numPosts = csvContent[n]['numPosts']
            postTotal = csvContent[n]['postTotal']
            postAvg = csvContent[n]['postAvg']
            numComments = csvContent[n]['numComments'] 
            commentsTotal = csvContent[n]['commentsTotal']
            commentsAvg = csvContent[n]['commentsAvg']
            f = open('mycsv.csv', 'a')
            print(f'writing {n}')
            with f as file:
                file.write(f'"{month}", "{totals}", "{avg}", "{numPosts}", "{postTotal}", "{postAvg}", "{numComments}", "{commentsTotal}", "{commentsAvg}"\n')
    f = open('mycsv.csv', 'a')
    with f as file:
        now = dt.today()
        file.write(f'"Created: {now}"')

connection = connectToDb()
authorData = getAuthorData()
getUsersPerFile()
gradeDates()
calcMetaData()
myCsv = convertToCsv()
csvColumns = ["month", "totals", "avg", "numPosts", "postTotal", "postAvg", "numComments", "commentsTotal", "commentsAvg"]

print(csvColumns)
