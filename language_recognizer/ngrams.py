# import collections
import math
import sys

# TODO: probability in one function!

def make_ngrams(plain_text, n):
    ngram_array = []
    array_text = list(plain_text)
    for i in range(len(array_text) - n + 1):
        ngram = []
        for j in range(i, i + n):
            ngram.append((array_text[j]))
        ngram_array.append(tuple(ngram))
    return ngram_array


def counter(ngram_array):
    def item_get(array, key):
        if key in array.keys():
            return array[key]
        else:
            return 0

    if sys.version_info < (2, 7):
        # compatibility
        map = {}
        if ngram_array is not None:
            if hasattr(ngram_array, "iteritems"):
                for elem, count in ngram_array.iteritems():
                    map[elem] = item_get(map, elem) + count
            else:
                for elem in ngram_array:
                    map[elem] = item_get(map, elem) + 1
        return map
    else:
        import collections

        return collections.Counter(ngram_array)


def count_ngrams(plain_text, n):
    ngram_array = make_ngrams(plain_text, n)
    ngrams = counter(ngram_array)
    return ngrams


#count the probability of unigrams, return logaritmus of probability to avoid small numbers
#probability = count of found / total count
def probability(unigrams):
    total = sum(unigrams.values())
    unigram_probability = {}
    for the_unigram in unigrams:
        unigram_probability[the_unigram] = -math.log(unigrams[the_unigram] / total, 10)
    return unigram_probability


#probability = count of certain bigram / total count bigrams with the same first letter
def probability_of_bigram(bigrams):
    bigram_probability = {}
    for the_bigram in bigrams:
        sum_of_frequency = 0
        for the_bigram2 in bigrams:
            if (the_bigram[0] == the_bigram2[0]):
                sum_of_frequency += bigrams[the_bigram2]
        bigram_probability[the_bigram] = -math.log(bigrams[the_bigram] / sum_of_frequency, 10)
        if bigram_probability[the_bigram] == -0.00:
            del bigram_probability[the_bigram]  #trash: throw away :)

    return bigram_probability


#probability = count of certain trigram / total count of trigrams with the same first two letters
def probability_of_trigram(trigrams):
    trigram_probability = {}
    for the_trigram in trigrams:
        sum_of_frequency = 0
        for the_trigram2 in trigrams:
            if (the_trigram[0] == the_trigram2[0]) & (the_trigram[1] == the_trigram2[1]):
                sum_of_frequency += trigrams[the_trigram2]
        trigram_probability[the_trigram] = -math.log(trigrams[the_trigram] / sum_of_frequency, 10)
        if trigram_probability[the_trigram] == -0.00:
            del trigram_probability[the_trigram]
    return trigram_probability
