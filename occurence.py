#!/usr/bin/python

# 3) tridu/metodu ktera jako parametr dostane cestu k souboru, metoda projde soubor 
# a spocita kolikrat se kazdej jazyk vyskytl. 
# vrati jako array/tuple/nejakejBlbejDatovejTypHnusnehoPythonu :P

import sys
import getopt

class NoFileException(Exception):
	def __init__(self, *value):
		self.value = value

	def __str__(self):
		return "" . join(self . value)


class Occurence:
	def __init__ (self):
		self . _languages = {}

	def is_str ( self, s ):
		return isinstance ( s, type( str () ) )

	def add ( self, lang ):
		if lang in self . _languages . keys ():
			self . _languages [ lang ] += 1
		else:
			self . _languages [ lang ] = 1

	def trim ( self, string ):
		if len(string) <= 0:
			return string
		ltrim = 0
		rtrim = len(string)-1
		while string [ ltrim ] == '\n' or string [ ltrim ] == ' ' or string [ ltrim ] == '\r':
			ltrim = ltrim + 1
		while string [ rtrim ] == '\n' or string [ rtrim ] == ' ' or string [ rtrim ] == '\r':
			rtrim = rtrim - 1
		return string [ ltrim:rtrim+1 ]

	
	def count ( self, filename ):
		"""
			Counts occurences of the unique lines in file.

			@param filename (string) filename or (file) python object
			@return Dictionary of distinct lines with counted occurence.
			@throws NoFileException if no file is specified
		"""
		if not filename or not len ( filename ):
			raise NoFileException ( "Fatal error. No input file given" );
		if self . is_str ( filename ):
			fp = open ( filename, "r" )
		else:
			fp = filename

		if not fp:
			raise NoFileException ( "Fatal error. File does not exist or has bad permitions" )

		self . _languages = {}

		try:
			for line in fp:
				self . add ( self . trim ( line ) )
		finally:
			fp . close ()

		return self . _languages;


def main ( argv = None ):

	filename = None

	if argv is None:
		argv = sys.argv
	try:
		opts, args = getopt.getopt( argv[1:], "hf:", [ "help", "file=" ] )
	except getopt.GetoptError:
		print ("Usage: " + sys.argv[0] + \
			" [-h|-f <file>|--file <file>]")
		return 0
	for opt, arg in opts:
		if opt in ('-h', '--help'):
			print ("Usage: " + sys.argv[0] + " [options]")
			print ("")
			print ("Options:")
			print ("	-h|								  show this help " \
				"message and exit")
			print ("	-f|--file <file>						   print " \
				"count occurences in file <file>")
			return 0
		elif opt in ( '-f', '--file' ):
			filename = arg

	counter = Occurence();

	print (counter.count ( filename ));

	return 0

if __name__ == "__main__":
	sys.exit( main () )
