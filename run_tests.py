import codecs
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
    # more commands like this


def generateOccurences():
    oc = Occurence()
    results = []
    results.append(("CZE", oc.count("test_results/cze1.txt")))
    results.append(("CZE", oc.count("test_results/cze2.txt")))
    results.append(("DE", oc.count("test_results/de1.txt")))
    results.append(("NOR", oc.count("test_results/nor1.txt")))
    print(results)
    return results


def generateCSV(results):
    outputFile = codecs.open("results/graphs.csv", 'w+', encoding="utf-8")  # creates/rewrites output file
    for (rightLang, result) in results:
        outputFile.write(rightLang + '\r\n')
        for lang in result:  # languages
            outputFile.write(lang + ',')
        outputFile.write('\r\n')  # newline
        for lang in result:  # counts
            outputFile.write(result[lang] + ',')
    outputFile.close()


if __name__ == "__main__":
    createTestFiles()
    testFiles()
    results = generateOccurences()
    generateCSV(results);

sys.exit(0)
