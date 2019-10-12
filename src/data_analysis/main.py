import sqlite3

# Grab stuff from database
# pass to ryan
# put output into database

DB_INPUT = "documents.db"
DB_OUTPUT = "../../webdev/db.sqlite3"

LEFT = 0
CENTER = 1
RIGHT = 2

input = sqlite3.connect(DB_INPUT)
c_input = input.cursor()

source2bias = {
"The Huffington Post":LEFT,
"Politico":LEFT,
"ABC News": CENTER,
"Fox News":RIGHT,
"The Hill":CENTER,
"Time":LEFT
}

bias = []
content = []
title = []
url = []
author = []
source = []
for row in c_input.execute("SELECT * from documents"):
    title_x, source_x, url_x, author_x, description_x, content_x = row
    bias.append(source2bias[source_x])
    content.append(content_x)

    title.append(title_x)
    url.append(url_x)
    author.append(author_x)
    source.append(source_x)

input.close()
print(bias)

topics = docs_to_bias(content, bias)

output = sqlite3.connect(DB_OUTPUT)
c = output.cursor()

for topic_id, topic in enumerate(topics):
    keywords = "Keywords"
    curr_date = "2019-10-12"
    c.execute("INSERT INTO newslisting_topic(id, keywords, pub_date) VALUES (?,?,?)", (topic_id, keywords, curr_date))

    left, center, right = topic
    for medoid in [left, center, right]:
        i, sentiment = medoid
        c.execute("""INSERT INTO newslisting_article(id, title, link, topic_id, author, sentiment, outlet)
                  VALUES (?,?,?,?,?,?,?)""", i, title[i], url[i], topic_id, author[i], sentiment, source[i])

output.commit()
output.close()