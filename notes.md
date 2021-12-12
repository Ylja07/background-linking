# Notes

Note: Topics and qrels are already given

## What's happening:
- Reranker graph comparison based on doc
- Indexing (command can be found in README), sample index `Index/lucene-index.sample` already present
- Use database to speed up graph generation (`database_utils/build_db.py`), `db/sample.db` already present
- Obtain candidates using BM25 + RM3 via Anserini, `candidates/candidates.sample.txt` already present
- Use word embeddings for graph creation to initialize edges (download link can be found in README)
- For every candidate document create a graph to compute similarity score
- Simply sort the documents according to this score and diversify them 
(if a ranked document contains many entities with type `person`, consecutive documents which focus on these entities are discarded),
this ranking is written to the results file

## Generating candidates
Pepijn mentions "Candidates were obtained using BM25 + RM3 via Anserini, see https://github.com/castorini/anserini/blob/master/docs/regressions-backgroundlinking19.md."  
To replicate this, we had to do the following:
- Clone the Anserini repo (I just downloaded it as ZIP)
- Download Maven and add the /bin folder to PATH
- In the Anserini directory, add the following plugin to the `pom.xml`:
  ```xml
  <plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-surefire-plugin</artifactId>
    <version>2.19.1</version>
    <configuration>
      <testFailureIgnore>true</testFailureIgnore>
    </configuration>
  </plugin>
  ```
- Build Anserini with `mvn clean package appassembler:assemble -DskipTests`
- Set the `JAVA_HOME` environment variable to the java path, in my case "C:\Program Files\Java\jdk-17", but of course this depends on the Java version. I think it's supposed to be a system variable, but I just added it to my user variables.
- Ensure that the command `echo %JAVA_HOME%` correctly returns this path. In my case this did not work in Powershell, but it did work in cmd, so I used cmd for the next step
- While in the `bglinking/resources` folder of our project repo, run
```
start Anserini_path/target/appassembler/bin/SearchCollection \
-index Index/lucene-index.sample \
-topicreader BackgroundLinking \
-topics topics-and-qrels/topics.sample.txt \
-output runs/run.sample.bm25+rm3.topics.sample.txt \
-backgroundlinking -backgroundlinking.k 100 -bm25 -rm3 -hits 100
```

