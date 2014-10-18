import codecs
# from reads input file and creates new one. on every line of new file is one sentence
# string source_file, string outputFile
from language_recognizer import langVector
from language_recognizer.langRecognizer import recognize_language, number_of_ngrams


def createTestFile(inputFileName, outputFileName):
    inputFile = codecs.open(inputFileName, encoding="utf-8")
    outputFile = codecs.open(outputFileName, 'w+', encoding="utf-8")  # creates/rewrites output file
    str = ""
    for line in inputFile:
        str += line
    str = str.replace('. ', '.')  # i dont want to start lines with space
    str = str.replace('\r\n', '')
    str = str.replace('\n', '')
    str = str.replace('"', ' ')
    str = str.replace(';', '.')
    str = str.replace('  ', ' ')
    str = str.replace('\r', '')
    output = str.split('.')
    for outText in output:
        if outText != "":
            outputFile.write(outText + '.' + '\r\n')
    inputFile.close()
    outputFile.close()


def testFile(inputFileName, outputFileName):
    vectors = langVector.load_vector("language_recognizer/language_vector.p")
    inputFile = codecs.open(inputFileName, encoding="utf-8")
    outputFile = codecs.open(outputFileName, 'w+', encoding="utf-8")  # creates/rewrites output file
    for line in inputFile:
        language, probability = recognize_language(line, vectors, number_of_ngrams)
        outputFile.write(language + '\r\n')
    inputFile.close()
    outputFile.close()

# createTestFile("tests_create/cze1.txt", "tests/cze1.txt")

if __name__ == "__main__":
    testFile("tests/cze1.txt", "test_results/cze1.txt")
