import pickle
import os
import sys
import collections
import json
import re
import operator

import language_recognizer.ngrams as ngrams

class Vector:
    def __init__  ( self, vector_file ):
        self . _vector_file = vector_file
        self . _changed = False
        self . _vectors = {}
        self . loadVector ()

    def __enter__ ( self ):
        return self
    def __exit__ ( self, exct_type, exce_value, traceback ):
        self . save ()

    def save ( self ):
        if not self . _changed:
            return
        #with open ( self . _vector_file, "wb") as f:
        #    pickle.dump(self . _vectors, f) 
        with open ( self . _vector_file, "w", encoding = "utf-8" ) as f:
            for language in self . _vectors . keys ():
                for i, ngrams in enumerate ( self . _vectors [ language ] [ "ngrams" ] ):
                    nd = {}
                    for key in ngrams . keys ():
                        nd [ str ( key ) ] = ngrams [ key ]
                    self . _vectors [ language ] [ "ngrams" ] [ i ] = nd

            json . dump ( self . _vectors, f )

    def vectors ( self ):
        return self . _vectors

    def __iter__ ( self ):
        return self . _vectors . __iter__ ()        

    def loadVector ( self ):
        if not os.path.isfile( self . _vector_file ) or not os.stat( self . _vector_file ).st_size > 0:
            return

        with open ( self . _vector_file, encoding = "utf-8" ) as inputFile:
            self . _vectors = json . load ( inputFile )
            for language in self . _vectors . keys ():
                for i, ngrams in enumerate ( self . _vectors [ language ] [ "ngrams" ] ):
                    nd = {}
                    for key in ngrams . keys ():
                        nd [ eval ( key ) ] = ngrams [ key ]
                    self . _vectors [ language ] [ "ngrams" ] [ i ] = nd

    def fillResult ( self, result, ngrams_sum ):
        for i, ngram in enumerate ( ngrams_sum ):
            result [ "count" ] . append ( sum ( ngram . values () ) )


        result [ "total" ] = [ 0 for x in ngrams_sum ]
        for vector in self . _vectors . keys ():
            for i, ngram in enumerate ( self . _vectors [ vector ] [ "count" ] ):
                result [ "total" ] [ i ] += ngram
        for i, ngram in enumerate ( result [ "count" ] ):
            result [ "total" ] [ i ] += ngram

        result [ "ngrams" ] = ngrams_sum


        for i, ngram in enumerate ( ngrams_sum ):
            #probability = ngram_prop_func [ i ] ( ngram )
            probability = ngrams . probability2 ( result, i + 1 )
            #print ( probability )
            for k in list ( ngram . keys() ):
                if k not in probability:
                    del ngram [ k ]
                    continue
                ngram [ k ] = ( probability [ k ], ngram [ k ] )

        result [ "ngrams" ] = ngrams_sum

        return result              

    def addVector ( self, language, source_file, ngrams_sum_func = None, fullFormat = False, update = False ):
        self . _changed = True
        if language in self . _vectors . keys ():
            del self . _vectors [ language ]
        #if update and language in self . _vectors . keys ():
        #    self . _vectors [ language ] [ "total" ] [ ]
        ngrams_sum = [ {}, {}, {} ]
        result = { "count": [],
                   "ngrams": [],
                   "total": [] }

        if ngrams_sum_func is not None:
            ngrams_sum = ngrams_sum_func ( source_file, ngrams_sum )
            result [ "ngrams" ] = ngrams_sum
            result = self . fillResult ( result, ngrams_sum )
        else:
            with open ( source_file, encoding = "utf-8" ) as inputFile:
                if fullFormat:
                    result = json . load ( inputFile )
                else:
                    # only list of ngrams with their count
                    ngrams_sum = json . load ( inputFile )
                    result = self . fillResult ( result, ngrams_sum )       


        #print ( result )
        #if language in self . _vectors . keys () and update:
        #    self . _vectors [ language ] . update ( result )
        #else:
        self . _vectors [ language ] = result
        print ( "I have learned " + language + "!" )


def readPlainText ( source_file, ngrams_sum ):
    with open ( source_file, encoding = "utf-8" ) as inputFile:
        s = 0
        for line in inputFile:
            s = s + 1
            line = re . sub ( "\r", "\n", line )
            line = re . sub ( "\n\n", "\n", line )
            for i, ngram in enumerate ( ngrams_sum ):
                extracted_grams = ngrams . count_ngrams ( line, i + 1 )
                combined = [ extracted_grams, ngrams_sum [ i ] ]
                ngrams_sum [ i ] = sum((collections.Counter(dict(lines)) for lines in combined), collections.Counter())

    return ngrams_sum   

def readHadoopOutput ( source_file, ngrams_sum ):
    with open ( source_file, encoding = "utf-8" ) as inputFile:
        s = 0
        for line in inputFile:
            line = line . strip ()
            #print (s )
            s = s + 1 
            parts = line . split ( "\t" )
            if len ( parts ) <= 0 or len ( parts ) > 2:
                raise Exception ( "Fatal error. readHadoopOutput(): Wrong line format." )
            try:
                key = eval ( parts [ 0 ] )
                val = int ( parts [ 1 ] )
            except Exception as inst:
                raise Exception ( "Fatal error. readHadoopOutput(): Wrong line format." )

            gram = len ( key )
            if gram <= 0:
                raise Exception ( "Fatal error. readHadoopOutput(): Wrong key format." )
            ngrams_sum [ gram - 1 ] [ key ] = val

    return ngrams_sum 


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
    """
    Not finished memory-safe loading

    def memory():
        # LINUX
        import resource
        resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000
    language = None
    key = None
    nest = 0
    if os.path.isfile(vector_file) and os.stat(vector_file).st_size > 0:
        with open  ( vector_file, "rb" ) as inputFile, open ( "read.txt", "w", encoding = "utf-8" ) as out:
            parser = ijson . parse ( inputFile )
            for prefix, event, value in parser:
                if ( prefix, event, value ) == ( '', 'start_map', None ):
                    print ( "Start processing the file" )
                elif ( prefix, event ) == ( '', 'map_key' ):
                    language = value
                    vectors [ language ] = [ {}, {}, {} ]
                elif ( prefix, event ) == ( language, "start_array" ):
                    print ( "Starting processing the language %s" % language )
                elif language and ( prefix, event ) == ( "%s.item" % language, "start_map" ):
                    pass
                elif language and ( prefix, event ) == ( "%s.item" % language, "end_map" ):
                    nest = nest + 1

                elif language and ( prefix, event ) == ( "%s.item" % language, "map_key" ):
                    key = value
                elif language and key and ( prefix, event ) == ( "%s.item.%s" % ( language, key ), "number" ):
                    probability = float ( value )
                    vectors [ language ] [ nest ] [ key ] = probability
                    key = None
                elif ( prefix, event ) == ( language, "end_array" ):
                    print ( "Finishing processing the language %s" % language )
                    language = None
                    #print ( memory () )
                    nest = 0
                elif ( prefix, event, value ) == ( '', 'end_map', None ):
                    print ( "Finishing processing the file" )    
    #print ( repr ( vectors ) . encode ( "utf-8" ) )
    """

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


    nd = {}
    for lang in vectors.keys():
        nd [ lang ] = []
        i = 0
        for ngrams in vectors[lang]:
            nd [ lang ] . append ( {} )
            for k in ngrams.keys():
                nk = "" . join ( k )
                nd [ lang ] [ i ] [ nk ] = ngrams [ k ]
            i = i + 1
    f = open ( "dump.txt", "w", encoding = "utf-8" )
    json.dump(nd, f)
    f.close()
    return vectors
