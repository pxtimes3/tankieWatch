import pandas as pd
import os
from calendar import monthrange

from psaw import PushshiftAPI
api = PushshiftAPI()

from dateutil.relativedelta import relativedelta
from datetime import datetime as dt

subreddit="shitWehraboosSay"
limit=100000
workers=(os.cpu_count()*4)-2
months=1

start = dt.strptime(dt.today().strftime("%Y%m"), "%Y%m")

for x in range(months):

    if x == 0:
        after = dt.strptime((dt.today() - relativedelta(months=1)).strftime("%Y%m"), "%Y%m")
    else:
        after = dt.strptime((after - relativedelta(months=1)).strftime("%Y%m"), "%Y%m")

    days = monthrange(int(after.strftime("%Y")),int(after.strftime("%m")))
    
    before = after + relativedelta(days=int(days[1] - 1))

    print(f'Checking {before.strftime("%Y-%m-%d")} to {after.strftime("%Y-%m-%d")}')

    comments = api.search_comments(num_workers=workers, subreddit=subreddit, limit=10, before=int(dt.timestamp(before)), after=int(dt.timestamp(after)), fields=['id','author','created_utc'])
    commentResults=list(comments)
    print(f'Retrieved {len(commentResults)} comments from Pushshift')

    comments_df = pd.DataFrame([thing.d_ for thing in commentResults])

    posts = api.search_submissions(num_workers=workers, subreddit=subreddit, limit=10, before=int(dt.timestamp(before)), after=int(dt.timestamp(after)), fields=['id','author','created_utc'])
    postResults=list(posts)
    print(f'Retrieved {len(postResults)} posts from Pushshift')

    posts_df = pd.DataFrame([thing.d_ for thing in postResults])

    commentsFile = f'.json/{before.strftime("%Y%m%d")}-{after.strftime("%Y%m%d")}-{subreddit}-comments.json'
    postsFile = f'.json/{before.strftime("%Y%m%d")}-{after.strftime("%Y%m%d")}-{subreddit}-posts.json'

    comments_df.to_json(commentsFile)
    posts_df.to_json(postsFile)