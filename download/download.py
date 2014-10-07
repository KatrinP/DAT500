#!/usr/bin/python

## README
# Script for downloading list of articles in particular language 
# from wikipedia.org
#
# Usage:
#	Examples:
#		./script.py --help for usage information
#		./script.py --language nn set the language
#		./script.py --input <directory|file>
#		./script.py --t <number of threads>
#		./script.py --merge merge after threads are done
#		./script.py --delete-after-merger delete thread files and leave only the merged one
#		./script.py -c how many links should threads pick up on every loop
#		./script.py --output . -n "%(lang)s" output will be in actual directory/<lang>
#
#
# Input:
#	File contains on each line name of the wikipedia article.
#	Should be generated by running
#	./links.py --languages fi --limit 50000 -u "%(1)s"
#
#	Note that the -u parameter is the most important
#
#
# @author Kryštof Tulinger
# @year 2014
# -----------------------------------------------------------------------------

import sys
import codecs
import os
import threading
import time
import getopt

from wikipedia import Wikipedia
from wiki2plain import Wiki2Plain


class DownloadThread ( threading . Thread ):
	def __init__ ( self, id, wiki ):
		threading . Thread . __init__ ( self )
		self . _wiki = wiki
		self . _id = id
		self . _file = wiki . outputPathDirectory() + wiki . delim () + wiki . outputPath () % { "lang" : wiki . lang () } + wiki . delim () + "T" + repr ( id ) + ".txt"
		self . _pagebreak = "\r\n"
		self . _links = wiki . numberOfLinks ()
	def stop ( self ):
		self . _Thread__stop ()

	def run ( self ):
		print ( "Thread " + repr ( self . _id ) + " has started" )
		run = False
		with codecs . open ( self . _file, "w", encoding = "utf-8" ) as outputFile:
			while True:
				links = self . _wiki . links ( self . _links )
				if not links:
					break
				for link in links:
					self . _wiki . addCounter ( 1 )
					self . _wiki . addReadBytes ( len ( link . encode ( "utf-8" ) ) + len ( self . _pagebreak .encode ( "utf-8" ) ) )
					try:
						raw = self . _wiki . wiki () . article ( link )
						plain = Wiki2Plain ( raw )
						outputFile . write ( plain . text )
						outputFile . write ( self . _pagebreak + self . _pagebreak )
						self . _wiki . stats ()
					except:
						print ( "Article " + repr(link.encode("utf-8")) + " does not exists" )
				run = True

		if run:
			sys . stdout . write ( "\n" )
		print ( "Thread " + repr ( self . _id ) + " has finished" )

