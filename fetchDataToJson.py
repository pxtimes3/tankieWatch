
import pandas as pd
import os
from calendar import monthrange

from pmaw import PushshiftAPI
api = PushshiftAPI()

from dateutil.relativedelta import relativedelta
from datetime import datetime as dt

subreddit="shitWehraboosSay"
limit=100000
workers=(os.cpu_count()*4)-2
months=3

start = dt.strptime(dt.today().strftime("%Y%m"), "%Y%m")

for x in range(months):

    if x == 0:
        after = dt.strptime((dt.today() - relativedelta(months=1)).strftime("%Y%m"), "%Y%m")
    else:
        after = dt.strptime((after - relativedelta(months=1)).strftime("%Y%m"), "%Y%m")

    days = monthrange(int(after.strftime("%Y")),int(after.strftime("%m")))
    
    before = after + relativedelta(days=int(days[1] - 1))

    print(f'Checking {before.strftime("%Y-%m-%d")} to {after.strftime("%Y-%m-%d")}')

    comments = api.search_comments(num_workers=workers, subreddit=subreddit, limit=limit, before=int(dt.timestamp(before)), after=int(dt.timestamp(after)))

    print(f'Retrieved {len(comments)} comments from Pushshift')

    comments_df = pd.DataFrame(comments)

    file = f'{before.strftime("%Y%m%d")}-{after.strftime("%Y%m%d")}-{subreddit}.json'

    comments_df.to_json(file)