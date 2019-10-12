import nltk
from nltk.corpus import stopwords
from collections import Counter
import math

from sklearn.cluster import KMeans
import numpy as np


NUM_KEYWORDS = 15

# keywordify
# Takes list of N strings for documents
# Returns 2D, NxM list of string keywords; match up to articles
def keywordify(documents) :
    num_docs = len(documents)

    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    word_tokenizer = nltk.tokenize.punkt.PunktLanguageVars()
    lemmatizer = nltk.WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))

    term_freqs = [None] * num_docs
    all_freqs = Counter()
    keywords = [None] * num_docs

    # Clean and tokenize all docs
    for doc_idx in range(num_docs) :
        sent_tokens = tokenizer.tokenize(documents[doc_idx].strip())
        word_tokens = [word_tokenizer.word_tokenize(sent) for sent in sent_tokens]
        tokens = []
        for wt in word_tokens :
            tokens.extend(wt)
        tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]
        term_freqs[doc_idx] = Counter(tokens)
        all_freqs += term_freqs[doc_idx]

    idf = {}
    for term in all_freqs :
        idf[term] = math.log(num_docs / len([doc_idx for doc_idx in range(num_docs) if term_freqs[doc_idx][term] > 0]))

    # Calculate tfidfs for each term in each doc
    for doc_idx in range(num_docs) :
        tfidf = {}
        for term in term_freqs[doc_idx] :
            tfidf[term] = term_freqs[doc_idx][term] * idf[term]
        try :
            top_keys = sorted(tfidf, key=tfidf.get, reverse=True)[:NUM_KEYWORDS]
            keywords[doc_idx] = {k:tfidf[k] for k in top_keys}
        except :
            print("Error in except, keywordify 1")
            keywords[doc_idx] = tfidf

    doc_vecs = [None] * num_docs

    for doc_idx in range(num_docs) :
        word_dict = { term:0 for term in all_freqs}
        for term in keywords[doc_idx] :
            word_dict[term] = term_freqs[doc_idx][term]
        doc_vecs[doc_idx] = list(word_dict.values())

    word_list = list(all_freqs.keys())

    return doc_vecs, word_list


def cluster_docs(data, word_list) :
    data = np.array(data)
    kmeans = KMeans(n_clusters=6).fit(data)
    print(kmeans.labels_)
    return kmeans


    #######

docs = [""] * 15
for i in range(15) :
	with open("../../resources/sample_documents/document{}.txt".format(i)) as f :
		docs[i] = f.read()

doc_vecs, word_list = keywordify(docs)
cluster_docs(doc_vecs, word_list)
