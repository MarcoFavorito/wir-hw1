if [ "$#" -ne 1 ]; then
	echo "Usage: ./clean.sh <basename-of-the-index>"
	exit -1
fi
rm $1.collection $1-*
