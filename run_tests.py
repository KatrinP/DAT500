import sys

from occurence import Occurence
from tests import createTestFile
from tests import testFile


def createTestFiles():
    createTestFile("tests_create/cze1.txt", "tests/cze1.txt")
    createTestFile("tests_create/cze2.txt", "tests/cze2.txt")
    createTestFile("tests_create/de1.txt", "tests/de1.txt")
    createTestFile("tests_create/nor1.txt", "tests/nor1.txt")
    # more commands like this


def testFiles():
    testFile("tests/cze1.txt", "test_results/cze1.txt")
    testFile("tests/cze2.txt", "test_results/cze2.txt")
    testFile("tests/de1.txt", "test_results/de1.txt")
    testFile("tests/nor1.txt", "test_results/nor1.txt")
    #more commands like this


def generateOccurences():
    oc = Occurence()
    dict1 = oc.count("test_results/cze1.txt");
    dict2 = oc.count("test_results/cze2.txt");
    dict3 = oc.count("test_results/de1.txt");
    dict4 = oc.count("test_results/nor1.txt");
    # etc than create and fill csv file
    print(dict1)
    print(dict2)
    print(dict3)
    print(dict4)

if __name__ == "__main__":

	createTestFiles()
	testFiles()
	generateOccurences()

	sys.exit(0)
