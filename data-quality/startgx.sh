#!/bin/sh

cd Documents/dqm
source env/bin/activate
cd kpidata/great_expectations/uncommitted/
jupyter notebook &
cd data_docs/local_site/
python3 -m http.server 8000 &
