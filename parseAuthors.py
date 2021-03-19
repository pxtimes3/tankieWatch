import json
import os
import pymysql
from datetime import datetime as dt
from dotenv import load_dotenv
load_dotenv()

try:
    with pymysql.connect(
        host=os.getenv("DB_HOST"),
  		user=os.getenv("DB_USER"),
  		port=int(os.getenv("DB_PORT")),
  		password=os.getenv("DB_PASS"),
        database="tankieWatch"
    ) as connection:
        print("Connected to db: tankieWatch")
except pymysql.Error as e:
    print(e)

bannedAuthors = ["AutoModerator", "[deleted]", "SnapshillBot", "BadDadBot", "BotMetric", "GoodBot_BadBot", "AbbrevTranslatorBot", "AgainstAHSCensorBot", "AlexaPlayBot", "AnimalFactsBot", "Anti", "AntiGoogleAmpBot", "AntiObnoxiousBot", "BadDadBot", "BigLebowskiBot", "Burgandy_Bot", "CMBDeletebot", "CakeDay", "Chuck_Norris_Jokebot", "ClickableLinkBot", "GitCommandBot", "GoodBot_BadBot", "Gyazo_Bot", "Link", "LinkifyBot", "MostAnnoyingBot", "News_Bot", "NoGoogleAMPBot", "PORTMANTEAU", "RedditSilverRobot", "RemindMeBot", "SuicideAwarenessBot", "ThePrequelMemesBot", "WikiTextBot", "YoMommaJokeBot", "converter", "friendly", "icarebot", "naughtabot", "nwordcountbot", "oofed", "remindditbot", "sub_doesnt_exist_bot", "these_days_bot", "tupac_cares_bot", "tweettranscriberbot", "twitterInfo_bot", "userleansbot", "wikipedia_text_bot", "wordscounterbot"]
uniqueAuthors = {}

directory = r'./json'
#ext = ("comments.json", "posts.json")
for entry in os.scandir(directory):
    if (entry.path.endswith(".json")):
        file = entry.path

        with open(file) as f:
            data = json.loads(f.read())
            authors = data['author']

            for key in authors:
                author = authors[key]
                if author not in bannedAuthors:
                    if author not in uniqueAuthors:
                        uniqueAuthors[author] = 1
                    else:
                        uniqueAuthors[author] = uniqueAuthors[author] + 1

uniqueAuthors = sorted(uniqueAuthors.items(), key=lambda x:x[0], reverse=False)

connection.ping(reconnect=True)
for i in uniqueAuthors:
	#print(i[0], i[1])
	insertAuthorQuery = f'''
    INSERT INTO authors (author, updated) 
    VALUES ("{i[0]}", from_unixtime({int(dt.today().timestamp())})) 
    ON DUPLICATE KEY 
    UPDATE id=id;
    '''
	
	with connection.cursor() as cursor:
	    cursor.execute(insertAuthorQuery)
	    connection.commit()


print(f'Total # of authors: {len(uniqueAuthors)}')