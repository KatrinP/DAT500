#!/usr/bin/env python
import sys

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


for line in sys.stdin: # read input from STDIN
  line = line.strip() # remove leading and trailing whitespace
  ngrams = count_ngrams(line,1);

  for elem in ngrams.keys():
	print '%s\t%s' % ( str ( elem ), ngrams[elem])


