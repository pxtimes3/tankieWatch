import json
import os

bannedAuthors = ["AutoModerator", "[deleted]", "SnapshillBot"]
uniqueAuthors = {}

directory = r'.'
for entry in os.scandir(directory):
    if (entry.path.endswith("shitWehraboosSay.json")):
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

for i in uniqueAuthors:
	print(i[0], i[1])

print(f'Total # of comment authors: {len(uniqueAuthors)}')