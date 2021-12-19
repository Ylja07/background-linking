import argparse
import os

from utils import utils, db_utils
from pyserini import index, analysis
from pyserini.search import SimpleSearcher
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument(
    "--index",
    dest="index",
    default="lucene-index.core18.pos+docvectors+rawdocs_all",
    help="specify the corpus index",
)

parser.add_argument(
    "--db", dest="db", default="entity_database_20.db", help="specify the database"
)

parser.add_argument(
    "--topics",
    dest="topics",
    default="topics.backgroundlinking20.txt",
    help="specify qrels file",
)

parser.add_argument(
    "--candidates",
    dest="candidates",
    default="run.backgroundlinking20.bm25+rm3.topics.backgroundlinking20.txt",
    help="Results file that carries candidate docs",
)

parser.add_argument(
    "--qrels",
    dest="qrels",
    default="qrels.backgroundlinking20.txt",
    help="specify qrels file",
)

parser.add_argument(
    "--output", dest="output", default="output_graph.txt", help="specify output file"
)

parser.add_argument(
    "--run-tag", dest="run_tag", default="unspecified_run_tag", help="specify run tag"
)

parser.add_argument("--stats", dest="stats", default=False, help="Show index stats")

parser.add_argument(
    "--use-entities",
    dest="use_entities",
    default=False,
    action="store_true",
    help="Use entities in addition to tf-idf",
)

parser.add_argument(
    "--nr-terms",
    dest="nr_terms",
    default=100,
    type=int,
    help="Number of tf-idf terms to keep track of",
)

parser.add_argument(
    "--nr-results",
    dest="nr_results",
    default=100,
    type=int,
    help="Number of results to be returned by the Anserini searcher",
)

parser.add_argument(
    "--xor",
    dest="xor",
    default=False,
    action="store_true",
    help="Use only entities when these are found, else tf-idf",
)

parser.add_argument(
    "--entities-stemming",
    dest="entities_stemming",
    default=False,
    action="store_true",
    help="Use stemming in the lucene analyzer for the entities",
)
parser.add_argument(
    "--entities-stopwords",
    dest="entities_stopwords",
    default=False,
    action="store_true",
    help="Filter out stopwords in the lucene analyzer for the entities",
)
parser.add_argument(
    "--entities-unique",
    dest="entities_unique",
    default=False,
    action="store_true",
    help="Filter out duplicate entities",
)
parser.add_argument(
    "--entities-noref",
    dest="entities_noref",
    default=False,
    action="store_true",
    help="Get the actual entity instead of the ref text",
)

args = parser.parse_args()

print(f"\nIndex: resources/Index/{args.index}")
print(f"Topics were retrieved from resources/topics-and-qrels/{args.topics}")
print(f"Results are stored in resources/output/runs/{args.output}\n")
utils.create_new_file_for_sure(f"resources/output/{args.output}")

conn, cursor = db_utils.connect_db(f"resources/db/{args.db}")

# Load index
index_utils = index.IndexReader(f"resources/Index/{args.index}")
searcher = SimpleSearcher(f"resources/Index/{args.index}")
analyzer_nostem = analysis.Analyzer(analysis.get_lucene_analyzer(stemming=False, stopwords=False))
#analyzer = analysis.Analyzer(analysis.get_lucene_analyzer())
analyzer = analysis.Analyzer(analysis.get_lucene_analyzer(stemming=args.entities_stemming, stopwords=args.entities_stopwords))
collection_length = index_utils.stats()["total_terms"]

# Read topics
topics = utils.read_topics_and_ids_from_file(f"resources/topics-and-qrels/{args.topics}")

for topic_num, topic_docid in tqdm(topics):

    # Calculate top 100 (by default) tf-idfs for the query doc
    tf_idfs_query = utils.create_top_n_tfidf_vector(index_utils, topic_docid, args.nr_terms, 0, total_N=collection_length)
    query = " ".join(tf_idfs_query.keys())

    if args.use_entities:
        # Get entities for query doc

        if args.entities_noref:
            # Get actual entity
            cursor.execute( """
                            SELECT entity FROM entities WHERE docid="{}"
                            """.format(topic_docid)
            )
        else:
            # Get text referring to entity
            cursor.execute( """
                            SELECT ref_text FROM entities WHERE docid="{}"
                            """.format(topic_docid)
            )
        query_entities = cursor.fetchall()

        if len(query_entities) != 0:
            if args.entities_unique:
                query_entities = set(query_entities)

            entities_string = " ".join(i[0] for i in query_entities)

            if args.entities_noref:
                entities_string = entities_string.replace("_"," ")
            
            analyzed_entities = " ".join(analyzer.analyze(entities_string))

            if args.xor:
                query = analyzed_entities
            else:
                query += " " + analyzed_entities
    
    # Create new ranking.
    ranking = {}

    # Search the collection using the constructed query
    hits = searcher.search(query, args.nr_results)
    for h in hits:
        ranking[h.docid] = h.score
    
    # Sort retrieved documents according to new similarity score.
    sorted_ranking = utils.normalize_dict(
        {
            k: v
            for k, v in sorted(ranking.items(), key=lambda item: item[1], reverse=True)
        }
    )

    # Store results in txt file.
    utils.write_to_results_file(
        sorted_ranking, str(topic_num), args.run_tag, f"resources/output/{args.output}"
    )

# Evaluate performance with trec_eval.
os.system(
    (
        "/opt/anserini-tools/eval/trec_eval.9.0.4/trec_eval -c -M1000 -m map"
        f" -m ndcg_cut -m P.10 resources/topics-and-qrels/{args.qrels}"
        f" resources/output/{args.output}"
    )
)
