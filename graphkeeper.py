import zookeeper, threading, sys

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
			print "Couldn't open logfile for writing"

	
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

	
	def shut_down(self):
		if self.connected:
			zookeeper.close(self.handle)	

	
	def exists_ng(self, ng):
		return zookeeper.exists(self.handle, ng, None)
	
	def get_ng(self, ng):
		return zookeeper.get(self.handle, ng, None)

	# adds a named graph and overwrites the content in case it exists already
	def put_ng(self, ng, val):
		zookeeper.create(self.handle, ng, val, [ZOO_OPEN_ACL_UNSAFE], zookeeper.SEQUENCE)
              
if __name__ == '__main__':
	gk = GraphKeeper()
	
	print 'Set up of GraphKeeper ...'
	gk.set_up()
	
	gk.put_ng('/ng', '<http://data.example.org/person/tim> dc:publisher "Tim" .')
	
	(data, stat) = gk.get_ng('/ng-0') 
	print data