import codecs
# string source_file, string newFile
def createTestFile(sourceFile, newFile):
    file = codecs.open(sourceFile, encoding="utf-8")
    str = ""
    for line in file:
        str += line
    str = str.replace('. ', '.')  # i dont want to start lines with space
    str = str.replace('\n\r', '')
    str = str.replace('\n', '')
    str = str.replace('\r', '')
    output = str.split('.')
    newFile = codecs.open(newFile, 'w+', encoding="utf-8")  # output file
    firstline = next(output)  # first line withnout newline on end. new line char added to old line with every new line
    newFile.write(firstline + '.')
    for outText in output:
        if (outText != ""):
            newFile.write('\n\r' + outText + '.')
    file.close()
    newFile.close()


    # createTestFile("tests_create/cze1.txt", "tests/cze1.txt")