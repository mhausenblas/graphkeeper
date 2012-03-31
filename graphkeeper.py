"""
GraphKeeper, a simple RDF store in ZooKeeper.
Michael Hausenblas, DERI
Public Domain
Documentation: 
  https://github.com/mhausenblas/graphkeeper
"""
import zookeeper, threading, ntriples, urllib, sys
try:
    import json
except ImportError:
    import simplejson as json
from pprint import pprint
import logging
_logger = logging.getLogger('gk')
_logger.setLevel(logging.DEBUG)
_handler = logging.StreamHandler()
_handler.setFormatter(logging.Formatter('%(levelname)s::%(name)s: %(message)s'))
_logger.addHandler(_handler)

ZOO_OPEN_ACL_UNSAFE = {"perms":0x1f, "scheme":"world", "id" :"anyone"};

class GraphKeeper(object):
	
	SERVER_PORT = 2181

	def __init__(self):
		self.host = "localhost:%d" % self.SERVER_PORT
		self.connected = False
		self.handle = -1
		try:
			f = open('gk.log','w')
			zookeeper.set_log_stream(f)
		except IOError:
			_logger.debug('Couldn\'t open logfile for writing')

	
	def set_up(self):
		self.cv = threading.Condition()
		self.connected = False
		def connection_watcher(handle, type, state, path):
			self.cv.acquire()
			self.connected = True
			self.cv.notify()
			self.cv.release()
		self.cv.acquire()
		self.handle = zookeeper.init(self.host, connection_watcher)
		self.cv.wait(10.0)
		self.cv.release()
		if not self.connected:
			raise Exception("Couldn't connect to host -", self.host)

		# set up the NG2znode look-up table:
		if not zookeeper.exists(self.handle, '/look-up', None):
			d = { 'default-graph' : '/dg' }
			zookeeper.create(self.handle, '/look-up', json.dumps(d), [ZOO_OPEN_ACL_UNSAFE])
		else:
			(self.NG2znode, stat) = zookeeper.get(self.handle, '/look-up', None)
			self.NG2znode =  json.loads(str(self.NG2znode))
			_logger.debug('%s' %self.NG2znode['default-graph'])

	
	def shut_down(self):
		if self.connected:
			zookeeper.close(self.handle)	

	
	def exists_ng(self, ng):
		return zookeeper.exists(self.handle, ng, None)
	
	def get_ng(self, ng):
		return zookeeper.get(self.handle, ng, None)

	# adds a named graph and overwrites the content in case it exists already
	def put_ng(self, ng, val):
		# create the new znode that holds the graph data
		payload = { 'graph' : ng , 'data' : val }
		znode_id = zookeeper.create(self.handle, '/ng', json.dumps(payload), [ZOO_OPEN_ACL_UNSAFE], zookeeper.SEQUENCE)
		# now update mNG2znode look-up table:
		(self.NG2znode, stat) = zookeeper.get(self.handle, '/look-up', None)
		self.NG2znode =  json.loads(str(self.NG2znode))
		self.NG2znode[ng] = znode_id
		zookeeper.set(self.handle, '/look-up', json.dumps(self.NG2znode))

	def import_dataset(self, uri):
		parser = ntriples.NTriplesParser(sink=GKSink())
		u = urllib.urlopen(uri)
		s = parser.parse(u)
		u.close()
		
		for ng in s.ng:
			print ng
			print s.ng[ng]
			self.put_ng(ng, s.ng[ng])

class GKSink(object): 
	def __init__(self): 
		self.length = 0
		self.ng = {}
	
	def ser(self, s, p, o):
		if type(s) == ntriples.URI: s = '<' + s + '>'
		if type(p) == ntriples.URI: p = '<' + p + '>'
		if type(o) == ntriples.URI: o = '<' + o + '>'
		if type(o) == ntriples.Literal: o = '"' + o + '"'
		return (s, p, o)
		
	def triple(self, s, p, o): 
		self.length += 1
		(s, p, o) = self.ser(s, p, o)
		if s in self.ng:
			self.ng[s] = self.ng[s] + '\n' + s + ' ' + p + ' ' + o + ' .'
		else:
			self.ng[s] = s + ' ' + p + ' ' + o + ' .'
		
if __name__ == '__main__':
	gk = GraphKeeper()
	gk.set_up()
	gk.import_dataset('test/dataset0.nt')