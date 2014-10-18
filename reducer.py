#!/usr/bin/python2.7

from operator import itemgetter
import sys
import codecs

current = None
current_count = 0
ngram = None

sys.stdin = codecs.getreader("utf-8")(sys.stdin)

for line in sys.stdin: # read input from STDIN
  line = line.strip() # remove leading and trailing whitespace
  try:
    ngram, count = line.split('\t', 1) # parse the input we got from email_count_mapper.py, two words, tab delimited
  except:
    print ( "error: " + line )
    continue
  try: # convert count from str to int, if not possible discard this input
    count = int(count)
  except ValueError:
    continue

  if current == ngram: #this works because mapper output is sorted by key (ngram) by Hadoop before feeding to reducer input
    current_count += count #if email domain hasn't changed continue counting its occurances
  else:
    if current: #if email domain has changed output count for previous email domain to STDOUT and start counting for new email domain
      print ( '%s\t%s' % (current, current_count) )

  current_count = count
  current = ngram

# output the last email domain
if current == ngram:
  print ( '%s\t%s' % (current, current_count) )
