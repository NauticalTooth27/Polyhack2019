import nltk
from nltk.corpus import stopwords
from collections import Counter
from collections import defaultdict
import math
import string

from sklearn.cluster import DBScan

import numpy as np

from nltk.sentiment.vader import SentimentIntensityAnalyzer


NUM_KEYWORDS = 10

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

    sentiments = [None] * num_docs

    # Clean and tokenize all docs
    for doc_idx in range(num_docs) :
        sent_tokens = tokenizer.tokenize(documents[doc_idx].strip())
        sentiments[doc_idx] = get_sentiment(sent_tokens)
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

    return doc_vecs, word_list, sentiments

def euclidean_distance(v1, v2) :
    assert(len(v1) == len(v2))
    sum = 0
    for i in range(len(v1)) :
        sum += (v1[i] - v2[i]) ** 2



# Deprecated - doc_sources passed differently
# def get_nearest_other_bias(data, target_doc, doc_sources, bias=CENTER) :

    # low_dist = -1
    # low_dist_idx = -1
    #
    # for idx in data :
    #     if not SOURCE_BIASES[doc_sources[idx]] == bias :
    #         continue
    #     if low_dist == -1 :
    #         low_dist = euclidean_distance(data[idx], target_doc)
    #         low_dist_idx = idx
    # if low_dist_idx == -1 :
    #     return None
    # else :
    #     return low_dist_idx



def get_sentiment(tokenized_sentences) :
    sid = SentimentIntensityAnalyzer()
    total_scores = defaultdict(float)

    for sentence in tokenized_sentences :
        scores = sid.polarity_scores(sentence)
        for key in scores :
            total_scores[key] += scores[key]

    compound = total_scores['compound']

    if compound > 0.75 :
        return "Very positive"
    elif compound > 0.25 :
        return "Rather positive"
    elif compound > -0.25 :
        return "Fairly neutral"
    elif compound > -0.75 :
        return "Rather negative"
    else :
        return "Very negative"


# Returns a list of shared keywords between at least one doc vector - if the
#   vectors share no words, a list with just the empty string is returned.
def get_shared_keywords(doc_vecs, word_list) :
    shared = []
    vec_length = len(doc_vecs[0])
    for vec in doc_vecs :
        if not len(vec) == vec_length :
            return [""]

    for i in range(vec_length) :
        target = True if doc_vecs[0][i] > 0 else False
        for j in range(len(doc_vecs)) :
            curr_val = True if doc_vecs[j][i] > 0 else False
            if not curr_val == target :
                break

        shared.append(word_list[i])
    return shared


##### New Deal #####

def cluster_docs(data, word_list) :
    data = np.array(data)
    dbscan = DBScan().fit(data)
    labels = dbscan.labels

    num_clusters = max(labels)
    cluster = np.empty([num_clusters, 1])   # This might not work

    for doc_idx in range(len(data)) :
        if labels[doc_idx] == -1 :
            continue
        cluster[ labels[doc_idx] ].append(doc_idx)

    return cluster


# Takes list of doc indices from cluster_docs, returns three lists sorted by bias from doc_sources
def partition(doc_indices, doc_sources) :
    biases = [[], [], []]   # 0 = left, 1 = center, 2 = right

    for idx in doc_indices :
        biases[doc[sources[idx]]].append(idx)

    return biases


# def medoid(v1, v2) :
#     dist_matrix = np.zeros((len(v1), len(v2)))
#     for i in range(len(v1) - 1) :
#         for j in range(i + 1, len(v2)) :
#             coord_1 = (v1[i], v2[i])
#             ""
#             dist_matrix[i, j] = distance(coord1, coord2)
#             dist_matrix[j, i] = distance[j, i] = dist_matrix[i, j]
#     medoid_index = np.argmin(dist_matrix.sum(axis=0))
#     medoid = ( lat[medoid_index], long[medoid_index] )
#     return medoid

def medoid(doc_indices, data) :
    dist_matrix = np.zeros(len(doc_indices), len(doc_indices))
    for i in range(len(doc_indices) - 1) :
        for j in range(i + 1, len(doc_indices)) :
            doc_1 = data[i]
            doc_2 = data[j]
            dist_matrix[i, j] = euclidean_distance(doc_1, doc_2)
            dist_matrix[j, i] = dist_matrix[i, j]
    medoid_index = np.argmin(dist_matrix.sum(axis=0))
    medoid = doc_indices[medoid_index]
    return medoid


## RUN THIS ##
def docs_to_biased(document_texts, doc_sources) :

    doc_vecs, word_list, sentiments = keywordify(document_texts)

    clusters = cluster_docs(doc_vecs, word_list)
    result = np.empty(len(clusters))
    for topic_idx in range(len(clusters)) :
        biases = partition(clusters[topic_idx])
        meds = [medoid(biases[0], doc_vecs), medoid(biases[1], doc_vecs), medoid(biases[2], doc_vecs)]
        for i in range(len(meds)) :
            meds[i] = (meds[i], sentiments[meds[i]])
        result[topic_idx] = meds
    return result


    #######

docs = [""] * 15
for i in range(15) :
	with open("../../resources/sample_documents/document{}.txt".format(i)) as f :
		docs[i] = f.read()

doc_vecs, word_list, sentiment = keywordify(docs)
cluster_docs(doc_vecs, word_list)




# Citations:
# Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for
#   Sentiment Analysis of Social Media Text. Eighth International Conference on
#   Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.
#
#
