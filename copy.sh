#!/bin/sh

LANGUAGE="$1"
S3=s3://uisbucket/group-4
RESULTS=results
WIKI=wiki
LANGUAGES=languages


if [ "x$LANGUAGE" = "x" ]
then
	echo "Usage:"
	echo "$0 <language>"
	echo ""
	echo "Language <language> has to be stored in $S3/$LANGUGAGES/<language>$WIKI/<language>.txt"
	echo "Results will be after job finishes in $S3/$RESULTS/<language>$WIKI/<ngram>/"
	echo ""
	echo "Mapper and reducer are python files stored in /mnt/DAT500"
	echo "Three mappers must be provided with names as mapper1.py for unigram,"
	echo "mapper2.py for bigram and mapper3.py for trigram"
	echo ""
	echo "This firstly copy the data from s3 to local hadoop filesystem and then back"
	exit 1
fi


LANGUAGE_LOWER=$(echo $LANGUAGE | tr "A-Z" "a-z")

for i in 1 2 3
do
/home/hadoop/bin/hadoop fs -cp /process/"$LANGUAGE"/$i/*  "$S3"/"$RESULTS"/"$LANGUAGE_LOWER""$WIKI"/$i/ &
done
