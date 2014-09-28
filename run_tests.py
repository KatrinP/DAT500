from occurence import Occurence
from tests import createTestFile


def createTestFiles():
    createTestFile("tests_create/cze1.txt", "tests/cze1.txt")
    # more commands like this


def testFiles():
    a = ""
    # testFile("tests/cze1.txt", "test_results/cze1.txt")
    #more commands like this


def generateOccurences():
    oc = Occurence()
    dict1 = oc.count("test_results/cze1.txt");
    # etc than create and fill csv file


createTestFiles()
testFiles()
generateOccurences()
