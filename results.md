Note: for background linking, we usually care most about the top 5 results, since this is usually the amount of background articles that's actually shown to the user.  
In these tests, the following evaluation measurements are used:
- P_K: Precision@K
- recall_K: Recall@K
- ndcg_cut_K: NDCG@K

Where the integer $K$ indicates that we look at the top $K$ documents.

# Baseline: tf-idf (100 terms)

```bash
docker run --rm -v $PWD/bglinking/resources:/opt/background-linking/bglinking/resources blimg_simple --run-tag tfidf_100
```

```cmd
P_5                     all     0.5429
P_10                    all     0.5061
recall_5                all     0.1273
recall_10               all     0.2003
ndcg_cut_5              all     0.4177
ndcg_cut_10             all     0.4453
```

# Baseline for query expansion: RM-3

```bash
docker run --rm -v $PWD/bglinking/resources:/opt/background-linking/bglinking/resources blimg_simple --run-tag rm3 --rm3
```

```cmd
P_5                     all     0.6122
P_10                    all     0.5816
recall_5                all     0.1494
recall_10               all     0.2396
ndcg_cut_5              all     0.4676
ndcg_cut_10             all     0.4942
```

# Query expansion: use entities, use stemming & filter stopwords while analyzing

```bash
docker run --rm -v $PWD/bglinking/resources:/opt/background-linking/bglinking/resources blimg_simple --run-tag entities --use-entities --entities-stemming --entities-stopwords
```

```cmd
P_5                     all     0.5755
P_10                    all     0.5735
recall_5                all     0.1246
recall_10               all     0.2438
ndcg_cut_5              all     0.4248
ndcg_cut_10             all     0.4693
```

# Query expansion: use entities, **don't** use stemming & don't filter stopwords while analyzing

```bash
docker run --rm -v $PWD/bglinking/resources:/opt/background-linking/bglinking/resources blimg_simple --run-tag entities_nostem_nostop --use-entities
```

```cmd
P_5                     all     0.5878
P_10                    all     0.5755
recall_5                all     0.1265
recall_10               all     0.2376
ndcg_cut_5              all     0.4312
ndcg_cut_10             all     0.4723
```

# Query expansion: use **only** entities, use stemming & filter stopwords while analyzing

```bash
docker run --rm -v $PWD/bglinking/resources:/opt/background-linking/bglinking/resources blimg_simple --run-tag entities_only --use-entities --entities-stemming --entities-stopwords --xor
```

```cmd
P_5                     all     0.4735
P_10                    all     0.4184
recall_5                all     0.1016
recall_10               all     0.1567
ndcg_cut_5              all     0.3347
ndcg_cut_10             all     0.3421
```

# Query expansion: use **actual entities instead of text referring to entities**, use stemming & filter stopwords while analyzing

```bash
docker run --rm -v $PWD/bglinking/resources:/opt/background-linking/bglinking/resources blimg_simple --run-tag entities_actual --use-entities --entities-stemming --entities-stopwords --entities-noref
```

```cmd
P_5                     all     0.5796
P_10                    all     0.5347
recall_5                all     0.1255
recall_10               all     0.2314
ndcg_cut_5              all     0.4154
ndcg_cut_10             all     0.4520
```

# Query expansion: use entities, use stemming & filter stopwords while analyzing, **filter out duplicate entities**

```bash
docker run --rm -v $PWD/bglinking/resources:/opt/background-linking/bglinking/resources blimg_simple --run-tag entities_unique --use-entities --entities-stemming --entities-stopwords --entities-unique
```

```cmd
P_5                     all     0.5837
P_10                    all     0.5510
recall_5                all     0.1359
recall_10               all     0.2200
ndcg_cut_5              all     0.4299
ndcg_cut_10             all     0.4590
```

# Query expansion: use entities, use stemming & filter stopwords while analyzing, **use top 10 entities**

```bash
docker run --rm -v $PWD/bglinking/resources:/opt/background-linking/bglinking/resources blimg_simple --run-tag entities_top10 --use-entities --entities-stemming --entities-stopwords --entities-top-amount 10
```

```cmd
P_5                     all     0.5796
P_10                    all     0.5571
recall_5                all     0.1344
recall_10               all     0.2277
ndcg_cut_5              all     0.4204
ndcg_cut_10             all     0.4674
```

# Query expansion: use entities, use stemming & filter stopwords while analyzing, **use top 20 entities**

```bash
docker run --rm -v $PWD/bglinking/resources:/opt/background-linking/bglinking/resources blimg_simple --run-tag entities_top20 --use-entities --entities-stemming --entities-stopwords --entities-top-amount 20
```

