import tarfile
import os

file_path = 'prez_speeches/adams.tar.gz'
extract_path = 'Quiz_4/'
with tarfile.open(file_path, 'r:gz') as tar:
    tar.extractall(path=extract_path)

    base_name = os.path.basename(file_path).split(".")[0]
    dir_path = extract_path + "/" + base_name
    texts = []
    for filename in os.listdir(dir_path):
        with open(os.path.join(dir_path, filename), 'r', encoding='utf-8') as file:
            texts.append(file.read())