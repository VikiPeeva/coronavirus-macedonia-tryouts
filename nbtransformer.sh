#!/bin/bash

BASEDIR=$(dirname "$0")
cd $BASEDIR
cwd=$(pwd)

notebook=$1
nbname=${notebook%".ipynb"}
nbinteract $notebook
cd nbinteract_html_transformer
htmlname="../$nbname.html"

python ./transformer.py -i $htmlname -o $htmlname