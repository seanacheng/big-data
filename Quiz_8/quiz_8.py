import logging
import itertools

import numpy as np
import gensim

logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
logging.root.level = logging.INFO  # ipython sometimes messes up the logging setup; restore

def head(stream, n=10):
    """Convenience fnc: return the first `n` elements of the stream, as plain list."""
    return list(itertools.islice(stream, n))

from gensim.test.utils import datapath, get_tmpfile
from gensim.corpora import WikiCorpus, MmCorpus
path_to_wiki_dump = datapath("enwiki-latest-pages-articles1.xml-p000000010p000030302-shortened.bz2")
corpus_path = get_tmpfile("wiki-corpus.mm")
wiki = WikiCorpus(path_to_wiki_dump)  # create word->word_id mapping, ~8h on full wiki
MmCorpus.serialize(corpus_path, wiki)  # another 8h, creates a file in MatrixMarket format and mapping

texts = [' '.join(txt) for txt in wiki.get_texts()]
print(texts[0])
print(texts[1])

# import gensim.utils as utils
from smart_open import smart_open
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from gensim.corpora.wikicorpus import _extract_pages, filter_wiki

def tokenize(text):
    return [token for token in simple_preprocess(text) if token not in STOPWORDS]

def iter_wiki(dump_file):
    """Yield each article from the Wikipedia dump, as a `(title, tokens)` 2-tuple."""
    ignore_namespaces = 'Wikipedia Category File Portal Template MediaWiki User Help Book Draft'.split()
    for title, text, pageid in _extract_pages(smart_open(dump_file)):
        text = filter_wiki(text)
        tokens = tokenize(text)
        if len(tokens) < 50 or any(title.startswith(ns + ':') for ns in ignore_namespaces):
            continue  # ignore short articles and various meta-articles
        yield title, tokens

wiki_file = './data/simplewiki-latest-pages-articles.xml.bz2'
stream = iter_wiki(wiki_file)
for title, tokens in itertools.islice(iter_wiki(wiki_file), 8):
    print (title, tokens[:10])  # print the article title and its first ten tokens

id2word = {0: u'word', 2: u'profit', 300: u'another_word'}

doc_stream = (tokens for _, tokens in iter_wiki(wiki_file))

id2word_wiki = gensim.corpora.Dictionary(doc_stream)
print(id2word_wiki)

id2word_wiki.filter_extremes(no_below=20, no_above=0.1)
print(id2word_wiki)

doc = "A blood cell, also called a hematocyte, is a cell produced by hematopoiesis and normally found in blood."
bow = id2word_wiki.doc2bow(tokenize(doc))
print(bow)

print(id2word_wiki[10882])

class WikiCorpus(object):
    def __init__(self, dump_file, dictionary, clip_docs=None):
        """
        Parse the first `clip_docs` Wikipedia documents from file `dump_file`.
        Yield each document in turn, as a list of tokens (unicode strings).

        """
        self.dump_file = dump_file
        self.dictionary = dictionary
        self.clip_docs = clip_docs

    def __iter__(self):
        self.titles = []
        for title, tokens in itertools.islice(iter_wiki(self.dump_file), self.clip_docs):
            self.titles.append(title)
            yield self.dictionary.doc2bow(tokens)

    def __len__(self):
        return self.clip_docs

# create a stream of bag-of-words vectors
wiki_corpus = WikiCorpus(wiki_file, id2word_wiki)
vector = next(iter(wiki_corpus))
print(vector)  # print the first vector in the stream

len(vector)
max([pair[1] for pair in vector])

index = [pair[1] for pair in vector].index(15)

(most_index, most_count) = max(vector, key=lambda pair: pair[1])
print(id2word_wiki[most_index], most_count)

gensim.corpora.MmCorpus.serialize('./data/wiki_bow.mm', wiki_corpus)

mm_corpus = gensim.corpora.MmCorpus('./data/wiki_bow.mm')
print(mm_corpus)

print(next(iter(mm_corpus)))

from gensim.utils import SaveLoad
class ClippedCorpus(SaveLoad):
    def __init__(self, corpus, max_docs=None):
        """
        Return a corpus that is the "head" of input iterable `corpus`.

        Any documents after `max_docs` are ignored. This effectively limits the
        length of the returned corpus to <= `max_docs`. Set `max_docs=None` for
        "no limit", effectively wrapping the entire input corpus.

        """
        self.corpus = corpus
        self.max_docs = max_docs

    def __iter__(self):
        return itertools.islice(self.corpus, self.max_docs)

    def __len__(self):
        return min(self.max_docs, len(self.corpus))

clipped_corpus = gensim.utils.ClippedCorpus(mm_corpus, 4000)  # use fewer documents during training, LDA is slow
lda_model = gensim.models.LdaModel(clipped_corpus, num_topics=10, id2word=id2word_wiki, passes=4)

