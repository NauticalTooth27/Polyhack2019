import nltk
from nltk.corpus import stopwords
from collections import Counter
import math
import string

from sklearn.cluster import KMeans
import numpy as np


NUM_KEYWORDS = 15

# Bias indices
LEFT = 0
CENTER = 1
RIGHT = 2

# Source biases
SOURCE_BIASES = {"Time":LEFT, "The Huffington Post":LEFT, "Politico":LEFT, "ABC News":CENTER, "Fox News":RIGHT, "The Hill":CENTER}

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
        word_tokens = [word_tokenizer.word_tokenize(sent.lower()) for sent in sent_tokens]
        tokens = []
        for wt in word_tokens :
            # for w in wt :
            #     w = w.strip(string.punctuation)
            tokens.extend(wt)
        tokens = [lemmatizer.lemmatize(token).strip(string.punctuation + "–—“’") for token in tokens if token not in stop_words and token not in string.punctuation + "–—“’ "]
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
    kmeans = KMeans(n_clusters=3).fit(data)
    print(kmeans.labels_)
    return kmeans

def euclidean_distance(v1, v2) :
    assert(len(v1) == len(v2))
    sum = 0
    for i in range(len(v1)) :
        sum += (v1[i] - v2[i]) ** 2


def get_nearest_other_bias(data, target_doc, doc_sources, bias=CENTER) :

    low_dist = -1
    low_dist_idx = -1

    for idx in data :
        if not SOURCE_BIASES[doc_sources[idx]] == bias :
            continue
        if low_dist == -1 :
            low_dist = euclidean_distance(data[idx], target_doc)
            low_dist_idx = idx
    if low_dist_idx == -1 :
        return None
    else :
        return low_dist_idx


    #######

docs = [""] * 15
for i in range(15) :
	with open("../../resources/sample_documents/document{}.txt".format(i)) as f :
		docs[i] = f.read()

doc_vecs, word_list = keywordify(docs)
cluster_docs(doc_vecs, word_list)
