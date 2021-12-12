import numpy as np

project_root = 'C:/Users/mika/Documents/Radboud/Courses/Master_Year_1/Information_Retrieval/Project/background-linking-IR'
input_file = "{}/bglinking/resources/candidates/candidates_filtered.backgroundlinking20.txt".format(project_root)
output_file = "{}/bglinking/resources/candidates/candidates_final.backgroundlinking20.txt".format(project_root)

allowed_docids = [
    "a6be1e92-50de-11e1-bd4f-8a7d53f6d6c2",
    "1ff747a2-5274-11e6-88eb-7dda4e2f2aec",
    "4O65GQGRCNAADKPRA73EWUXBOY",
    "e9e4688e-9b9d-11e1-9b4b-7af57477550e",
    "AFJNUFUYYVE5PEWJNUF7LZTHXQ",
    "F2AXCYUPH5BEVNXKMQ74MMKWTA",
    "FAI6K4URXRFOBGSWRLWAPRIMN4",
    "BNQBR26SIVA2TCH45LX5C7VSCI",
    "NDTJ2WV4A5GIBAKQX57XJED2AI",
    "1ce479a6f181ef041bcec0e55a0e1fde",
    "6TCZKBHR6EI6TCPL5RLM2QKHGI",
    "288ff6b0-4c2b-11e1-8d55-edfca0e33083",
    "8316d01c-8039-11e6-b002-307601806392",
    "b4ea9dcc-b338-11e5-a842-0feb51d1d124",
    "225b87f0-ef5c-11e4-a55f-38924fca94f9"
]

candidates = []

# Read all candidates filter out entries with a docid that is not in the database
with open(input_file, 'r') as file:
    for line in file.readlines():
        topicid,_,docid,rank,_,_ = line.split(' ')
        if docid not in allowed_docids:
            continue
        candidates += [line]

with open(output_file, 'w') as file:
    for c in candidates:
        file.write(c)