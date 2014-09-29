#!/usr/bin/python

import sys
import os
import tempfile
import subprocess
import math


class Graph:
	def __init__ (self):
		self . _gnuplot_preambule = '''reset
			set term png
			set output "%s"
			set size square
			set isosample 50,50
			set parametric
			set xrange [-1:1]
			set yrange [-1:1]
			set vrange [0:1]
			unset border
			unset xtics
			unset ytics
			unset colorbox
			set view map
			set palette defined(0 "red",1 "green",2 "blue",\\
				3 "yellow",4 "cyan",5 "brown",6 "greenyellow",\\
				7 "gray",8"bisque",9"violet",10"black")
			set cbrange [0:10]
			set multiplot
		'''
		self . _gnuplot_amendment = '''unset multiplot'''

	def is_dict (self, d):
		return isinstance ( d, type( dict () ) )
	def is_str ( self, s ):
		return isinstance ( s, type( str () ) )
	def sign ( self, x ):
		if ( x >= 0 ):
			return 1
		else:
			return -1

	def process ( self, data, output ):
		if not self . is_dict ( data ):
			raise Exception ( "Fatal error. Argument of process() must be a dict" )
		if not self . is_str ( output ):
			raise Exception ( "Fatal error. Argument of process() must be a string" )

		number_of_lines = sum ( data . values () )
		preambule = self . _gnuplot_preambule % output
		amendement = self . _gnuplot_amendment
		try:
			gnuplot_script = tempfile . NamedTemporaryFile ( mode = "w", prefix = "dat500_tmp_", delete = False )
			gnuplot_script . write ( preambule )
			tmp_name = gnuplot_script . name
			i = 0
			u_begin = 0
			for lang in data . keys ():
				piece = float ( data [ lang ] ) / number_of_lines
				percentage = int ( round ( piece, 2 ) * 100 )
				u_end = u_begin + piece

				ang = ( u_begin + u_end ) * math . pi
				x = math . cos ( ang )
				x = x + self . sign ( x ) * 0.3
				y = math . sin ( ang )
				y = y + self . sign ( y ) * 0.3

				gnuplot_script . write ( "set urange [%f*2*pi:%f*2*pi]\n" % (u_begin, u_end) )
				gnuplot_script . write ( "set label %d center \"%s %d%%\" at %f,%f\n" % ( int( i + 1 ), lang, percentage, x, y ) ) 
				gnuplot_script . write ( "splot cos(u)*v, sin(u)*v, %f w pm3d notitle\n" % ( i % 11 ) )

				i = i + 1
				u_begin = u_end

			gnuplot_script . close ()

			cmd = "gnuplot %s" % tmp_name

			p = subprocess.Popen(
				cmd,
				shell=True,
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE)
			output, err = p.communicate()
			p_status = p.wait()
			if p_status != 0:
				raise Exception ( "Fatal error. Can not run subprocess gnuplot. %s" % err )			
		except Exception:
			raise
		finally:
			try:
				gnuplot_script . close ()
			except Exception:
				pass
			os . remove ( tmp_name )


if __name__ == "__main__":

	gr = Graph()

	gr . process ( { "a": 3, "b": 6, "c": 7, "d": 1 }, "pie" )


	sys.exit(0)