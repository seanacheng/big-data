# import matplotlib.pyplot as plt
# import numpy as np
# import csv
# import math



# taxi_rides = []
# with open('Quiz_3/chicago-taxi-rides.csv', 'r') as file:
#     reader = csv.reader(file)
#     for row in reader:
#         try:
#             int(row[0])
#             taxi_rides.append(row)
#         except:
#             continue

# x = [int(row[0]) for row in taxi_rides]
# y = [int(row[1] )for row in taxi_rides]
# z = [math.log(int(row[2])) for row in taxi_rides]
# plt.scatter(x, y, c=z, cmap='Blues', s=10)
# plt.colorbar(label='trips')
# plt.xlabel('dropoff_community_area')
# plt.ylabel('pickup_community_area')
# plt.xticks([10, 20, 30, 40, 50, 60, 70])
# plt.yticks([10, 20, 30, 40, 50, 60, 70])
# plt.show()

# matrix = np.zeros((77, 77))

# for row in taxi_rides:
#     matrix[int(row[0])-1, int(row[1])-1] = int(row[2])

# column_sums = matrix.sum(axis=0)
# stochastic_matrix = matrix / column_sums

# rank = np.full(77, 1/77)
# # print("iteration 0")
# # print(rank)

# for i in range(6):
#     rank = np.dot(stochastic_matrix,rank)
# #     print("iteration "+str(i+1))
# #     print(rank)

# hardship_index = [39.4,47.3,31.5,21.7,16.9,9.9,10.3,8.6,21.8,28.2,31.3,26.7,42.8,45.7,36.2,32.3,33.4,43.9,55.9,54.3,38.6,25.6,60.3,18.7,53.1,68.3,58.9,26.6,59.8,70.6,50.1,9.0,11.2,63.5,42.5,53.2,64.9,49.8,34.6,60.2,25.3,50.4,51.4,47.9,47.6,54.9,51.2,38.4,52.6,43.3,58.1,56.7,54.3,84.2,37.0,38.7,56.1,66.1,51.5,41.9,62.6,49.2,65.3,38.8,53.7,59.2,63.3,70.5,54.3,40.8,51.5,24.5,43.3,25.6,36.7,33.8,28.9]
# total_hardship = sum(hardship_index)
# hardship_index = [i/total_hardship for i in hardship_index]

# plt.plot(np.arange(77), rank, label='TrafficRank')
# plt.plot(np.arange(77), hardship_index, label='Hardship Index')
# plt.title('Economic Rank vs. Hardship Index')
# plt.xlabel('community areas')
# plt.ylabel('rank/index')
# plt.legend()
# plt.show()

import tarfile
import os
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def get_top_15_words(tar_file_path, extract_path):
    with tarfile.open(tar_file_path, 'r:gz') as tar:
        tar.extractall(path=extract_path)

    base_name = os.path.basename(tar_file_path).split(".")[0]
    dir_path = extract_path + "/" + base_name
    texts = []
    for filename in os.listdir(dir_path):
        with open(os.path.join(dir_path, filename), 'r', encoding='utf-8') as file:
            texts.append(file.read())

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(texts)
    word_scores = np.array(tfidf_matrix.sum(axis=0)).flatten() # Sum TF-IDF scores for each word across all documents

    feature_names = vectorizer.get_feature_names_out()
    sorted_indices = word_scores.argsort()[::-1]

    print(f"Top 15 Most Important Words for {base_name.capitalize()}:")
    for i in range(15):
        word = feature_names[sorted_indices[i]]
        score = word_scores[sorted_indices[i]]
        # print(f"{i+1}. {word}: {score:.4f}")
        print(f"{i+1}. {word}")

file_path = 'Quiz_3/prez_speeches/carter.tar.gz'
extract_path = 'Quiz_3/'
get_top_15_words(file_path, extract_path)