_ = lda_model.print_topics(-1)  # print a few most important words for each LDA topic

tfidf_model = gensim.models.TfidfModel(mm_corpus, id2word=id2word_wiki)

lsi_model = gensim.models.LsiModel(tfidf_model[mm_corpus], id2word=id2word_wiki, num_topics=200)

print(next(iter(lsi_model[tfidf_model[mm_corpus]])))

gensim.corpora.MmCorpus.serialize('./data/wiki_tfidf.mm', tfidf_model[mm_corpus])
gensim.corpora.MmCorpus.serialize('./data/wiki_lsa.mm', lsi_model[tfidf_model[mm_corpus]])
# gensim.corpora.MmCorpus.serialize('./data/wiki_lda.mm', lda_model[mm_corpus])

tfidf_corpus = gensim.corpora.MmCorpus('./data/wiki_tfidf.mm')
# `tfidf_corpus` is now exactly the same as `tfidf_model[wiki_corpus]`
print(tfidf_corpus)

lsi_corpus = gensim.corpora.MmCorpus('./data/wiki_lsa.mm')
# and `lsi_corpus` now equals `lsi_model[tfidf_model[wiki_corpus]]` = `lsi_model[tfidf_corpus]`
print(lsi_corpus)

text = "A blood cell, also called a hematocyte, is a cell produced by hematopoiesis and normally found in blood."

# transform text into the bag-of-words space
bow_vector = id2word_wiki.doc2bow(tokenize(text))
print([(id2word_wiki[id], count) for id, count in bow_vector])

# transform into LDA space
lda_vector = lda_model[bow_vector]
print(lda_vector)
# print the document's single most prominent LDA topic
print(lda_model.print_topic(max(lda_vector, key=lambda item: item[1])[0]))

# transform into LSI space
lsi_vector = lsi_model[tfidf_model[bow_vector]]
print(lsi_vector)
# print the document's single most prominent LSI topic (not interpretable like LDA!)
print(lsi_model.print_topic(max(lsi_vector, key=lambda item: abs(item[1]))[0]))

# store all trained models to disk
lda_model.save('./data/lda_wiki.model')
lsi_model.save('./data/lsi_wiki.model')
tfidf_model.save('./data/tfidf_wiki.model')
id2word_wiki.save('./data/wiki.dictionary')


# load the same model back; the result is equal to `lda_model`
same_lda_model = gensim.models.LdaModel.load('./data/lda_wiki.model')

# select top 50 words for each of the 20 LDA topics
# top_words = [[word for _, word in lda_model.show_topic(topicno, topn=50)] for topicno in range(lda_model.num_topics)] # original code
top_words = [[word for word, _ in lda_model.show_topic(topicno, topn=50)] for topicno in range(lda_model.num_topics)] # changed for equivalence
print(top_words)

# get all top 50 words in all 20 topics, as one large set
all_words = set(itertools.chain.from_iterable(top_words))

print("Can you spot the misplaced word in each topic?")

# for each topic, replace a word at a different index, to make it more interesting
replace_index = np.random.randint(0, 10, lda_model.num_topics)

replacements = []
for topicno, words in enumerate(top_words):
    other_words = all_words.difference(words)
    replacement = np.random.choice(list(other_words))
    replacements.append((words[replace_index[topicno]], replacement))
    words[replace_index[topicno]] = replacement
    print (topicno, ' '.join([str(w) for w in words[:10]]))
    # print("%i: %s" % (topicno, ' '.join(words[:10])))

print("Actual replacements were:")
print(list(enumerate(replacements)))

# evaluate on 1k documents **not** used in LDA training
doc_stream = (tokens for _, tokens in iter_wiki(wiki_file))  # generator
test_docs = list(itertools.islice(doc_stream, 8000, 9000))

def intra_inter(model, test_docs, num_pairs=10000):
    # split each test document into two halves and compute topics for each half
    half = int(len(test_docs)/2)
    part1 = [model[id2word_wiki.doc2bow(tokens[: half])] for tokens in test_docs]
    part2 = [model[id2word_wiki.doc2bow(tokens[half :])] for tokens in test_docs]

    # print computed similarities (uses cossim)
    print("average cosine similarity between corresponding parts (higher is better):")
    print(np.mean([gensim.matutils.cossim(p1, p2) for p1, p2 in zip(part1, part2)]))

    random_pairs = np.random.randint(0, len(test_docs), size=(num_pairs, 2))
    print("average cosine similarity between 10,000 random parts (lower is better):")
    print(np.mean([gensim.matutils.cossim(part1[i[0]], part2[i[1]]) for i in random_pairs]))

print("LDA results:")
intra_inter(lda_model, test_docs)

print("LSI results:")
intra_inter(lsi_model, test_docs)

