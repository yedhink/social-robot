#!/usr/bin/env bash

if [ $(which pip3) ]; then
	echo "Using the existing version of pip3 for installation..."
else
	echo "Installating pip3..."
	curl "https://bootstrap.pypa.io/get-pip.py" -o "$HOME/get-pip.py"
	python3 $HOME/get-pip.py
	
	# why sudo though? well connecting to arduino via usb port
	# and controlling it via python needs su previleges. thus
	# installing pypi packages globally(which is not the best practice)
	# can save a lot of overhead
	sudo pip3 install -r ./requirements.txt

	# for testing purposes
	sudo pip3 install --upgrade tensorflow scipy keras
	sudo pip3 install https://github.com/OlafenwaMoses/ImageAI/releases/download/2.0.2/imageai-2.0.2-py3-none-any.whl 
fi
