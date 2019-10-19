from goose3 import Goose
import os
import random
import numpy as np
import sqlite3
from newsapi import NewsApiClient
from multiprocessing import Pool

NEWS_API_KEY = os.environ["NEWS_API_KEY"]
NUM_PROC = 2
NUM_SAMPLES_PER_SOURCE = 5

all_sources = ["cnn", "the-new-york-times", "time", "the-huffington-post", "politico",
               "bbc-news", "the-hill", "the-wall-street-journal", "reuters", "usa-today",
               "fox-news", "the-washington-times", "the-american-conservative", "daily-mail", "breitbart-news"]

newsapi = NewsApiClient(api_key=NEWS_API_KEY)
conn = sqlite3.connect("documents.db")
c = conn.cursor()
c.execute('''CREATE TABLE documents(label text, title text, source text, url text,
             author text, description text, content text)''')
conn.commit()

def get_content(url):
    g = Goose()
    article = g.extract(url = url)
    print("    ",article.title)
    return article.cleaned_text

def save_to_db(article, content, label):
    title = article["title"]
    source = article["source"]["name"]
    url = article["url"]
    author = article["author"]
    description = article["description"]
    c.execute("INSERT INTO documents(label, title, source, url, author, description, content) VALUES (?, ?, ?, ?, ?, ?, ?)", (label, title, source, url, author, description, content))
    conn.commit()

def save_article(article, label):
    url = article["url"]
    source = article["source"]["id"]
    print("SOURCE:", source)
    try:
        content = get_content(url)
        if content:
            save_to_db(article, content, label)
    except Exception as e:
        print("    ERROR: ", url)
        print("    ",e)

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
        with Pool(NUM_PROC) as p:
            content_list = p.starmap(save_article, [(article, subject) for article in ordered_articles])

def sample():
    articles_about_subject("Giuliani")
    articles_about_subject("impeachment")
    articles_about_subject("Turkey")
    articles_about_subject("Hong Kong")

sample()