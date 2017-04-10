#!/bin/bash

debug_msg="CLEAN"

echo
echo $debug_msg - start...

if [ ! -d out ]; then
    echo $debug_msg - already clean!
    echo
else
    rm -r out
fi

echo $debug_msg - done!
echo