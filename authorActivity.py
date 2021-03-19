import pandas as pd
import random
from datetime import datetime as dt
import json
import os
import pymysql
import time
from pmaw import PushshiftAPI
from dotenv import load_dotenv

api = PushshiftAPI()
load_dotenv()

limit = int(os.getenv("LIMIT"))
userlimit =  int(os.getenv("USERLIMIT"))
graceDays =  int(os.getenv("GRACEDAYS"))
n = 0

bannedAuthors = ["AutoModerator", "[deleted]", "SnapshillBot", "BadDadBot", "BotMetric", "GoodBot_BadBot", "AbbrevTranslatorBot", "AgainstAHSCensorBot", "AlexaPlayBot", "AnimalFactsBot", "Anti", "AntiGoogleAmpBot", "AntiObnoxiousBot", "BadDadBot", "BigLebowskiBot", "Burgandy_Bot", "CMBDeletebot", "CakeDay", "Chuck_Norris_Jokebot", "ClickableLinkBot", "GitCommandBot", "GoodBot_BadBot", "Gyazo_Bot", "Link", "LinkifyBot", "MostAnnoyingBot", "News_Bot", "NoGoogleAMPBot", "PORTMANTEAU", "RedditSilverRobot", "RemindMeBot", "SuicideAwarenessBot", "ThePrequelMemesBot", "WikiTextBot", "YoMommaJokeBot", "converter", "friendly", "icarebot", "naughtabot", "nwordcountbot", "oofed", "remindditbot", "sub_doesnt_exist_bot", "these_days_bot", "tupac_cares_bot", "tweettranscriberbot", "twitterInfo_bot", "userleansbot", "wikipedia_text_bot", "wordscounterbot"]

start = time.time()

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
			cursor.execute("SELECT id,author FROM authors")
			result = cursor.fetchall()

except pymysql.Error as e:
	print(e)

def updatedDict():
	connection.ping(reconnect=True)
	#print("Connected to db: tankieWatch")
	updatedDict={}
	with connection.cursor() as cursor:
		try:
			query = "SELECT author_id, updated FROM activity"
			cursor.execute(query)
			result = cursor.fetchall()
			if result:
				for i in result:
					updatedDict[i[0]] = i[1]
				return updatedDict
			else:
				return False
		except pymysql.Error as e:
			print(e)	

def countEntityPerSub(jsonStr):
	uniqueSubs = {}
	jsonStr = json.loads(jsonStr)
	for k in jsonStr['subreddit']:
	 	subreddit = jsonStr['subreddit'][k]
	 	if subreddit not in uniqueSubs:
	 		uniqueSubs[subreddit] = 1
 		else: 
 			uniqueSubs[subreddit] = uniqueSubs[subreddit] + 1
	
	return uniqueSubs

def insertActivity(authorDict, author_id):
	try:
		connection.ping(reconnect=True)
		with connection.cursor() as cursor:
			try:
				query = '''
				INSERT INTO activity (author_id, activity, updated) VALUES (%s, %s, CURRENT_TIMESTAMP) 
				ON DUPLICATE KEY UPDATE activity=%s, updated=CURRENT_TIMESTAMP
				'''
				updated = dt.today().timestamp()
				cursor.execute(query, (author_id, authorDict, authorDict))
				connection.commit()
				result = cursor.rowcount

				if (result == 0):
					print("Something went wrong. Query was:")
					print(query)
					exit()
				else:
					print(f'Processed author_id {author_id}. {result} rows affected.')
			except pymysql.Error as e:
				print(e)
				print(query)
	except pymysql.Error as e:
		print(e)

updatedDict = updatedDict()