class DownloadWiki:
	def __init__ ( self, lang ):
		self . _bytes = 0;
		self . _readBytes = 0;
		self . _counter = 0;
        self._wiki = Wikipedia(lang)


		self . _linkFiles = []
		self . _openFile = None

		self . _locker = threading . Lock ()

		self . _start = None
		self . _lang = lang
		self . _verbose = False
		self . _delete_after_merge = False
		self . _merge_files = True
		self . _number_of_links = 500

		self . _delim = "\\"
		if sys . platform . startswith ( 'linux' ):
			self . _delim= "/"

		self . _outputPathDirectory = None
		self . _outputPath = "." + self . _delim + "%(lang)s" # %s for language

	def options ( self, options = {} ):
		if "wiki" in options.keys():
			self . _wiki = options[ "wiki" ]
		if "link_file" in options.keys():
			self . _linkFiles = options[ "link_file" ]
		if "output_path_directory" in options . keys():
			self . _outputPathDirectory = options[ "output_path_directory" ]
		if "output_path" in options . keys():
			self . _outputPath = options[ "output_path" ]
		if "verbose" in options . keys():
			self . _verbose = options[ "verbose" ]
		if "merge" in options . keys():
			self . _merge_files = options[ "merge" ]
		if "delete_after_merge" in options . keys():
			self . _delete_after_merge = options[ "delete_after_merge" ]
		if "number_of_links" in options . keys():
			self . _number_of_links = options[ "number_of_links" ]
		if "split_files" in options . keys():
			self . _split_files = int ( options[ "split_files" ] )


	def is_list ( self, s ):
		"""
			Check if @param s is a type of list
		"""
		return isinstance ( s, type( list () ) )

	def is_str ( self, s ):
		"""
			Check if @param s is a type of str
		"""
		return isinstance ( s, type( str () ) )

    def addReadBytes ( self, b ):
		self . _locker . acquire ();
		self . _readBytes = self . _readBytes + b
		self . _locker . release ();
	def addCounter ( self, c ):
		self . _locker . acquire ();
		self . _counter = self . _counter + c
		self . _locker . release ();
	def counter ( self ):
		return self . _counter
	def readBytes ( self ):
		return self . _readBytes
	def bytes ( self ):
		if not self . _bytes:
			return 1
		return self . _bytes
	def speed ( self ):
		return self . counter () / (time . time () - self . _start);
	def duration ( self ):
		return (time . time () - self . _start) * ( self . bytes () - self . readBytes () ) / self . readBytes()
	def outputPathDirectory ( self ):
		return self . _outputPathDirectory
	def outputPath ( self ):
		return self . _outputPath
	def delim ( self ):
		return self . _delim
	def numberOfLinks ( self ):
		return self . _number_of_links
	def lang ( self ):
		return self . _lang

	def wiki ( self ):
		return self . _wiki

	def stats ( self ):
		duration = self . duration ()
		mode = 's'
		if ( duration > 60 and duration <= 3600 ):
			mode = 'm'
			duration = int ( duration / 60 )
		elif ( duration > 3600 ):
			mode = 'h'
			duration = duration / 3600
        sys.stdout.write(
            "\r%d%% [%d/%d] (%d) %.4f l/s. Remaining %.2f%c." % ( int(self.readBytes() * 100 / self.bytes()),
                                                                  self.readBytes(),
                                                                  self . bytes(),
																			    self . counter(),
																			    self . speed(),
																			    duration,
																			    mode ) )
	def links ( self, n ):
		self . _locker . acquire ()
		links = []
		i = 0
		while i != n and not self . _openFile . closed:
			line = self . _openFile . readline ()
			if not line:
				if len ( self . _linkFiles ) <= 0:
					break
				self . _openFile . close ()
				self . _linkFiles = self . _linkFiles [ :-1 ]
				if len ( self . _linkFiles ) > 0:
					self . _openFile = codecs . open ( self . _linkFiles [ -1 ], "r", encoding = "utf-8" )
					line = self . _openFile . readline ()
			if not line:
				break

			line = line . strip ()

			links . append ( line )

			i = i + 1

		if len ( links ) <= 0:
			links = None

		self . _locker . release ()

		return links

	def files ( self, inputPath ):
		if self . is_list ( inputPath ):
			newlist = []
			for f in inputPath:
				if not os . path . isfile ( f ):
					for g in os . listdir ( f ):
						if os . path . isfile ( f + self . _delim + g ):
							newlist . append ( f + self . _delim + g )
				else:
					newlist . append ( f )
			inputPath = newlist
		elif self . is_str ( inputPath ):
			if os . path . isfile ( inputPath ):
				if not self . _outputPathDirectory:
					self . _outputPathDirectory = inputPath [ :inputPath . rfind ( self . _delim ) ]
					if len ( self . _outputPathDirectory ) > 0 and self . _outputPathDirectory [ -1 ] == self . _delim:
                        self._outputPathDirectory = self._outputPathDirectory[:-1]
				inputPath = [ inputPath ]
			else:
				try:
					if not self . _outputPathDirectory:
						self . _outputPathDirectory = inputPath
					inputPath = [inputPath + self . _delim + f for f in os . listdir ( inputPath ) if os . path . isfile ( inputPath + self . _delim + f )]
				except Exception as inst:
					print ( "Fatal error." )
					raise
		return inputPath

	def download ( self, inputPath = [], nthreads = 5 ):

		inputPath = self . files ( inputPath )

		if not self . is_list ( inputPath ):
            raise Exception("Fatal error. Download (): invalid argument")

		if len ( inputPath ) <= 0:
			raise Exception ( "Fatal error. Download (): invalid argument. No files." )

		if not os . path . exists ( self . _outputPathDirectory + self . _delim + self . _outputPath % { "lang" : self . _lang } ):
			os . makedirs ( self . _outputPathDirectory + self . _delim + self . _outputPath % { "lang" : self . _lang } )

		self . _linkFiles = inputPath
		self . _openFile = codecs . open ( self . _linkFiles [ -1 ], "r", "utf-8" )
		self . _start = time . time ()

		for f in self . _linkFiles:
			self . _bytes = self . _bytes + os . stat ( f ) . st_size

		threads = []
		for i in range ( nthreads ):
			thread = DownloadThread( i, self )
			thread . name = "Thread " + repr ( i )
			thread . daemon = True
			threads . append ( thread )
			thread . start ()

		for t in threads:
			t . join ()

		if self . _merge_files:
			self . merge ()

		print ( "Exiting" )

	def merge ( self ):
        folder = self._outputPathDirectory + self._delim + self._outputPath % {"lang": self._lang}
		files = os . listdir ( folder )

		merged_name = self . _lang + ".txt"

		if self . _verbose:
			print ( "Merging" )

		chunks = 8192
		with codecs . open ( folder + self . _delim + merged_name, "w", encoding = "utf-8" ) as outputFile:
			for f in files:
				if f == merged_name:
					continue
				with codecs . open ( folder + self . _delim + f, "r", encoding = "utf-8" ) as inputFile:
					while True:
						data = inputFile . read ( chunks )
						if not data:
							break
						if self . _verbose:
							pass
						#sys . stdout . write ( "\r%f%% [%d/%d]" % ( round(readed*100/content_length), readed, content_length) )
						outputFile . write ( data )
				if self . _delete_after_merge:
					os . delete ( folder + self . _delim + f )
		if self . _verbose:
			print ( "Files merged to " + folder + self . _delim + merged_name )




