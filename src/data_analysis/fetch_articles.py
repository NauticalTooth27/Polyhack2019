from requests_html import HTMLSession
# IMPORTANT - use websockets==6.0 (not more recent version)
import os
import random
import numpy as np
import sqlite3
from newsapi import NewsApiClient
from multiprocessing import Pool

# Set constants
NEWS_API_KEY = "8ff68b63c768444394d75e5ab45cd3a6"#os.environ["NEWS_API_KEY"]
NUM_PROC = 8
NUM_SAMPLES_PER_SOURCE = 2

newsapi = NewsApiClient(api_key=NEWS_API_KEY)
conn = sqlite3.connect("documents.db")
c = conn.cursor()
c.execute('''CREATE TABLE documents(label text, title text, source text, url text,
             author text, description text, content text)''')
conn.commit()

'''
1. Get list of news from newsapi
2. Filter list for only correct things
3. For each url, render and parse the content
'''

all_sources = ["the-huffington-post", "politico", "abc-news", "fox-news", "the-hill", "time"]
source2content = {
"the-huffington-post": ".content-list-component",
"politico": ".story-text__paragraph",
#"slate": ".slate-paragraph",
"abc-news": "[itemprop=articleBody]",
"fox-news": ".article-body",
"the-hill": ".field-item",
#"westernjournal": ".entry-content",
"time": "#article-body"
}

select_p_after = {"westernjournal", "time"}

def get_content(url, source):
    session = HTMLSession()
    print("Rendering: ", url)
    r = session.get(url)
    r.html.render()
    content = ""
    for elem in r.html.find(source2content[source]):
        if source in select_p_after:
            for text_elem in elem.find("p"):
                content += text_elem.text
        else:
            content += elem.text

    print("        ", content[:20])
    return content

def articles_about_subject(subject):
    documents = list()
    articles = list()
    for source in all_sources:
        top_headlines = newsapi.get_everything(sources = source, q = subject)

        if not top_headlines["articles"]:
            print("None found: ", subject, source)
            continue

        ordered_articles = np.random.permutation(np.array(top_headlines["articles"]))
        sample_size = min(len(ordered_articles), NUM_SAMPLES_PER_SOURCE)
        ordered_articles = ordered_articles[:sample_size]
        print(ordered_articles[0])
        p = Pool(NUM_PROC)
        content_list = p.starmap(save_article, [(article, subject) for article in ordered_articles])

def save_article(article, label):
    url = article["url"]
    source = article["source"]["id"]
    try:
        content = get_content(url, source)
        if content:
            save_to_db(article, content, label)
    except Exception as e:
        print("    ERROR: ", url)
        print("    ",e)

def save_to_db(article, content, label):
    title = article["title"]
    source = article["source"]["name"]
    url = article["url"]
    author = article["author"]
    description = article["description"]
    c.execute("INSERT INTO documents(label, title, source, url, author, description, content) VALUES (?, ?, ?, ?, ?, ?, ?)", (label, title, source, url, author, description, content))
    conn.commit()

def sample():
    articles_about_subject("Giuliani")
    articles_about_subject("impeachment")
    articles_about_subject("Turkey")
    articles_about_subject("Hong Kong")

def all_articles():
    filtered_articles = list()
    for source in all_sources:
        top_headlines = newsapi.get_everything(sources = source, pageSize = 100)

    documents = list()
    for article in filtered_articles:
        url = article["url"]
        source = article["source"]["id"]
        content = get_content(url, source)
        documents.append(content)

    return documents

sample()
conn.commit()
conn.close()