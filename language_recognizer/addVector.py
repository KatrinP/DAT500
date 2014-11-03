import sys

import langVector


if len(sys.argv) < 3:
    print("Error: missing arguments (language or source file with train plain text)")
elif len(sys.argv) < 4:
    vector_file = "language_vector.p"
    langVector.add_language_vector(sys.argv[1], sys.argv[2], vector_file)
else:
    langVector.add_language_vector(sys.argv[1], sys.argv[2], sys.argv[3])

