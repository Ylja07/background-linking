# Baseline: tf-idf (100 terms)

```bash
docker run --rm -v $PWD/bglinking/resources:/opt/background-linking/bglinking/resources blimg_simple --index lucene-index.core18.pos+docvectors+rawdocs_all --db entity_database_20.db --topics topics.backgroundlinking20.txt --qrels qrels.backgroundlinking20.txt --candidates candidates.backgroundlinking20.txt --nr-terms 100 --output results_tfidf_100.txt --run-tag tfidf_100
```

```cmd
map                     all     0.2730
P_10                    all     0.5061
ndcg_cut_5              all     0.4177
ndcg_cut_10             all     0.4453
ndcg_cut_15             all     0.4561
ndcg_cut_20             all     0.4580
ndcg_cut_30             all     0.4664
ndcg_cut_100            all     0.5003
ndcg_cut_200            all     0.4930
ndcg_cut_500            all     0.4913
ndcg_cut_1000           all     0.4913
```

# Query expansion: use entities, use stemming & filter stopwords while analyzing

```bash
docker run --rm -v $PWD/bglinking/resources:/opt/background-linking/bglinking/resources blimg_simple --index lucene-index.core18.pos+docvectors+rawdocs_all --db entity_database_20.db --topics topics.backgroundlinking20.txt --qrels qrels.backgroundlinking20.txt --candidates candidates.backgroundlinking20.txt --nr-terms 100 --output results_entities.txt --run-tag entities --use-entities --entities-stemming --entities-stopwords
```

```cmd
map                     all     0.3320
P_10                    all     0.5735
ndcg_cut_5              all     0.4248
ndcg_cut_10             all     0.4691
ndcg_cut_15             all     0.4844
ndcg_cut_20             all     0.4957
ndcg_cut_30             all     0.5062
ndcg_cut_100            all     0.5333
ndcg_cut_200            all     0.5260
ndcg_cut_500            all     0.5244
ndcg_cut_1000           all     0.5244
```

# Query expansion: use entities, **don't** use stemming & don't filter stopwords while analyzing

```bash
docker run --rm -v $PWD/bglinking/resources:/opt/background-linking/bglinking/resources blimg_simple --index lucene-index.core18.pos+docvectors+rawdocs_all --db entity_database_20.db --topics topics.backgroundlinking20.txt --qrels qrels.backgroundlinking20.txt --candidates candidates.backgroundlinking20.txt --nr-terms 100 --output results_entities_nostem_nostop.txt --run-tag entities_nostem_nostop --use-entities
```

```cmd
map                     all     0.3345
P_10                    all     0.5755
ndcg_cut_5              all     0.4312
ndcg_cut_10             all     0.4721
ndcg_cut_15             all     0.4845
ndcg_cut_20             all     0.4977
ndcg_cut_30             all     0.5052
ndcg_cut_100            all     0.5358
ndcg_cut_200            all     0.5286
ndcg_cut_500            all     0.5270
ndcg_cut_1000           all     0.5270
```

# Query expansion: use **only** entities, use stemming & filter stopwords while analyzing

```bash
docker run --rm -v $PWD/bglinking/resources:/opt/background-linking/bglinking/resources blimg_simple --index lucene-index.core18.pos+docvectors+rawdocs_all --db entity_database_20.db --topics topics.backgroundlinking20.txt --qrels qrels.backgroundlinking20.txt --candidates candidates.backgroundlinking20.txt --nr-terms 100 --output results_entities_only.txt --run-tag entities_only --use-entities --entities-stemming --entities-stopwords --xor
```

```cmd
map                     all     0.2414
P_10                    all     0.4163
ndcg_cut_5              all     0.3363
ndcg_cut_10             all     0.3420
ndcg_cut_15             all     0.3500
ndcg_cut_20             all     0.3585
ndcg_cut_30             all     0.3637
ndcg_cut_100            all     0.3918
ndcg_cut_200            all     0.3874
ndcg_cut_500            all     0.3868
ndcg_cut_1000           all     0.3868
```

# Query expansion: use **actual entities instead of text referring to entities**, use stemming & filter stopwords while analyzing

```bash
docker run --rm -v $PWD/bglinking/resources:/opt/background-linking/bglinking/resources blimg_simple --index lucene-index.core18.pos+docvectors+rawdocs_all --db entity_database_20.db --topics topics.backgroundlinking20.txt --qrels qrels.backgroundlinking20.txt --candidates candidates.backgroundlinking20.txt --nr-terms 100 --output results_entities_actual.txt --run-tag entities_actual --use-entities --entities-stemming --entities-stopwords --entities-noref
```