```cmd
P_5                     all     0.5878
P_10                    all     0.5633
recall_5                all     0.1381
recall_10               all     0.2466
ndcg_cut_5              all     0.4250
ndcg_cut_10             all     0.4715
```

# Query expansion: use entities, use stemming & filter stopwords while analyzing, **use top 5% entities**

```bash
docker run --rm -v $PWD/bglinking/resources:/opt/background-linking/bglinking/resources blimg_simple --run-tag entities_top5_percent --use-entities --entities-stemming --entities-stopwords --entities-top-percentage 5
```

```cmd
P_5                     all     0.5837
P_10                    all     0.5673
recall_5                all     0.1374
recall_10               all     0.2428
ndcg_cut_5              all     0.4274
ndcg_cut_10             all     0.4667
```

# Query expansion: use entities, **don't** use stemming & don't filter stopwords while analyzing, **use top 10 entities**

```bash
docker run --rm -v $PWD/bglinking/resources:/opt/background-linking/bglinking/resources blimg_simple --run-tag entities_nostem_nostop_top10 --use-entities --entities-top-amount 10
```

```cmd
P_5                     all     0.5837
P_10                    all     0.5612
recall_5                all     0.1357
recall_10               all     0.2292
ndcg_cut_5              all     0.4208
ndcg_cut_10             all     0.4687
```

# Query expansion: use entities, **don't** use stemming & don't filter stopwords while analyzing, **use top 20 entities**

```bash
docker run --rm -v $PWD/bglinking/resources:/opt/background-linking/bglinking/resources blimg_simple --run-tag entities_nostem_nostop_top20 --use-entities --entities-top-amount 20
```

```cmd
P_5                     all     0.5918
P_10                    all     0.5612
recall_5                all     0.1384
recall_10               all     0.2403
ndcg_cut_5              all     0.4284
ndcg_cut_10             all     0.4676
```

# Query expansion: use entities, **don't** use stemming & don't filter stopwords while analyzing, **use top 5% entities**

```bash
docker run --rm -v $PWD/bglinking/resources:/opt/background-linking/bglinking/resources blimg_simple --run-tag entities_top5_percent --use-entities --entities-top-percentage 5
```

```cmd
P_5                     all     0.5959
P_10                    all     0.5592
recall_5                all     0.1385
recall_10               all     0.2347
ndcg_cut_5              all     0.4351
ndcg_cut_10             all     0.4635
```

# Baseline: tf-idf (**50 terms**)

```bash
docker run --rm -v $PWD/bglinking/resources:/opt/background-linking/bglinking/resources blimg_simple --run-tag tfidf_50 --nr-tfidf-terms 50
```

```cmd
P_5                     all     0.5918
P_10                    all     0.5551
recall_5                all     0.1463
recall_10               all     0.2311
ndcg_cut_5              all     0.4573
ndcg_cut_10             all     0.4914
```

# Baseline for query expansion: RM-3 (**50 terms**)

```bash
docker run --rm -v $PWD/bglinking/resources:/opt/background-linking/bglinking/resources blimg_simple --run-tag rm3_50 --rm3 --nr-tfidf-terms 50
```

```cmd
P_5                     all     0.6367
P_10                    all     0.6102
recall_5                all     0.1556
recall_10               all     0.2551
ndcg_cut_5              all     0.4754
ndcg_cut_10             all     0.5102
```

# Query expansion: use entities, use stemming & filter stopwords while analyzing (**50 tf-idf terms**)

```bash
docker run --rm -v $PWD/bglinking/resources:/opt/background-linking/bglinking/resources blimg_simple --run-tag entities_50 --use-entities --entities-stemming --entities-stopwords --nr-tfidf-terms 50
```

```cmd
P_5                     all     0.5714
P_10                    all     0.5673
recall_5                all     0.1271
recall_10               all     0.2395
ndcg_cut_5              all     0.4172
ndcg_cut_10             all     0.4652
```

# Query expansion: use entities, **don't** use stemming & don't filter stopwords while analyzing (**50 tf-idf terms**)

```bash
docker run --rm -v $PWD/bglinking/resources:/opt/background-linking/bglinking/resources blimg_simple --run-tag entities_nostem_nostop_50 --use-entities --nr-tfidf-terms 50
```

```cmd
P_5                     all     0.5796
P_10                    all     0.5592
recall_5                all     0.1275
recall_10               all     0.2375
ndcg_cut_5              all     0.4201
ndcg_cut_10             all     0.4635
```