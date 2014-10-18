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
	exit 1
fi


LANGUAGE_LOWER=$(echo $LANGUAGE | tr "A-Z" "a-z")

for i in 1 2 3
do
/home/hadoop/bin/hadoop jar /home/hadoop/contrib/streaming/hadoop-streaming.jar -Dmapred.reduce.tasks=5 -mapper mapper$i.py -reducer reducer.py -input "$S3"/"$LANGUAGES"/"$LANGUAGE""$WIKI"/"$LANGUAGE".txt -output "$S3"/"$RESULTS"/"$LANGUAGE_LOWER""$WIKI"/$i/ -file /mnt/DAT500/mapper$i.py -file /mnt/DAT500/reducer.py &
done
