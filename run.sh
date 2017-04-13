#!/bin/bash

debug_msg="MAIN"

echo
echo $debug_msg - start...

if [ ! -d scripts ]; then
    echo $debug_msg - cannot find \"scripts\" folder...
    echo $debug_msg - exiting...
    echo
    exit 1
fi

source scripts/0-clean.sh
source scripts/1-set-my-classpath.sh
source scripts/2-create-collection.sh
source scripts/3-build-index.sh
source scripts/4-apply-scorer-functions.sh
source scripts/5-aggregation.sh
source scripts/6-evaluation.sh
source scripts/7-make-plots.sh


echo $debug_msg - done!
echo
