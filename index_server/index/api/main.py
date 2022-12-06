"""REST API for index server."""
import re
from pathlib import Path
from math import sqrt
from flask import jsonify, request
from index.api.utils import InvalidUsage
import index


# In-memory data for inverted_index, stopwords, and pagerank
WORD_IDF = {}  # word -> idf
WORD_OCCURENCE = {}  # word -> (map(doc_id) -> (freq, norm_factor))
STOPWORDS = []
PAGERANK = {}


def load_index():
    """Load inverted index, stopwords, and pagerank into memory."""
    index_path = Path('index_server/index/inverted_index') /\
        index.app.config['INDEX_PATH']
    stopwords_path = Path('index_server/index/stopwords.txt')
    pagerank_path = Path('index_server/index/pagerank.out')

    with open(index_path, 'r', encoding='utf-8') as index_file:
        for line in index_file:
            vals = line.split()
            word = vals[0]
            doc_id, freq, norm_factor = int(vals[2]), \
                float(vals[3]), float(vals[4])
            WORD_IDF[word] = float(vals[1])
            WORD_OCCURENCE[word] = {}
            WORD_OCCURENCE[word][doc_id] = (freq, norm_factor)
            vals = vals[5:]
            while len(vals) > 0:
                doc_id, freq, norm_factor = int(vals[0]), \
                    float(vals[1]), float(vals[2])
                WORD_OCCURENCE[word][doc_id] = (freq, norm_factor)
                vals = vals[3:]

    with open(stopwords_path, 'r', encoding='utf-8') as stopwords_file:
        for line in stopwords_file:
            STOPWORDS.append(line.rstrip())

    with open(pagerank_path, 'r', encoding='utf-8') as pagerank_file:
        for line in pagerank_file:
            [docid, rank] = line.split(',')
            PAGERANK[int(docid)] = float(rank)


@index.app.route('/api/v1/', methods=['GET'])
def get_main():
    """Return a list of services available."""
    context = {
        "hits": "/api/v1/hits/",
        "url": "/api/v1/"
    }
    print(len(WORD_IDF), len(STOPWORDS), len(PAGERANK))
    return jsonify(**context)


@index.app.route('/api/v1/hits/', methods=['GET'])
def get_hits():
    """Return a list of hits with doc ID and score."""
    query = request.args.get('q', type=str)
    weight = request.args.get('w', default=0.5, type=float)
    if weight < 0. or weight > 1.:
        raise InvalidUsage('Bad Request', status_code=400)

    query_words = []
    if query is not None:
        # "+" automatically converted to " " in query
        query = re.sub(r"[^a-zA-Z0-9 ]+", "", query)
        query = query.casefold()
        # convert to list of strings
        query_words = query.split()
        # eliminate stopwords
        query_words = [word for word in query_words if word not in STOPWORDS]

    # find hits:
    # set {hit_doc_id} = intersection of set {Qi_doc_id},
    # where Qi is the i-th entry of query words.
    context = {
        "hits": [],
    }

    hit_docs = set()
    if len(query_words) > 0:
        if query_words[0] in WORD_OCCURENCE:
            hit_docs = set(WORD_OCCURENCE[query_words[0]].keys())
            idx = 1
            while idx < len(query_words) and len(hit_docs) > 0:
                # break if empty set
                if query_words[idx] in WORD_OCCURENCE:
                    hit_docs = hit_docs & \
                        set(WORD_OCCURENCE[query_words[idx]].keys())
                else:  # intersection with empty set
                    hit_docs = set()
                idx += 1
        # compute score for each doc
        query_tf = compute_freq(query_words)
        for docid in hit_docs:
            score = compute_score(query_words, query_tf, docid, weight)
            context['hits'].append({"docid": docid, "score": score})

        # sort with descending score
        context['hits'].sort(key=(lambda elem: elem['score']), reverse=True)

    # context['num_hits'] = len(context['hits']) # debug print

    # context = {
    #     "query": query_words
    # }

    return jsonify(**context)


def compute_freq(query_words):
    """Compute frequency for each word in the query string."""
    freq = {}
    for word in query_words:
        if word not in freq:
            freq[word] = 1
        else:
            freq[word] += 1
    return freq


def compute_score(query_words, query_tf, docid, weight):
    """Compute weighted tf-idf score for query and doc(docid)."""
    # compute [tf * idf] for each word in query_words
    dot_prod = 0.
    norm_q_squared = 0.
    norm_d_squared = 0.
    for word in query_words:
        query_tfidf = query_tf[word] * WORD_IDF[word]
        doc_tfidf = WORD_OCCURENCE[word][docid][0] * WORD_IDF[word]
        dot_prod += query_tfidf * doc_tfidf
        norm_q_squared += query_tfidf * query_tfidf
        norm_d_squared = WORD_OCCURENCE[word][docid][1]  # same for docid

    tfidf = dot_prod / (sqrt(norm_q_squared) * sqrt(norm_d_squared))
    return weight * PAGERANK[docid] + (1 - weight) * tfidf
