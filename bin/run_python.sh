#!/bin/bash

## Test python environment is setup correctly
test_environment () {
  echo ">>> Testing Python Environment"
  /usr/local/bin/test_environment.py
}

## Install Python Dependencies
requirements () {
  echo ">>> Installing Required Modules .."
  cd /usr/local/bin/
  python -m pip install -U pip setuptools wheel
  python -m pip install -r /usr/local/requirements.txt
  echo ">>> Done!"
}

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
      -h | --help | "")
          display_help  # Call your function
          exit 0
          ;;

      -c | --clean)
          clean  # Call your function
          break
          ;;

      -m | --make_dataset)
          make_dataset  # Call your function
          break
          ;;

      -r | --requirements)
          requirements  # Call your function
          break
          ;;

      -t | --test_environment)
          test_environment  # Call your function
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