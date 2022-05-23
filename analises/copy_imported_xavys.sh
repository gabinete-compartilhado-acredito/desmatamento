#!/usr/bin/env bash

# Copy `xavy` python modules imported in the file provided as input to the target
# directory provided as input.
# USE EXAMPLE: copy_imported_xavys.sh analise_orcamento_e_desmatamento.ipynb ./xavy/

pythonfile=$1
targetdir=$2

importlist=`grep "import xavy\..* as" $pythonfile -o | cut -d" " -f2 | cut -d. -f2`

for f in $importlist
do
    echo "cp ~/prog/my-python/xavy/${f}.py $targetdir"
    cp ~/prog/my-python/xavy/${f}.py $targetdir
done
