#!/bin/bash

## Test python environment is setup correctly
if [[ $1 = "test_environment" ]]; then
	echo ">>> Testing Python Environment"
	/usr/local/bin/test_environment.py
fi

## Install Python Dependencies
if [[ $1 = "requirements" ]]; then
 	echo ">>> Installing Required Modules .."
 	cd /usr/local/bin/
	python -m pip install -U pip setuptools wheel
	python -m pip install -r /usr/local/bin/requirements.txt
	python -m spacy download en_core_web_sm # Install English language package for spaCy
#	jupyter contrib nbextension install --system
	echo ">>> Done!"
fi

## Make Dataset
if [[ $1 == "data" ]]; then
	bash run_python.sh requirements
	python src/data/make_dataset.py data/raw data/processed
fi

## Delete all compiled Python files
if [[ $1 = "clean" ]]; then
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
fi