```cmd
map                     all     0.3122
P_10                    all     0.5347
ndcg_cut_5              all     0.4154
ndcg_cut_10             all     0.4520
ndcg_cut_15             all     0.4674
ndcg_cut_20             all     0.4799
ndcg_cut_30             all     0.4913
ndcg_cut_100            all     0.5151
ndcg_cut_200            all     0.5083
ndcg_cut_500            all     0.5068
ndcg_cut_1000           all     0.5068
```

# Query expansion: use entities, use stemming & filter stopwords while analyzing, **filter out duplicate entities**

```bash
docker run --rm -v $PWD/bglinking/resources:/opt/background-linking/bglinking/resources blimg_simple --index lucene-index.core18.pos+docvectors+rawdocs_all --db entity_database_20.db --topics topics.backgroundlinking20.txt --qrels qrels.backgroundlinking20.txt --candidates candidates.backgroundlinking20.txt --nr-terms 100 --output results_entities_unique.txt --run-tag entities_unique --use-entities --entities-stemming --entities-stopwords --entities-unique
```

```cmd
map                     all     0.3138
P_10                    all     0.5510
ndcg_cut_5              all     0.4299
ndcg_cut_10             all     0.4590
ndcg_cut_15             all     0.4765
ndcg_cut_20             all     0.4899
ndcg_cut_30             all     0.4988
ndcg_cut_100            all     0.5233
ndcg_cut_200            all     0.5160
ndcg_cut_500            all     0.5143
ndcg_cut_1000           all     0.5143
```

# Baseline: tf-idf (50 terms)

```bash
docker run --rm -v $PWD/bglinking/resources:/opt/background-linking/bglinking/resources blimg_simple --index lucene-index.core18.pos+docvectors+rawdocs_all --db entity_database_20.db --topics topics.backgroundlinking20.txt --qrels qrels.backgroundlinking20.txt --candidates candidates.backgroundlinking20.txt --nr-terms 50 --output results_tfidf_50.txt --run-tag tfidf_50
```

```cmd
map                     all     0.3208
P_10                    all     0.5551
ndcg_cut_5              all     0.4573
ndcg_cut_10             all     0.4914
ndcg_cut_15             all     0.5041
ndcg_cut_20             all     0.5106
ndcg_cut_30             all     0.5221
ndcg_cut_100            all     0.5562
ndcg_cut_200            all     0.5479
ndcg_cut_500            all     0.5458
ndcg_cut_1000           all     0.5458
```

# Query expansion: use entities, use stemming & filter stopwords while analyzing (50 tf-idf terms)

```bash
docker run --rm -v $PWD/bglinking/resources:/opt/background-linking/bglinking/resources blimg_simple --index lucene-index.core18.pos+docvectors+rawdocs_all --db entity_database_20.db --topics topics.backgroundlinking20.txt --qrels qrels.backgroundlinking20.txt --candidates candidates.backgroundlinking20.txt --nr-terms 50 --output results_entities_50.txt --run-tag entities_50 --use-entities --entities-stemming --entities-stopwords
```

```cmd
map                     all     0.3353
P_10                    all     0.5673
ndcg_cut_5              all     0.4174
ndcg_cut_10             all     0.4654
ndcg_cut_15             all     0.4815
ndcg_cut_20             all     0.4863
ndcg_cut_30             all     0.4993
ndcg_cut_100            all     0.5313
ndcg_cut_200            all     0.5243
ndcg_cut_500            all     0.5228
ndcg_cut_1000           all     0.5228
```

# Query expansion: use entities, **don't** use stemming & don't filter stopwords while analyzing  (50 tf-idf terms)

```bash
docker run --rm -v $PWD/bglinking/resources:/opt/background-linking/bglinking/resources blimg_simple --index lucene-index.core18.pos+docvectors+rawdocs_all --db entity_database_20.db --topics topics.backgroundlinking20.txt --qrels qrels.backgroundlinking20.txt --candidates candidates.backgroundlinking20.txt --nr-terms 50 --output results_entities_nostem_nostop_50.txt --run-tag entities_nostem_nostop_50 --use-entities
```

```cmd
map                     all     0.3390
P_10                    all     0.5592
ndcg_cut_5              all     0.4203
ndcg_cut_10             all     0.4637
ndcg_cut_15             all     0.4829
ndcg_cut_20             all     0.4888
ndcg_cut_30             all     0.5003
ndcg_cut_100            all     0.5338
ndcg_cut_200            all     0.5268
ndcg_cut_500            all     0.5253
ndcg_cut_1000           all     0.5253
```