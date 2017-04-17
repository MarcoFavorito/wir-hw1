#!/bin/bash

debug_msg="MAIN"

echo
echo $debug_msg - start...

if [ ! -d $script_folder ]; then
    echo $debug_msg - cannot find \"scripts\" folder...
    echo $debug_msg - exiting...
    echo
    exit 1
fi

source $script_folder/0-clean.sh
source $script_folder/1-set-my-classpath.sh
source $script_folder/2-create-collection.sh
source $script_folder/3-build-index.sh
source $script_folder/4-apply-scorer-functions.sh
source $script_folder/5-aggregation.sh
source $script_folder/6-evaluation.sh
source $script_folder/7-make-plots.sh

rm -R $script_folder/__pycache__
rm $script_folder/*.pyc

echo "MAIN" - done!
echo