def main ( argv = None ):

	def usage ():
		print ( "Usage: " + sys.argv[0] + " [options]" )
		print ( "" )
		print ( "Options:" )
		print ( "	--help|-h			show this help message and exit" )
		print ( "	--input|-i <dir>		set the input file/directory" )
		print ( "	--output|-o <dir|file>		set the output directory, default is the same as input" )
		print ( "	--language|-l <lang>		set the language" )
		print ( "	--merge|-m			set if the thread files should be merged after complete run" )
		print ( "	--delete-after-merge		set if thread files should be deleted after complete run" )
		print ( "	--name|-n <name>		set the subdirectory of output directory where the results will be stored; %(lang)s can be used" )
		print ( "	--threads|-t <number>		number of threads" )
		print ( "	--number-of-links <number>	number of links processed by thread in a loop" )
		print ( "" )
		print ( "Examples:" )
		print ( "	script.py --input ..\\languages\\nowiki\\ -t 8 --merge -c 500 -l nn" )
		print ( "	script.py --input ..\\languages\\nowiki\\nn.links.txt.00000000.txt -t 8 --merge --delete-after-merge -c 20 -l nn" )


	if not argv:
		argv = sys . argv

	options = {}
	threads = 5
	input = []
	lang = None

	if argv is None:
		argv = sys.argv
	try:
		opts, args = getopt.getopt(
			argv[1:], "hvl:o:i:mdn:t:c:", [
				"help", "language=", "input=", "output=",
				"merge", "delete-after-merge", "name=", "threads=" "number-of-links=" ])
	except getopt.GetoptError:
		usage ()
		return 0
	for opt, arg in opts:
		if opt in ('-h', '--help'):
			usage ()
			return 0
		elif opt in ("--language", "-l"):
			lang = str ( arg )
		elif opt in ("--input", "-i"):
			input = arg
		elif opt in ("--output", "-o"):
			options [ "output_path_directory" ] = arg
		elif opt in ("--name", "-n"):
			options [ "output_path" ] = arg
		elif opt in ("--merge", "-m"):
			options [ "merge" ] = True
		elif opt in ("--delete-after-merge", "-d"):
			options [ "delete_after_merge" ] = True
		elif opt in ("--number-of-links", "-c"):
			options [ "number_of_links" ] = int ( arg )
		elif opt in ("--threads", "-t"):
			threads = int ( arg )
		elif opt == "-v":
			options [ "verbose" ] = True
		else:
			assert False, "Fatal error. Bad option."


	if not lang:
		raise Exception ( "Fatal error. No language specified." )

	options [ "verbose" ] = True

	d = DownloadWiki( lang )
	d . options ( options )
	d . download ( input, threads )


	return 0

if __name__ == "__main__":
	sys . exit ( main () )