## Word embeddings
- Generated using GEER (https://github.com/informagi/GEEER)
- Can be downloaded from https://surfdrive.surf.nl/files/index.php/s/V2mc4zrcE46Ucvs (2.7GB tar)
- Loaded at `reranker.py` line 178, Used in the `initialize_edges` function of `DefaultGraphBuilder` to compute term similarity.

## Database
A database was created to speed up the graph generation.
Named entities and tf-idf terms were stored per candidate document in a database.
To generate a sample database, I had to do the following:
- Install all packages (I created a new `bglinking` conda environment for this)
- Move/copy all files from the `database_utils` and `general_utils` to a common `utils` folder
- Fix the imports in `build_db.py` and `utils.py` (Pepijn used i.e. `from bglinking.database_utils import db_utils`, I changed this to simply `import db_utils` since the package approach didn't seem to work).
- Add the `C:\Program Files\Java\jdk-17\bin\server` to PATH to fix an error from `PyJNIus`
- While in the `bglinking/utils` folder, using cmd for the same reason as above, run
```
python build_db.py \
--index lucene-index.sample \
--name test \
--candidates candidates.sample.txt \
--topics topics.sample.txt
```
- This resulted in the creation of `resources/db/test.db`, which does not look the same as `sample.db`..

## Workflow for "real" data
I'll run these commands from the `bglinking/resources` folder, unless otherwise specified.

### Indexing
```
start C:/Users/mika/Documents/Radboud/Courses/Master_Year_1/Information_Retrieval/Project/anserini-master/target/appassembler/bin/IndexCollection \
 -collection WashingtonPostCollection \
 -input C:/Users/mika/Documents/Radboud/Courses/Master_Year_1/Information_Retrieval/Project/WashingtonPost.v3/data \
 -index Index/lucene-index.core18.pos+docvectors+rawdocs_all \
 -generator WashingtonPostGenerator \
 -threads 1 -storePositions -storeDocvectors -storeRaw -optimize -storeContents
```
This indexes 671.945 documents, which took about 13 minutes on my machine, and generates the `lucene-index.core18.pos+docvectors+rawdocs_all` folder inside the `bglinking/resources/Index` folder.

### Generating candidates
<!-- ```
start C:/Users/mika/Documents/Radboud/Courses/Master_Year_1/Information_Retrieval/Project/anserini-master/target/appassembler/bin/SearchCollection \
-index Index/lucene-index.core18.pos+docvectors+rawdocs_all \
-topicreader BackgroundLinking \
-topics topics-and-qrels/topics.backgroundlinking19.txt \
-output runs/run.backgroundlinking19.bm25+rm3.topics.backgroundlinking19.txt \
-backgroundlinking -backgroundlinking.k 100 -bm25 -rm3 -hits 100
``` 

This resulted in an exception:
```
2021-12-12 12:17:53,914 ERROR [pool-2-thread-1] search.SearchCollection$SearcherThread (SearchCollection.java:274) - pool-2-thread-1: Unexpected Exception:
java.lang.IllegalArgumentException: docID must be >= 0 and < maxDoc=671945 (got docID=-1)
        at org.apache.lucene.index.BaseCompositeReader.readerIndex(BaseCompositeReader.java:189)
.....
```

After a while I realized this is probably caused by a mismatch in the used corpus.
Pepijn notes that "note that we used version 2 of the corpus for the 2019 topics, and version 3 for the 2020 topics", while the 18 and 19 topics are present in his repository.
And since we are using version 3 of the corpus, I suppose some of the 2019 topics refer to docids that are not present in our corpus.
So I downloaded the 2020 topics from TREC and am now using these instead.
-->
```
start C:/Users/mika/Documents/Radboud/Courses/Master_Year_1/Information_Retrieval/Project/anserini-master/target/appassembler/bin/SearchCollection \
-index Index/lucene-index.core18.pos+docvectors+rawdocs_all \
-topicreader BackgroundLinking \
-topics topics-and-qrels/topics.backgroundlinking20.txt \
-output runs/run.backgroundlinking20.bm25+rm3.topics.backgroundlinking20.txt \
-backgroundlinking -backgroundlinking.k 100 -bm25 -rm3 -hits 100
```
This generates the `run.backgroundlinking20.bm25+rm3.topics.backgroundlinking20.txt` file inside the  `bglinking/resources/runs` folder.  
This file has to manually be copied to the `bglinking/resources/candidates` folder and renamed to `candidates.backgroundlinking20.txt` for the next step.

### Generating database with word embeddings
This command must be executed from the `bglinking/utils` folder, since the paths are processed relative to there in `build_db.py`:
```
python build_db.py \
--index lucene-index.core18.pos+docvectors+rawdocs_all \
--name entity_database_20 \
--candidates candidates.backgroundlinking20.txt \
--topics topics.backgroundlinking20.txt
```
Other possible arguments are `--extractor rel` (or spacy), `--topics-only False`, `-n 100`, `--cut 9999999` but these default values seem fine. 

On my machine, it took an estimated 90 seconds per iteration, and there would be a total of 4935 iterations.. meaning it would take $4935*90=444150$ seconds, 123.375 hours, to complete the database creation.  
So instead, I filtered the candidates by storing the top 5 candidates for 10 random topics using `filter_candidates.py` and stored these in the `candidates_filtered.backgroundlinking20.txt` file which I used instead.

Database creation can result in an error:
```
Traceback (most recent call last):
  File "build_db.py", line 126, in <module>
    rel_request = requests.post(
  File "C:\Users\mika\anaconda3\envs\bglinking\lib\site-packages\requests\models.py", line 898, in json
    return complexjson.loads(self.text, **kwargs)
  File "C:\Users\mika\anaconda3\envs\bglinking\lib\json\__init__.py", line 357, in loads
    return _default_decoder.decode(s)
  File "C:\Users\mika\anaconda3\envs\bglinking\lib\json\decoder.py", line 337, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
  File "C:\Users\mika\anaconda3\envs\bglinking\lib\json\decoder.py", line 355, in raw_decode
    raise JSONDecodeError("Expecting value", s, err.value) from None
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

I'm not sure whether this is simply bad error handling, or if it was caused by me moving things around, I suppose the former.  
It does not seem to be consistent.  
In the end, I ended up with an `entity_database_20.db` file in the `bglinking/resources/db` folder containing 15 docids, so I removed all candidates which reference docids that are not in the database from the `candidates_filtered.backgroundlinking20.txt` file using `remove_invalid_docids.py`, and stored the result in the `candidates_final.backgroundlinking20.txt` file.

## Todo
- Ensure that paragraph information is still present
- Create graphs for every paragraph? Then assign a score to these paragraphs to weight the graphs and combine them into a single document graph again
- Experiment with different graph configurations (docker)

- Print / visualize created graph
- Print available information

## Questions for Chris
None at the moment