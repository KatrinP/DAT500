import sys

from occurence import Occurence
from tests import createTestFile
from tests import testFile


def createTestFiles():
    createTestFile("tests_create/cze1.txt", "tests/cze1.txt")
    # more commands like this


def testFiles():
    testFile("tests/cze1.txt", "test_results/cze1.txt")
    #more commands like this


def generateOccurences():
    oc = Occurence()
    dict1 = oc.count("test_results/cze1.txt");
    # etc than create and fill csv file
    print(dict1)

if __name__ == "__main__":

	createTestFiles()
	testFiles()
	generateOccurences()

	sys.exit(0)
