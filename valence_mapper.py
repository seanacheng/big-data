#!/usr/bin/env python
"""valence_mapper.py"""

import sys
import requests
import re
import string
import tarfile
import os

stopwords_list = requests.get("https://gist.githubusercontent.com/rg089/35e00abf8941d72d419224cfd5b5925d/raw/12d899b70156fd0041fa9778d657330b024b959c/stopwords.txt").content
stopwords = list(set(stopwords_list.decode().splitlines()))

def remove_stopwords(words):
    list_ = re.sub(r"[^a-zA-Z0-9]", " ", words.lower()).split()
    return [itm for itm in list_ if itm not in stopwords]

def clean_text(text):
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), ' ', text)
    text = re.sub('[\d\n]', ' ', text)
    return ' '.join(remove_stopwords(text))

def load_afinn():
    afinn_url = 'https://raw.githubusercontent.com/fnielsen/afinn/master/afinn/data/AFINN-en-165.txt'
    afinn_collection = requests.get(afinn_url).text
    afinn_dict = dict(line.split('\t') for line in afinn_collection.splitlines())
    return {word: int(score) for word, score in afinn_dict.items()}

def read_input(file):
    for line in file:
        yield clean_text(line).split()

def main(separator='\t'):
    president = os.environ['mapreduce_map_input_file'].split("_")[0]
    data = read_input(sys.stdin)
    for words in data:
        for word in words:
            valence = afinn.get(word)
            print("LongValueSum:" + '%s%s%d' % (president, separator, valence))

if __name__ == "__main__":
    afinn = load_afinn()  # Load AFINN data
    main()


# file_path = 'prez_speeches/adams.tar.gz'
# extract_path = 'Quiz_4/'
# with tarfile.open(file_path, 'r:gz') as tar:
#     tar.extractall(path=extract_path)

#     base_name = os.path.basename(file_path).split(".")[0]
#     dir_path = extract_path + "/" + base_name
#     texts = []
#     for filename in os.listdir(dir_path):
#         with open(os.path.join(dir_path, filename), 'r', encoding='utf-8') as file:
#             texts.append(file.read())