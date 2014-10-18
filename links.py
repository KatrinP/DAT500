#!/usr/bin/python

## README
# Script for downloading list of articles in particular language 
# from wikipedia.org
#
# Usage:
#	Examples:
#		./script.py --help for usage information
#		./script.py --language cs,uk,fi for downloading languages with abbrevitation "cs", "uk", "fi"
#		./script.py --language "cs, uk, fi" for using spaces, put the list in quotation marks
#		./script.py --language cs,uk,fk --skip skip non existing urls
#		./script.py --language cs,uk,fi --update download only languages which has not been downloaded yet
#		./script.py --language cs --name "example-name-of-%(0)s-file.txt" use different template for naming output files
#		./script.py --language cs --directory "./lng/" use different directory to store results
#
#	Note that in templates "%(0)s" can be used for inserting the current processed language
#		Example:
#			./script.py -l cs,sk -n "%(0)s.file.txt" will produce files cs.file.txt and sk.file.txt in target directory
#
# @author Kryštof Tulinger
# @year 2014
# -----------------------------------------------------------------------------


import sys
import os
import urllib.request as urllib
import bz2
import tempfile
import codecs
import getopt
import html.parser as HTMLParser
import re

class Download:
	def __init__ ( self ):
		self . _langs = [ "en",
						  "sv",
						  "nl",
						  "de",
						  "fr",
						  "ru",
						  "it",
						  "es",
						  "pl",
						  "ja",
						  "pt",
						  "uk",
						  "zh",
						  "ca",
						  "no",
						  "nn",
						  "fi",
						  "cs",
						  "sk",
						  "da",
						  "bg",
						  "cy", # welsh
						  "ur" 	# urdu 
						  ]
		self . _index_file = "http://dumps.wikimedia.org/%(0)swiki/latest/%(0)swiki-latest-pages-articles-multistream-index.txt.bz2"
		self . _build_url = "http://%(0)s.wikipedia.org/wiki/%(1)s"
		self . _destination_dir = "./languages/%(0)swiki"
		self . _destination_template = "%(0)s.links.txt"
		self . _verbose = True
		self . _skip_non_existent = False
		self . _update = False
		self . _split_files = 50000
		self . _HTMLparser = HTMLParser . HTMLParser ()

	def options ( self, options = {} ):
		if "languages" in options.keys():
			self . _langs = options[ "languages" ]
		if "index_file" in options.keys():
			self . _index_file = options[ "index_file" ]
		if "build_url" in options . keys():
			self . _build_url = options[ "build_url" ]
		if "destination_dir" in options . keys():
			self . _destination_dir = options[ "destination_dir" ]
		if "destination_template" in options . keys():
			self . _destination_template = options[ "destination_template" ]
		if "verbose" in options . keys():
			self . _verbose = options[ "verbose" ]
		if "skip" in options . keys():
			self . _skip_non_existent = options[ "skip" ]
		if "update" in options . keys():
			self . _update = options[ "update" ]
		if "split_files" in options . keys():
			self . _split_files = int ( options[ "split_files" ] )
		
	def langs ( self ):
		"""
			Getter for langs
		"""
		return self . _langs

	def createWiki ( self, lang ):
		"""
			Creates a wiki abbrevitation from the language abbrevitation
			@param lang wiki language
		"""
		return lang . replace ( "-", "_" )

	def is_list ( self, s ):
		"""
			Check if @param s is a type of list
		"""
		return isinstance ( s, type( list () ) )


	def urlretrieve ( self, url ):
		"""
			Downloads a given url to temporary file
			Also displays the progress of downloading
			@param url given url
			@return tuple of opened file with content from url and a byte-size of the content
		"""
		out = tempfile . NamedTemporaryFile ( "r+b", prefix = "dat500_tmp_" )
		try:
			inp = urllib . urlopen ( url )
		except urllib.HTTPError as inst:
			print ( "Fatal error. On url " + url )
			out . close ()
			raise
		content_length = int ( inp . info () [ "Content-Length" ] )
		if self . _verbose:
			print ( "Downloading %s" % url )
		chunks = 8192
		readed = 0
		while True:
			data = inp . read ( chunks )
			if not data:
				break
			if readed + chunks > content_length:
				readed = content_length
			else:
				readed = readed + chunks
			if self . _verbose:
				sys . stdout . write ( "\r%f%% [%d/%d]" % ( round(readed*100/content_length), readed, content_length) )
			out . write ( data )
		out . seek ( 0 )
		if self . _verbose:
			print ( "" );
		return ( out, content_length )

	def get ( self, lang ):
		"""
			Downloads and decompress list of articles in selected language
			@param lang abbrevitation of language from wikipedia
			@return open decompressed file in encoding utf-8 @see decompress()
		"""
		wiki = self . createWiki ( lang )
		url = self . _index_file % { "0": wiki }
		( filename, size ) = self . urlretrieve ( url )
		return self . decompress ( filename, size )

	def decompress ( self, inp, size = 0 ):
		"""
			Decompress the input file @param inp by using bz2 decompression
			@param size does not play a big role
			@return open decompressed file with encoding utf-8
		"""
		out = tempfile . NamedTemporaryFile ( "r+b", prefix = "dat500_tmp_", delete = False )
		content_length = size
		if self . _verbose:
			print ( "Decompressing %s" % inp . name )
		chunks = 8192
		readed = 0
		with bz2.BZ2File ( inp . name, "rb" ) as input:
			while True:
				data = input . read ( chunks )
				if not data:
					break
				if readed + chunks > content_length:
					readed = content_length
				else:
					readed = readed + chunks
				if size and self . _verbose:
					sys . stdout . write ( "\r%f%% [%d/%d]" % ( round(readed*100/content_length), readed, content_length) )
				out . write ( data )
		if size and self . _verbose:
			print ( "" );
		filename = out . name
		out . close ()
		inp . close ()

		return codecs . open ( out . name,  encoding="utf-8" )

	def buildUrl ( self, lang, article ):
		"""
			Creates an url for article in given language
			@param lang language
			@param article name of the article
			@return created url which follows format given by member variable
		"""
		article = article . split ( ":" )
		if len ( article ) > 3:
			return None
		article = article [ 2: ]
		article = ":" . join ( article )
		url = self . _build_url % { "0" : lang, "1" : article }
		url = re . sub ( r'(&.+?;)', lambda m: self . _HTMLparser . unescape ( m . group () ), url )
		# url = urllib . quote ( url )
		return url

	def download ( self, lang = None ):
		"""
			Downloads whole collection of languages given by member variable @var _languages
			or from list given by @param lang
			By default, creates a directory tree:
			- ./languages
				- <abb>wiki [nnwiki]
					- <abb>.links.txt [nn.links.txt]
				- <abb>wiki [nowiki]
					- <abb>.links.txt [no.links.txt]
			this can be changed through member variables _destination_dir and _destination_template
		"""
		if lang is None or not self . is_list ( lang ):
			langs = self . _langs
		else:
			langs = lang
		apendix = ".%08d.txt"
		limit = 0
		line_count = 0
		for lang in langs:
			
			save_path = self . _destination_dir % { "0": lang }
			destination_path = save_path + "/" + self . _destination_template % { "0": lang }

			if self . _update and \
			   ( ( os . path . isfile ( destination_path ) and \
				   os . access ( destination_path, os . W_OK ) ) or (\
				 ( os . path . isfile ( (destination_path + apendix) % 0 ) and \
				   os . access ( (destination_path + apendix)  % 0, os . W_OK ) ) ) ) and (\
			   self . _destination_dir . find ( "%(0)s" ) != -1 or \
			   self . _destination_template . find ( "%(0)s" ) != -1 ):
				print ( "Language \"%s\" has been already downloaded. Skiping." % lang )
				continue

			if self . _destination_dir . find ( "%(0)s" ) == -1 and \
			   self . _destination_template . find ( "%(0)s" ) == -1:
			   line_count = limit * self . _split_files
			   if limit:
			   	destination_path = destination_path + apendix
			else:
				line_count = 0
				limit = 0

			try:
				rawfile = self . get ( lang )
			except urllib.HTTPError as inst:
				if not self . _skip_non_existent:
					raise
				if self . _verbose:
					print ( "Skiping \"%s\". Url does not exist." % lang )
				continue

			if not os . path . exists ( save_path ):
				os . makedirs ( save_path )

			if self . _verbose:
				print ( "Generating \"%s\" files" % lang )

			for line in rawfile:
				if line_count >= limit * self . _split_files:
					if limit == 1:
						output . close ()
						new_path = destination_path + apendix
						if os . path . isfile ( new_path % ( limit - 1 ) ):
							os . remove ( new_path % ( limit - 1 ) )
						os . rename ( destination_path, new_path % ( limit - 1 ) )
						destination_path = new_path

					if limit > 0:
						if not output . closed:
							output . close ()
						new_path = destination_path % ( limit )
					else:
						new_path = destination_path

					if self . _destination_dir . find ( "%(0)s" ) == -1 and \
					   self . _destination_template . find ( "%(0)s" ) == -1:
						# if name of the file is not parameterized by lang
						# we will append the data to the destination file
						output = codecs . open ( new_path, "a", encoding = "utf-8" )
					else:
						# otherwise we rewrite the destination file
						output = codecs . open ( new_path, "w", encoding = "utf-8" )
					limit = limit + 1

				line = line . strip ()
				url = self . buildUrl ( lang, line )
				if not url:
					continue
				output . write ( url + "\r\n" )
				line_count = line_count + 1
			if self . _verbose:
				if limit:
					print ( "%d files generated in directory \"%s\"" % ( limit, save_path ) )
					print ( "%d lines saved totally" % line_count )
				else:
					print ( "%d lines saved in file \"%s\"" % ( line_count, new_path ) )
			output . close ()
			name = rawfile . name
			rawfile . close ();
			os . remove ( name )

	def console ( self, lang = None ):
		"""
			Downloads whole collection of languages given by member variable @var _languages
			or from list given by @param lang and sends it to the stdout
		"""
		if lang is None or not self . is_list ( lang ):
			langs = self . _langs
		else:
			langs = lang

		for lang in langs:
			rawfile = self . get ( lang )

			for line in rawfile:
				line = line . strip ()
				url = self . buildUrl ( lang, line )
				if not url:
					continue
				print ( url . encode ( "utf-8" ) )
			name = rawfile . name
			rawfile . close ();
			os . remove ( name )		


