import operator
import collections
import sys
import math
import getopt

import language_recognizer.ngrams as ngrams
import language_recognizer.langVector as langVector


def smoothing ( string, vector, n ):
    def occurence ( string, vector, n ):
        if n < 0:
            return 0
        
        #print ( "\t\t%s in vector[%d]" % ( repr ( string ), n - 1) )
        if string in vector [ "ngrams" ] [ n - 1 ] . keys ():
            return vector [ "ngrams" ] [ n - 1 ] [ string ] [ 1 ]

        return occurence ( string [ 1:], vector, n - 1 )


    up = 1
    #print ( "occurence: " )
    #print ( "\t%s" % repr ( string ) ) 
    up = up + occurence ( string [ 1: ], vector, n - 1 )

    #print ( "occurence: " + str ( up ) )

    if n < 0:
        n = 0

    total = vector [ "count" ] [ n - 1 ] * vector [ "total" ] [ n - 1 ] + 1

    return -math . log ( up / total, 10 )


# MAYBE: improve the command line arguments???

# constants:
smoothing_rate = 1
ngram_rate = 1
number_of_ngrams = 3

#count a score for sentence from vector of a language ~ probability for ngrams in the language (suma of logarithms)
def count_ngram_score(sentence, vector, n ):
    score = 0
    ngrams_array = ngrams.make_ngrams(sentence, n )
    #print ( ngrams_array )
    #print ( ngrams_array )
    #smoothing - for ngrams which don't appear in vector of language
    #set the worst (max) value in lang vector
    ngram_prop_func = [ ngrams.probability, ngrams.probability_of_bigram, ngrams.probability_of_trigram ]
    #smoothing = max(vector [ "ngrams" ] [n - 1].items(), key=operator.itemgetter(1))[0]
    #print ( smoothing )
    for ngram in ngrams_array:
        #ngram = "" . join ( ngram )
        #print ( repr ( vector[ "ngrams" ]  [ n - 1 ] ))
        if ngram in vector[ "ngrams" ] [n - 1]:
            #print ( str ( vector[ "ngrams" ] [n - 1][ngram] ) )
            #print ( "hit")
            score += vector[ "ngrams" ] [n - 1][ngram][0] # 0 - prob
        else:
            #continue
            #print ( "not hit" )
            
            score += smoothing ( ngram, vector, n )

    return score


#n = number of kinds of used ngrams (uni + bi + trigram = 3)
def recognize_language(sentence, vectors, n):
    scores = []

    #print ( repr ( scores ) )
    #result for uni/bi/trigrams - 0 ~ uni etc.
    winners_for_ngram = []  #remebers which language was the best for uni, bi and trigram
    detected_languages = collections.defaultdict(int)  #key = best lang for some ngram, value is number (countet rate)

    #score is list which contents a dictionary for each ngram.
    #Key in dict is language, value is the for for given sentence
    for i in range(0, n):
        scores.append({})
        smoothing = 0
        #for language in vectors.keys():
        #    m = max(vectors[language][i].items(), key=operator.itemgetter(1)) [ 1 ]
        #    if m > smoothing:
        #        smoothing = m
        for language in vectors.keys():
            #print ( "for language: " + language )
            #print ( "pro " + str ( i + 1 ) + " gramy jazyka: " + language )
            scores[i][language] = count_ngram_score(sentence, vectors[language], i + 1)
            #print ( "result: " + str ( scores [ i ] [ language ] ) ) 
        #find the language with lowes score for i-gram
        #print ( "items" )
        #print ( scores [ i ] . items () )
        #print ( "min" )
        #print ( min(scores[i].items(), key=operator.itemgetter(1)) )
        best_language = min(scores[i].items(), key=operator.itemgetter(1))

        #print ( smoothing )
        if len ( scores[i].items() ) == len ( [ o for o in scores[i].items() if o [1] == best_language[1] ] ) and len ( scores[i].items() ) != 1:
            continue
        best_language = best_language [ 0 ]
        
        #print ( best_language )
        #ngram_rate tell us how much more important is the result by trigram then by unigram etc.
        #notice and add rate if for ngram is the language the best
        detected_languages[best_language] += (i + 1) * ngram_rate
        winners_for_ngram.append(best_language)




    #print ( repr ( detected_languages  ))
    final_language = find_the_best(detected_languages, winners_for_ngram, n)
    #count probability of our result
    probability = detected_languages[final_language] / sum(detected_languages.values())
    return final_language, probability


