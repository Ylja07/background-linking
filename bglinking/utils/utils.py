import math
import re
from operator import itemgetter

import numpy as np
from bs4 import BeautifulSoup
import sqlite3

def connect_db(db_name: str):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    return conn, cursor

def prevent_zero(i):
    if i == 0:
        return 0.000000001
    else:
        return i

def normalize_dict(dictionary):
    max_rank = np.max(list(dictionary.values()))
    min_rank = np.min(list(dictionary.values()))
    for n, w in dictionary.items():
        dictionary[n] = (w - min_rank) / prevent_zero((max_rank - min_rank))
    return dictionary

def create_new_file_for_sure(file_name):
    """Temporary solution to make sure the file is newly created."""
    results_file = open(file_name, "w")
    results_file.close()

def resolve_tie(score, rank, last_score, dup):
    score = round(score, 6)
    if rank == 0 or (last_score - score) > 10 ** (-4):
        dup = 0
    else:
        dup += 1
        score -= 10 ** (-6) * dup
    return score, dup

def write_to_results_file(
    ranking: dict, query_num: str, run_tag: str, file_name: str, last_score=True
):
    """Write results to txt."""
    last_score = 0
    dup = 0
    results_file = open(file_name, "a")
    i = 0
    for rank, docid in enumerate(list(ranking.keys())):
        last_score, dup = resolve_tie(ranking[docid], rank, last_score, dup)
        results_file.write(
            f"{query_num} Q0 {repair_docid(docid)} {i+1} {last_score} {run_tag}\n"
        )
        i += 1
    results_file.close()

def tfidf(tf, df, N):
    return math.log((1.0 + N) / df) * tf

def create_top_n_tfidf_vector(
    index_utils, docid: str, n: int, t: int, total_N=595031
) -> dict:
    """Create list of top N terms with highest tfidf in a document
    accompanied with their tf."""
    # retrieve already analyzed terms in dict: tf
    tf = index_utils.get_document_vector(docid)

    # Filter terms: should not contain numbers and len >= 2.
    w_pattern = re.compile("[a-z]+")
    filtered_tf = {
        term: tf
        for term, tf in tf.items()
        if len(w_pattern.findall(term)) == 1
        and len(term.replace(".", "")) >= 2
        and re.search("[a-z]+", term)[0] == term
    }

    # df
    df = {
        term: (index_utils.get_term_counts(term, analyzer=None))[0]
        for term in filtered_tf.keys()
    }

    # calcute tfidf for each term and store in dict.
    terms_tfidf = {
        term: tfidf(tf[term], df[term], total_N)
        for term in filtered_tf.keys()
        if tfidf(tf[term], df[term], total_N) >= t
    }

    # Sort terms based on tfidf score.
    tfidf_terms_sorted = {
        term: tf[term]
        for term, tfidf in sorted(terms_tfidf.items(), key=itemgetter(1), reverse=True)[
            :n
        ]
    }

    return tfidf_terms_sorted

def repair_docid(docid: str):
    return re.sub("_PASSAGE[0-9]+", "", docid)

def read_topics_and_ids_from_file(file_path: str):
    topics = []
    with open(file_path) as f:
        content = f.read()
        soup = BeautifulSoup(content, features="lxml")
        for topic in soup.find_all("top"):
            num_string = topic.find("num").string
            num = [int(s) for s in num_string.split() if s.isdigit()]
            docid = topic.find("docid").string
            assert len(num) == 1, "Found more topic numbers for single topic.."
            topics.append([num[0], docid])
    return topics
