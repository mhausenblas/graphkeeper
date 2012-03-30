# GraphKeeper - a simple, distributed RDF store in ZooKeeper 

_GraphKeeper_ is a simple, distributed RDF store in ZooKeeper. Read the [design notes](http://scriptogr.am/mhausenblas/post/rdf-store-in-zookeeper-part-1 "A simple RDF store in ZooKeeper - Part 1") first to get an idea. 

## Dependencies and configuration

This software has been developed and tested under MacOS Lion. I'm using [ZooKeeper 3.3.5](http://ftp.heanet.ie/mirrors/www.apache.org/dist/zookeeper/zookeeper-3.3.5/zookeeper-3.3.5.tar.gz) with [Python bindings](http://pypi.python.org/pypi/zc-zookeeper-static/3.3.5 "zc-zookeeper-static 3.3.5 : Python Package Index") in an Python 2.7.1 environment. I have the following content in `conf/zoo.cfg` in the ZooKeeper home dir:

	tickTime=2000
	initLimit=10
	syncLimit=5
	dataDir=tmp
	clientPort=2181

## Usage

To launch GraphKeeper you have to initially `chmod 755 gk-launch.sh` once and set the path to your ZooKeeper installation. Then you can `./gk-launch.sh` to fire up ZooKeeper and after which you should see something like:

	JMX enabled by default
	Using config: /Users/michael/Documents/dev/zookeeper-3.3.5/bin/../conf/zoo.cfg
	-n Starting zookeeper ... 
	STARTED

Then you can try out GraphKeeper and you should see:

	$ python graphkeeper.py
	Set up of GraphKeeper ...
	<http://data.example.org/person/tim> dc:publisher "Tim" .

To shut down GraphKeeper you do `chmod 755 gk-shutdown.sh` once and then you can `./gk-shutdown.sh` it.

## Todo

* Payload codec
* Named graph to znode look-up table
* TriG parsing

## License

The software provided here is in the Public Domain.