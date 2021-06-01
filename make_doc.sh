#! /bin/bash -e

mkdir docs

sphinx-apidoc -f -o ./docs .

sphinx-build -b singlehtml ./docs ./docs/_build