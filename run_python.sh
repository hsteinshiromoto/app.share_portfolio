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
	python -m pip install -r /usr/local/requirements.txt
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

# Documentation
display_help() {
    echo "Usage: [variable=value] $0" >&2
    echo
    echo "   -c, --clean                Remove files *.py[co] and __pycache__"
    echo "   -m, --make_dataset         Run make_dataset.py"
    echo "   -h, --help                 Display help"
    echo "   -r, --requirements         Install modules from requirements.txt"
    echo "   -t, --test_environment     Test python environment"
    echo
    # echo some stuff here for the -a or --add-options
    exit 1
}


# Available options
while :
do
    case "$1" in
      -h | --help)
          display_help  # Call your function
          exit 0
          ;;

      -c | --clean)
          clean  # Call your function
          break
          ;;

      -m | --make_dataset)
          jupyter  # Call your function
          break
          ;;

      -r | --requirements)
          deploy_container  # Call your function
          break
          ;;

      -t | --test_environment)
          run_ssh_container  # Call your function
          break
          ;;

      "")
          run_container  # Call your function
          break
          ;;

      --) # End of all options
          shift
          break
          ;;
      -*)
          echo "Error: Unknown option: $1" >&2
          ## or call function display_help
          exit 1
          ;;
      *)  # No more options
          break
          ;;
    esac
done