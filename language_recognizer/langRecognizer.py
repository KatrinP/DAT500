import operator
import collections

import ngrams





# MAYBE: improve the command line arguments???

# constants:
smoothing_rate = 1.5
ngram_rate = 1
number_of_ngrams = 3

#count a score for sentence from vector of a language ~ probability for ngrams in the language (suma of logarithms)
def count_ngram_score(sentence, vector, n):
    score = 0
    ngrams_array = ngrams.make_ngrams(sentence, n)

    #smoothing - for ngrams which don't appear in vector of language
    #set the worst (max) value in lang vector
    smoothing = max(vector[n - 1].items(), key=operator.itemgetter(1))[0]
    for ngram in ngrams_array:
        if ngram in vector[n - 1]:
            score += vector[n - 1][ngram]
        else:
            score += vector[n - 1][smoothing] / smoothing_rate
    return score


#n = number of kinds of used ngrams (uni + bi + trigram = 3)
def recognize_language(sentence, vectors, n):
    scores = []

    #score is list which contents a dictionary for each ngram.
    #Key in dict is language, value is the for for given sentence
    for i in range(0, n):
        scores.append({})
        for language in vectors.keys():
            scores[i][language] = count_ngram_score(sentence, vectors[language], i + 1)

    #result for uni/bi/trigrams - 0 ~ uni etc.
    winners_for_ngram = []  #remebers which language was the best for uni, bi and trigram
    detected_languages = collections.defaultdict(int)  #key = best lang for some ngram, value is number (countet rate)
    for i in range(0, n):
        #find the language with lowes score for i-gram
        best_language = min(scores[i].items(), key=operator.itemgetter(1))[0]
        #ngram_rate tell us how much more important is the result by trigram then by unigram etc.
        #notice and add rate if for ngram is the language the best
        detected_languages[best_language] += (i + 1) * ngram_rate
        winners_for_ngram.append(best_language)

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


#main:
#command line inputs and default setting od vectors file
"""
if len(sys.argv) > 2:
	sentence = sys.argv[1]
	vector_file = sys.argv[2]
elif len(sys.argv) == 2:
	sentence = sys.argv[1]
	vector_file = "language_vector.p"
else:
	sentence = input("Your sentence: ")
	vector_file = "language_vector.p"

vectors = langVector.load_vector(vector_file)
language, probability = recognize_language(sentence, vectors, number_of_ngrams)
print("Given sentence is in",language, "(with", probability*100, "% probability)")

"""