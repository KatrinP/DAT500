import codecs
import sys
import re
import os
import subprocess
import math

from occurence import Occurence
from results import Graph
from tests import createTestFile
from tests import testFile
from language_recognizer import langVector
from language_recognizer.langRecognizer import recognize_language, number_of_ngrams

CREATE_DIR = "./tests_create"
TEST_DIR = "./tests"
RESULT_DIR = "./tests_results"
GRAPH_DIR = "./tests_graphs"
CSV_DIR = "./tests_csv"


def is_list( l ):
	return isinstance ( l, type( list () ) )

def createDirs():
	if not os.path.exists(CREATE_DIR):
		os.makedirs(CREATE_DIR)
	if not os.path.exists(TEST_DIR):
		os.makedirs(TEST_DIR)
	if not os.path.exists(RESULT_DIR):
		os.makedirs(RESULT_DIR)
	if not os.path.exists(GRAPH_DIR):
		os.makedirs(GRAPH_DIR)
	if not os.path.exists(CSV_DIR):
		os.makedirs(CSV_DIR)

def getFiles( dirname ):
	outfiles = []
	if not is_list ( dirname ):
		dirname = [ dirname ]
	for d in dirname:
		files = os.listdir(d)
		for f in files:
			outfiles.append(f)

	return outfiles

def createTestFiles ():

	files = getFiles ( CREATE_DIR )

	for f in files:
		createTestFile ( CREATE_DIR + "/" + f, TEST_DIR + "/" + f )


def testFiles ():

	files = getFiles ( TEST_DIR )
	with langVector . Vector ( "vec.json" ) as lv:
		print ( "Vector %s loaded" % "vec.json" )
		vectors = lv . vectors ()
		for f in files:
			testFile( TEST_DIR + "/" + f, RESULT_DIR + "/" + f, vectors )

def determineLang ( filename ):
	lang = [ "cz", "de", "no", "en", "da", "it", "nl", "nn", "ro", "sk", "hr",
			 "bg", "br", "fi", "uk", "pl", "fr", "pt", "ru", "sv", "es" ]

	for l in lang:
		if re . match ( l, filename ):
			return l
	return None


def generateOccurences():

	files = getFiles ( RESULT_DIR )
	oc = Occurence()
	gr = Graph ()
	res = {}
	for f in files:
		res [ f ] = oc . count ( RESULT_DIR + "/" + f )

	results = []
	langs = {}
	for f in res . keys ():
		lang = determineLang ( f )
		results . append ( ( f, res [ f ] ) )
		if lang in langs . keys ():
			for i in res [ f ] . keys ():
				if i in langs [ lang ] . keys ():
					langs [ lang ] [ i ] += res [ f ] [ i ]
				else:
					langs [ lang ] [ i ] = res [ f ] [ i ]
		else:
			langs [ lang ] = res [ f ]


	for lang in langs . keys ():
		gr . process ( langs [ lang ], GRAPH_DIR + "/" + lang + ".png" )

	return results


def generateCSV(results):
	outputFile = codecs.open( CSV_DIR + "/graphs.csv", 'w+', encoding="utf-8")  # creates/rewrites output file
	for (rightLang, result) in results:
		outputFile.write(rightLang + '\r\n')
		for lang in result:  # languages
			outputFile.write(lang + ',')
		outputFile.write('\r\n')  # newline
		for lang in result:  # counts
			outputFile.write( str(result[lang]) + ',')
		outputFile.write('\r\n')
	outputFile.close()


if __name__ == "__main__":

	print ( "Creating dirs ... " )
	createDirs()
	print ( "done" )
	print ( "Creating test files ... " )
	createTestFiles()
	print ( "done" );
	print ( "Testing files" )
	testFiles()
	print ( "done" );
	print ( "Generating occurences and printing charts ... " )
	results = generateOccurences()
	print ( "done" )
	print ( "Generating csv ... " ) 
	generateCSV(results);
	print ( "done" )

	print ( "Bye" )

	sys.exit(0)