for i in result:
	if n == userlimit and userlimit != 0:
		break

	author = i[1]
	author_id = i[0]

	authorDict = {}

	# check updated for author_id
	if author_id not in updatedDict:
		delta = False
	else:
		delta = dt.now() - updatedDict[author_id]
	
	if delta == False or delta.days > graceDays and author not in bannedAuthors:

		print(f'Fetching posts for: {author}')
		posts = api.search_submissions(author=author, limit=limit, fields=['id','author','subreddit'])
		numPosts = len(posts)
		print(f'{numPosts} posts from {author} retrieved from Pushshift')
		
		if (numPosts > 0):
			posts_df = pd.DataFrame(posts)
			authorDict['posts'] = countEntityPerSub(posts_df.to_json())
		
		print(f'Fetching comments for: {author}')
		comments = api.search_comments(author=author, limit=limit, fields=['id','author','subreddit'])
		numComments = len(comments)
		print(f'{numComments} comments from {author} retrieved from Pushshift')
		
		if (numComments > 0):
			comments_df = pd.DataFrame(comments)
			authorDict['comments'] = countEntityPerSub(comments_df.to_json())

		#authorDict = {'posts': {'AmongUs': 8, 'ImaginaryMonsters': 1, 'Art': 2, 'TrevorHenderson': 1, 'backrooms': 2, 'findareddit': 1, 'TattooDesigns': 2, 'Libertarian': 1, 'DnDHomebrew': 1, 'cobrakai': 4, 'wargame': 1, 'DrawMyTattoo': 1, 'shittytechnicals': 7, 'vexillologycirclejerk': 1, 'vexillology': 15, 'menofwar': 1, 'evilbuildings': 1, 'tea': 1, 'Kaiserreich': 7, 'simpsonsshitposting': 3, 'LiminalSpace': 2, 'AfterTheEndFanFork': 1, 'offmychest': 1, 'AskReddit': 4, 'DnD': 4, 'Minecraft': 3, 'readanotherbook': 1, 'minipainting': 1, 'NoStupidQuestions': 1, 'TwoSentenceHorror': 5, 'Steel_Division': 4, 'gusjohnson': 2, 'Stanrogers': 1, 'XFiles': 1, 'Zoroastrianism': 1, 'workout': 1, 'LiminalReality': 1, 'evangelion': 1, 'evangelionmemes': 1, 'NeonGenesisEvangelion': 3, 'IThinkYouShouldLeave': 3, 'OldSchoolCool': 1, 'TheLastAirbender': 2, 'StupidFood': 1, 'thatHappened': 1, 'Poetry': 2, 'AlternateHistory': 10, 'DebateCommunism': 1, 'creativewriting': 1, 'Poems': 1, 'justpoetry': 1, 'OCPoetry': 1, 'boltaction': 1, 'hoi4modding': 3, 'hoi4': 1, 'gaming': 1, 'lego': 1, 'Wellthatsucks': 1, 'interestingasfuck': 1, 'MilitaryPorn': 1, 'copypasta': 3, 'Bandnames': 3, 'KRGmod': 1, 'FdRmod': 1, 'seashanties': 3, 'ShitWehraboosSay': 6, 'conservation': 2, 'videos': 1, 'CanadianPolitics': 1, 'MadeMeSmile': 1, 'JoelHaver': 1, 'kurtisconner': 1, 'GusAndEddy': 1}, 'comments': {'ImaginaryMonsters': 6, 'MakeMeSuffer': 5, 'AskReddit': 6, 'wargame': 29, 'iamverybadass': 2, 'herpetology': 1, 'kurtisconner': 1, 'AmongUs': 10, 'LiminalSpace': 2, 'somnivexillology': 1, 'backrooms': 8, 'Art': 1, 'insects': 3, 'boltaction': 5, 'Steel_Division': 51, 'mildlyinteresting': 1, 'cobrakai': 16, 'TrevorHenderson': 1, 'oddlyterrifying': 1, 'findareddit': 2, 'worldjerking': 12, 'heraldry': 1, 'Libertarian': 17, 'simpsonsshitposting': 3, 'DrawMyTattoo': 1, 'DnDHomebrew': 3, 'TheLastAirbender': 7, 'TargetedShirts': 5, 'mallninjashit': 1, 'community': 1, 'DunderMifflin': 2, 'submechanophobia': 1, 'TheSimpsons': 5, 'shittytechnicals': 32, 'ImaginaryBeasts': 1, 'OldSchoolRidiculous': 1, 'wwiipics': 10, 'vexillology': 39, 'NationsAndCannons': 1, 'Whatcouldgowrong': 1, 'UrbanHell': 1, 'IThinkYouShouldLeave': 27, 'MilitaryHistory': 5, 'interestingasfuck': 5, 'menofwar': 1, 'Militariacollecting': 10, 'Minecraft': 1, 'ww2': 24, 'cryptids': 1, 'magnetfishing': 1, 'TattooDesigns': 2, 'milsurp': 8, 'lotrmemes': 2, 'bigfoot': 2, 'Kaiserreich': 11, 'imaginarymaps': 11, 'animation': 1, 'shittysuperpowers': 5, 'kaiserredux': 1, 'AnimalsOnReddit': 2, 'oddlyspecific': 3, 'OldSchoolCool': 1, 'Humanoidencounters': 1, 'Cryptozoology': 2, 'readanotherbook': 12, 'foraging': 7, 'tabletoplive': 1, 'distantsocializing': 1, 'TechNewsToday': 2, 'NeonGenesisEvangelion': 14, 'LifeProTips': 2, 'RoastMe': 2, 'politics': 8, 'entertainment': 6, 'whereintheworld': 4, 'PublicFreakout': 4, 'polls': 2, 'CustomPlayerCutscene': 2, 'LessCredibleDefence': 4, 'thatHappened': 3, 'CursedTanks': 1, 'MarvelCringe': 9, 'Armor': 1, 'bookscirclejerk': 11, 'writingcirclejerk': 1, 'imsorryjon': 1, 'Medievalart': 3, 'AlternateHistory': 23, 'XFiles': 1, 'IASIP': 5, 'badhistory': 1, 'DebateCommunism': 1, 'hoi4modding': 6, 'hoi4': 2, 'tattoos': 1, 'RaftTheGame': 1, 'gaming': 2, 'offmychest': 3, 'Wellthatsucks': 3, 'ABoringDystopia': 1, 'worldnews': 3, 'papertowns': 2, 'FdRmod': 8, 'evilbuildings': 6, 'Naturewasmetal': 4, 'ImaginaryHorrors': 2, 'HistoryPorn': 8, 'wokekids': 28, 'The_Leftorium': 2, 'forwardsfromgrandma': 8, 'JoelHaver': 2, 'natureismetal': 4, 'SelfAwarewolves': 2, 'redneckengineering': 2, 'moviescirclejerk': 18, 'Archaeology': 2, 'badscificovers': 2, 'StupidFood': 2, 'shittytattoos': 2, 'vexillologycirclejerk': 6, 'AbruptChaos': 2, 'AbandonedPorn': 2, 'CornerGas': 2, 'MontyPythonMemes': 2, 'seashanties': 10, 'johnbrownposting': 2, 'inkarnate': 2, 'ShittyGifRecipes': 4, 'gusjohnson': 2, 'ShitWehraboosSay': 42, 'DnD': 2, 'niceguys': 4, 'justneckbeardthings': 2, 'GusAndEddy': 2, 'ifuckinghatecats': 4, 'TheWayWeWere': 2, 'TheMagnusArchives': 4, 'SWORDS': 2, 'SoulKnight': 2, 'KRGmod': 2, 'cringepics': 2, 'videos': 2, 'Warhammer': 2}}
		if numComments > 0 or numPosts > 0:
			insertActivity(json.dumps(authorDict), i[0])
		n = n + 1
	else:
		if delta != False:
			print(f'{author} is in the range of graceDays({graceDays}): {graceDays - delta.days}. Skipping.')
	
end = time.time()
print(f"Fetched {n} users in {end - start} seconds.")