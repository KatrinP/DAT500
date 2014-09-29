import pickle
import os
import sys
import collections

import language_recognizer . ngrams




# make a propbability list (vector) for one language
# source_file - file with plain text
def vector_of_language(source_file):
    opened_file = open(source_file, encoding="utf-8")
    unigrams = [{}, {}]
    bigrams = [{}, {}]
    trigrams = [{}, {}]
    for line in opened_file:
        unigrams[1] = ngrams.count_ngrams(line, 1)
        unigrams[0] = sum((collections.Counter(dict(lines)) for lines in unigrams), collections.Counter())
        bigrams[1] = ngrams.count_ngrams(line, 2)
        bigrams[0] = sum((collections.Counter(dict(lines)) for lines in bigrams), collections.Counter())
        trigrams[1] = ngrams.count_ngrams(line, 3)
        trigrams[0] = sum((collections.Counter(dict(lines)) for lines in trigrams), collections.Counter())

    unigram_probability = ngrams.probability(unigrams[0])
    bigram_probability = ngrams.probability_of_bigram(bigrams[0])
    trigram_probability = ngrams.probability_of_trigram(trigrams[0])
    return [unigram_probability, bigram_probability, trigram_probability]


def add_language_vector(language, source_file, vector_file):
    vectors = load_vector(vector_file)
    vectors[language] = vector_of_language(source_file)
    with open(vector_file, "wb") as f:
        pickle.dump(vectors, f)
    print("I have learned " + language + "!")

    return


def load_vector(vector_file):
    if os.path.isfile(vector_file) and os.stat(vector_file).st_size > 0:
        with open(vector_file, "rb") as f:
            vectors = pickle.load(f)
    else:
        vectors = {}
    if vectors == {}:
        user_answer = input(
            "File with language vectors was empty or didn't exist. New empty set of vectors will be created. OK? (Y/n): ")
        if user_answer.lower() == "n":
            sys.exit("Work without any vector file is not possible, sorry!")
    return vectors
