#!/usr/bin/python2.7

from operator import itemgetter
import sys
import codecs

current = None
current_count = 0
ngram = None

sys.stdin = codecs.getreader("utf-8")(sys.stdin)

for line in sys.stdin:
  line = line.strip()
  try:
    ngram, count = line.split('\t', 1)
  except:
    print ( "error: " + line )
    continue
  try:
    count = int(count)
  except ValueError:
    continue

  if current == ngram:
    current_count += count
  else:
    if current:
      print ( '%s\t%s' % (current, current_count) )

    current_count = count
    current = ngram

if current == ngram:
  print ( '%s\t%s' % (current, current_count) )
