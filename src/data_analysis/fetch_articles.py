from requests_html import HTMLSession
# IMPORTANT - use websockets==6.0 (not more recent version)
import os
import random
from newsapi import NewsApiClient

# Set constants
NEWS_API_KEY = os.environ["NEWS_API_KEY"]


newsapi = NewsApiClient(api_key=NEWS_API_KEY)

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
"abc-news": ".article-body",
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
    filtered_articles = list()
    for source in all_sources:
        top_headlines = newsapi.get_everything(sources = source, q = subject)
        if not top_headlines["articles"]:
            print("None found: ", subject, source)
            continue
        filtered_articles.append(random.choice(top_headlines["articles"]))

    documents = list()
    for article in filtered_articles:
        url = article["url"]
        source = article["source"]["id"]
        content = get_content(url, source)
        documents.append(content)

    return documents

documents = articles_about_subject("Giuliani")
documents.extend(articles_about_subject("impeachment"))
documents.extend(articles_about_subject("Turkey"))

for i in range(len(documents)):
    with open("../../resources/sample_documents/document{}.txt".format(i), "w+") as file:
        print(documents[i])
        file.write(documents[i])