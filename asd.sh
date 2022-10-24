#!/bin/bash

# ./sys-exit.py error 1> read result
# ./sys-exit.py sucesso 1> read result
# result=$(./sys-exit.py error)
result=$(./sys-exit.py sucesso)
error_code="$?"
if [ "$error_code" -eq 0 ]
then
	echo "result: $result"
else
	echo "fim"
	exit $error_code
fi

# >&2 echo "asd: $result"
# if ./asd.py
# then
# 	echo "oi"
# fi
