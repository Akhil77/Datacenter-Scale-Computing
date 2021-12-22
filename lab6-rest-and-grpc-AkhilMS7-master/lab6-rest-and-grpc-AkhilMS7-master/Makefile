USER=$(shell whoami)

##sudo pip3 install grpcio-tools
## Configure the Hadoop classpath for the GCP dataproc enviornment
##

#HADOOP_CLASSPATH=$(shell hadoop classpath)

run:
	sudo apt-get update
	sudo apt-get install -y python3 python3-pip
	sudo pip3 install --upgrade pip
	pip3 install Flask
	python3 -m pip install --upgrade Pillow
	pip3 install jsonpickle
	pip3 install requests
	python3 -m pip install --upgrade setuptools
	python3 -m pip install --upgrade grpcio
	python3 -m pip install --upgrade grpcio-tools