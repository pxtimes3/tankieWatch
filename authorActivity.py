import pandas as pd
import json
import os
from pmaw import PushshiftAPI
api = PushshiftAPI()
from mysql.connector import connect, Error
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
		with connection.cursor() as cursor:
			cursor.execute("SELECT id,author FROM authors")
			result = cursor.fetchall()

		#print(result)
except Error as e:
	print(e)

def countEntityPerSub(jsonStr):
	uniqueSubs = {}
	jsonStr = json.loads(jsonStr)
	print(len(jsonStr['subreddit']),type(jsonStr['subreddit']))
	for k in jsonStr['subreddit']:
	 	subreddit = jsonStr['subreddit'][k]
	 	if subreddit not in uniqueSubs:
	 		uniqueSubs[subreddit] = 1
 		else: 
 			uniqueSubs[subreddit] = uniqueSubs[subreddit] + 1
		#pass
	
	return uniqueSubs

for i in result:
	authorDict = {
		"posts" : {},
		"comments" : {},
	}
	author = i[1]
	
	print(f'Fetching posts for: {author}')
	posts = api.search_submissions(author=author, limit=100000, fields=['id','author','subreddit'])
	print(f'{len(posts)} posts from {author} retrieved from Pushshift')
	posts_df = pd.DataFrame(posts)
	authorDict['posts'] = countEntityPerSub(posts_df.to_json())
	# posts_df = pd.DataFrame(posts)
	# postsFile = f'{author}-posts.json'
	# posts_df.to_json(postsFile)

	print(f'Fetching comments for: {author}')
	comments = api.search_comments(author=author, limit=100000, fields=['id','author','subreddit'])
	print(f'{len(comments)} comments from {author} retrieved from Pushshift')
	comments_df = pd.DataFrame(comments)
	authorDict['comments'] = countEntityPerSub(comments_df.to_json())
	# commentsFile = f'{author}-comments.json'
	# comments_df.to_json(commentsFile)
	print(authorDict)