def main ( argv = None ):
	console = None

	options = {}

	if argv is None:
		argv = sys.argv
	try:
		opts, args = getopt.getopt(
			argv[1:], "hal:d:n:u:cv", [
				"help", "all", "languages=", "directory=",
				"name=", "url=", "console", "skip", "update", "limit=" ])
	except getopt.GetoptError:
		print ( "Usage: " + sys.argv[0] + \
			" [-h|--help, -a|--all, " + \
			"--directory|-d <dir>, --name|-n <file>, " + \
			"--console|-c, --build_url|-u, --languages|-l <list>, --skip, --limit <n>]" )
		return 0
	for opt, arg in opts:
		if opt in ('-h', '--help'):
			print ( "Usage: " + sys.argv[0] + " [options]" )
			print ( "" )
			print ( "Options:" )
			print ( "	-h|--help			show this help message and exit" )
			print ( "	--all|-a			download default set of languages" )
			print ( "	--directory|-d <dir>		specify the target directory" )
			print ( "	--name|-n <file>		specify the target file template" )
			print ( "	--build_url|-u <file>		specify the article template for urls" )
			print ( "	--languages|-l <list>		specify a different set of languages, in quotation marks, divided by comma" )
			print ( "					no quotation marks lead to undefined behaviour")
			print ( "	-c|--console			print the results to stdout instead of files specified with others parameters" )
			print ( "	-q				quiet" )
			print ( "	--skip				skip non existing urls" )
			print ( "	--update			skip files which has been already downloaded, works if at least on of -n or -d is parameterized" )
			print ( "	--limit <n>			split the target file into files after each <n-th> line" )
			print ( "" )
			print ( "	Note that by -d, -n, -u, \"%(0)s\" can be used to replace current processed language" )
			return 0
		elif opt in ("--all", "-a"):
			options [ "languages" ] = None
		elif opt in ("--name", "-n"):
			options [ "destination_template" ] = arg
		elif opt in ("--directory", "-d"):
			options [ "destination_dir" ] = arg
		elif opt in ("--url", "-u"):
			options [ "build_url" ] = arg
		elif opt in ("--console", "-c"):
			console = True
		elif opt == "-v":
			options [ "verbose" ] = False
		elif opt == "--skip":
			options [ "skip" ] = True
		elif opt == "--update":
			options [ "update" ] = True
		elif opt == "--limit":
			options [ "split_files" ] = arg
		elif opt in ("--languages", "-l"):
			l = arg . split ( "," )
			l = [ lg.strip() for lg in l ]
			options [ "languages" ] = l
		else:
			assert False, "Non existing option"


	d = Download ()
	d . options ( options )

	if console:
		d . console ()
	else:
		d . download ()

	return 0

if __name__ == "__main__":

	sys . exit ( main () );
