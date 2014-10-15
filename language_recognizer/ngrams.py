# import collections
import math
import sys

# TODO: probability in one function!

def make_ngrams(plain_text, n, split = lambda x: list ( x ) ):
    ngram_array = []
    array_text = split ( plain_text )
    for i in range(len(array_text) - n + 1):
        ngram = []
        #ngram = ""
        for j in range(i, i + n):
            #ngram = ngram + array_text [j]
            ngram.append((array_text[j]))
        ngram_array.append(tuple(ngram))
        #ngram_array.append(ngram)
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


def count_ngrams(plain_text, n, split = lambda x: list ( x ) ):
    ngram_array = make_ngrams(plain_text, n, split)
    ngrams = counter(ngram_array)
    return ngrams


def probability2(ngrams = [], n = 1, smooth = 1):
    #print ( ngrams )
    if n < 1:
        raise Exception ( "Fatal error. probability2(): n is less than one." )
    if len ( ngrams ) <= 0:
        raise Exception ( "Fatal error. probability2(): No n-grams." )
    total = 1
    gram_probability = {}
    for the_gram in ngrams [ "ngrams" ] [ n - 1 ]:
        up = 0      
        if isinstance ( ngrams [ "ngrams" ] [n-1] [the_gram], type( tuple () ) ) or \
           isinstance ( ngrams [ "ngrams" ] [n-1] [the_gram], type( list () ) ):
            up = ngrams [ "ngrams" ] [n-1] [the_gram] [1]
        else:    
            up = ngrams [ "ngrams" ] [n-1] [the_gram]

        up = up + smooth * 1

        if n > 1:
            V = ngrams [ "count" ] [ n - 2 ]

            if the_gram [ :n-1 ] in ngrams [ "ngrams" ] [ n - 2 ] . keys ():
                total = ngrams [ "ngrams" ] [ n - 2 ]  [ the_gram [ :n-1 ] ] [ 1 ]
            else:
                # this means that there was a violence during add of ngrams from this floor
                total = ngrams [ "total" ] [ n - 2 ]
                up = 1
                #up = 1
                #print ( "loking for " + the_gram + " in" )
                #print ( ngrams [ n - 2 ] )
                #total = 1
                #raise Exception ( "Fatal error. probability2(): N-grams has to be processed sorted by a n." )
            total = total + smooth * V
        else:
            V = 0
            V = ngrams [ "total" ] [ n - 1 ]
            total = ngrams [ "count" ] [ n - 1 ] + smooth * V


        gram_probability[the_gram] = -math.log( up / total, 10)
        if gram_probability [ the_gram ] == -0.00:
            del gram_probability [ the_gram ]
    return gram_probability    

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
