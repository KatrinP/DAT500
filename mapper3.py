#!/usr/bin/python2.7
import sys
import re
import io
import codecs

sys.stdin = codecs.getreader("utf-8")(sys.stdin)

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


for line in sys.stdin:
    #line = line.strip() # remove leading and trailing whitespace
    line = re . sub ( "\r", "\n", line )
    line = re . sub ( "\n\n", "\n", line )
    #
    #
    #   if we use count_ngrams ( line, 1, lambda x: x . split () )
    #   we are making ngrams from whole words
    #   By default is using lambda x: list ( x ) which splits string to characters 
    #

    ngrams = count_ngrams( line, 3 );
    for elem in ngrams.keys():
        print ( '%s\t%s' % ( str ( elem ) . encode ( "utf-8" ), ngrams[elem] ) )