#it can happen that the result is a drew...
def find_the_best(detected_languages, winners_for_ngram, n):
    #find the languge which highest value
    highest = max(detected_languages.values())
    #find all languages with highest value
    identic_result = []  #if there is a draw
    for key, value in detected_languages.items():
        if value == highest:
            identic_result.append(key)
    #decide which language from these with identical value is the best
    if len(identic_result) > 1:
        out = False
        for i in range(n, 0,
                       - 1):  #choose the one acording the highest ngram (trigram result is more predicative the unigram result)
            for language in identic_result:
                if winners_for_ngram[i - 1] == language:
                    final_language = language
                    out = True
                    break
            if out:
                break
    else:
        final_language = identic_result[0]
    return final_language


def main ( argv = None ):

    def usage ():
        print ( "Usage: " + sys.argv[0] + " [options] <sentence[, sentence2, ...]" )
        print ( "" )
        print ( "Options:" )
        print ( "   --help|-h               show this help message and exit" )
        print ( "   --l <lang>              set the language of new vector" )
        print ( "   --add-vector <file>     make and add vector from file <file>" )
        print ( "   --vectors|-v <file>     set the vectors file" )
        #print ( "" )
        #print ( "Examples:" )
        #print ( "   script.py --input ..\\languages\\nowiki\\ -t 8 --merge -c 500 -l nn" )
        #print ( "   script.py --input ..\\languages\\nowiki\\nn.links.txt.00000000.txt -t 8 --merge --delete-after-merge -c 20 -l nn" )





    if not argv:
        argv = sys . argv

    filename = None
    language = None
    sentences = []

    if argv is None:
        argv = sys.argv
    try:
        opts, args = getopt.getopt(
            argv[1:], "hv:l:", [
                "help", "add-vector=", "vectors=" ])
    except getopt.GetoptError:
        usage ()
        return 0
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage ()
            return 0
        elif opt == "--add-vector":
            filename = str ( arg )
        elif opt == "-l":
            language = str ( arg )
        elif opt in ( "--vectors", "-v" ):
            vector_file = str ( arg )
        else:
            assert False, "Fatal error. Bad option."


    sentences = [ a for a in args if a ]

    if len ( sentences ) <= 0:
        raise Exception ( "Fatal error. No sentence." )

    if ( filename and not language ) or \
       ( not filename and language ):
       raise Exception ( "Fatal error. Options --add-vector and -l has to be set together" )     

    if len(sys.argv) > 2:
        sentence = sys.argv[1]
        vector_file = sys.argv[2]
    elif len(sys.argv) == 2:
        sentence = sys.argv[1]
        vector_file = "language_vector.p"
    else:
        sentence = input("Your sentence: ")
        vector_file = "language_vector.p"

    #sentence = open ( "input.txt", "r", encoding = "utf-8" ) . read ()

    with langVector . Vector ( "vec.json" ) as lv:
        if filename and language:
            lv . addVector ( language, filename, plainText = True )
        lv.addVector("bulgarian", "language_recognizer/hadoopOut/bg.grams.txt", ngrams_sum_func=langVector.readHadoopOutput, update=True)
        lv.addVector("breton", "language_recognizer/hadoopOut/br.grams.txt", ngrams_sum_func=langVector.readHadoopOutput, update=True)
        lv.addVector("czech", "language_recognizer/hadoopOut/cs.grams.txt", ngrams_sum_func=langVector.readHadoopOutput, update=True)
        lv.addVector("danish", "language_recognizer/hadoopOut/da.grams.txt", ngrams_sum_func=langVector.readHadoopOutput, update=True)
        #lv.addVector("german", "language_recognizer/hadoopOut/de.grams.txt", ngrams_sum_func=langVector.readHadoopOutput, update=True)
        lv.addVector("english", "language_recognizer/hadoopOut/en.grams.txt", ngrams_sum_func=langVector.readHadoopOutput, update=True)
        lv.addVector("spanish", "language_recognizer/hadoopOut/es.grams.txt", ngrams_sum_func=langVector.readHadoopOutput, update=True)
        lv.addVector("finnish", "language_recognizer/hadoopOut/fi.grams.txt", ngrams_sum_func=langVector.readHadoopOutput, update=True)
        lv.addVector("french", "language_recognizer/hadoopOut/fr.grams.txt", ngrams_sum_func=langVector.readHadoopOutput, update=True)
        lv.addVector("italian", "language_recognizer/hadoopOut/it.grams.txt", ngrams_sum_func=langVector.readHadoopOutput, update=True)
        lv.addVector("dutch", "language_recognizer/hadoopOut/nl.grams.txt", ngrams_sum_func=langVector.readHadoopOutput, update=True)
        lv.addVector("nynorsk", "language_recognizer/hadoopOut/nn.grams.txt", ngrams_sum_func=langVector.readHadoopOutput, update=True)
        lv.addVector("norwegian", "language_recognizer/hadoopOut/no.grams.txt", ngrams_sum_func=langVector.readHadoopOutput, update=True)
        lv.addVector("polish", "language_recognizer/hadoopOut/pl.grams.txt", ngrams_sum_func=langVector.readHadoopOutput, update=True)
        lv.addVector("portuguese", "language_recognizer/hadoopOut/pt.grams.txt", ngrams_sum_func=langVector.readHadoopOutput, update=True)
        lv.addVector("romanian", "language_recognizer/hadoopOut/ro.grams.txt", ngrams_sum_func=langVector.readHadoopOutput, update=True)
        lv.addVector("russian", "language_recognizer/hadoopOut/ru.grams.txt", ngrams_sum_func=langVector.readHadoopOutput, update=True)
        lv.addVector("slovak", "language_recognizer/hadoopOut/sk.grams.txt", ngrams_sum_func=langVector.readHadoopOutput, update=True)
        lv.addVector("swedish", "language_recognizer/hadoopOut/sv.grams.txt", ngrams_sum_func=langVector.readHadoopOutput, update=True)
        lv.addVector("ukrainian", "language_recognizer/hadoopOut/uk.grams.txt", ngrams_sum_func=langVector.readHadoopOutput, update=True)


        #lv . addVector ( "belgium", "out/part-00000", ngrams_sum_func = langVector . readHadoopOutput, update = True )
        #lv . addVector ( "belgium", "out/output.txt", ngrams_sum_func = langVector . readHadoopOutput, update = True )
        #lv . addVector ( "belgium", "out/part-00001", ngrams_sum_func = langVector . readHadoopOutput, update = True )
        #lv . addVector ( "english", "trait/english.txt", plainText = True)
        #lv . addVector ( "urdu", "trait/urdu.txt", plainText = True)
        #lv . addVector ( "czech", "trait/czech.txt", plainText = True)
        #lv . addVector ( "polish", "trait/polish.txt", plainText = True)
        #lv . addVector ( "german", "trait/german.txt", plainText = True)
        #lv . addVector ( "norwegian", "trait/bokmal.txt", plainText = True)
        #lv . addVector ( "nynorsk", "trait/nynorsk.txt", plainText = True)
        #lv . addVector ( "german", "input.txt", plainText = True)


        #vectors = langVector.load_vector(vector_file)#vector_file
        vectors = lv . vectors ()
        #sys . exit ( 0 )

        for sentence in sentences:
            language, probability = recognize_language(sentence, vectors, number_of_ngrams)
            print("Given sentence is in",language, "(with", probability*100, "% probability)")



    return 0


#main:
if __name__ == "__main__":
    #command line inputs and default setting od vectors file


    sys.exit( main () )
