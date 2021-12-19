import csv
import sqlite3

project_root = 'C:/Users/mika/Documents/Radboud/Courses/Master_Year_1/Information_Retrieval/Project/background-linking-IR'
csv_in = "C:/Users/mika/Documents/Radboud/Courses/Master_Year_1/Information_Retrieval/Project/entity-doc/entity-doc.csv"
candidates = "{}/bglinking/resources/candidates/candidates.backgroundlinking20.txt".format(project_root)
topics = "{}/bglinking/resources/topics-and-qrels/topics.backgroundlinking20.txt".format(project_root)
db = "{}/bglinking/resources/db/entity_database_20.db".format(project_root)

allowed_docids = []

# Read all candidates and store all docids that are used
# with open(candidates, 'r') as file:
#     for line in file.readlines():
#         _,_,docid,_,_,_ = line.split(' ')
#         if docid not in allowed_docids:
#             allowed_docids += [docid]

#<top>
#  <num> Number: 886 </num>
#  <docid>AEQZNZSVT5BGPPUTTJO7SNMOLE</docid>
#  <url>https://www.washingtonpost.com/politics/2019/06/05/trump-says-transgender-troops-cant-serve-because-troops-cant-take-any-drugs-hes-wrong-many-ways/</url>
#</top>

# Read all topics and store all docids that are used
with open(topics, 'r') as file:
    for line in file.readlines():
        if "<docid>" in line:
            docid = line.split("<docid>")[1].split("</docid>")[0]            
            if docid not in allowed_docids:
                allowed_docids += [docid]

print("{} allowed docids".format(len(allowed_docids)))

conn = sqlite3.connect(db)
cursor = conn.cursor()

# Create database
# cursor.execute(
#     """CREATE TABLE "entities" (
#     "id"	    integer,
#     "pos"	    integer,
#     "len"	    integer,
#     "ref_text"	text,
#     "entity"	text,
#     "type"	    text,
#     "docid"	    text,
#     PRIMARY KEY("id"))"""
# )
# conn.commit()

docid_count = 0
with open (csv_in, 'r', encoding='Latin1') as f:
    reader = csv.reader(f,delimiter='|')
    data = next(reader)
    query = 'insert into entities (pos, len, ref_text, entity, type, docid) values ({0})'
    query = query.format(','.join('?' * len(data)))

    if data[5] in allowed_docids:
        docid_count+=1
        print("#{} Adding entities for docid {}".format(docid_count,data[5]))
        cursor.execute(query, data)

    cur_docid = data[5]

    for data in reader:
        # Only add entities for the docids that are used by the candidates
        if data[5] in allowed_docids:
            if data[5] != cur_docid:
                cur_docid = data[5]
                docid_count+=1
                print("#{} Adding entities for docid {}".format(docid_count,cur_docid))
            cursor.execute(query, data)
            conn.commit()
conn.close()