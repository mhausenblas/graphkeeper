"""
gk - CLI for GraphKeeper
Michael Hausenblas, DERI
Public Domain
Documentation: 
  https://github.com/mhausenblas/graphkeeper

Command line usage: 
   python gk.py <URI> - parses data from URI as N-Triples and loads it into the store
"""
from graphkeeper import *

if __name__ == '__main__':
	if len(sys.argv) == 2: 
		# sys.argv[1]
		gk = GraphKeeper()
		print 'Set up of GraphKeeper ...'
		gk.set_up()
		gk.import_dataset('test/dataset0.nt')
		# gk.put_ng('<http://data.example.org/person/tim>', '<http://data.example.org/person/tim> dc:publisher \'Tim\' .')
		# (data, stat) = gk.get_ng('/ng-0') 
		# print data
	else: print __doc__
