import numpy as np

project_root = 'C:/Users/mika/Documents/Radboud/Courses/Master_Year_1/Information_Retrieval/Project/background-linking-IR'
input_file = "{}/bglinking/resources/candidates/candidates.backgroundlinking20.txt".format(project_root)
output_file = "{}/bglinking/resources/candidates/candidates_filtered.backgroundlinking20.txt".format(project_root)

topic_amount = 10
candidates_per_topic = 5

# topic ids are between 886 and 935, so choose 10 of these
chosen_topics = np.random.choice(range(886,936), topic_amount, replace=False)
print("Chosen topics: {}".format(chosen_topics))

candidates = []

# Read all candidates and store the top 5 (= first 5, assuming the candidates are ordered) candidates for every chosen topic
with open(input_file, 'r') as file:
    for line in file.readlines():
        topicid,_,docid,rank,_,_ = line.split(' ')
        if int(topicid) not in chosen_topics:
            continue
        if int(rank) > candidates_per_topic:
            continue
        candidates += [line]

with open(output_file, 'w') as file:
    for c in candidates:
        file.write(c)