#!/usr/bin/env bash

# USE EXAMPLE: create_targz_from_filelist.sh arquivos_do_projeto lista-de-arquivos.txt
# RESULT: `arquivos_do_projeto.tar.gz` containing files listed in `lista-de-arquivos.txt`

filename=$1
listfile=$2

tar -cvf ${filename}.tar -T ${listfile}
gzip ${filename}.tar
