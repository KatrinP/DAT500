#!/bin/sh

VENDOR_DIR=./vendor
GITHUB=github.com
HTTP=https
GIT="git"

mkdir -p "$VENDOR_DIR" 2>&1 > /dev/null
if [ $? -ne 0 ]
then
	# directory exists, we don't care
fi

PACKAGES=( ( "KatrinP", "Language-recognizer" ) )

for PACKAGE in ${PACKAGES[*]}
do
	echo "Installing ${PACKAGE[1]} from ${PACKAGE[0]}"
	"$GIT" clone "$HTTP"://"$GITHUB"/"${PACKAGE[0]}"/"${PACKAGE[1]}" "$VENDOR_DIR"/"${PACKAGE[0]}"/"${PACKAGE[1]}"
	if [ $? -ne 0 ]
	then
		echo "Error installing package. Continue."
	fi
	export PYTHON_PATH="$PYTHON_PATH":"$VENDOR_DIR"/"${PACKAGE[0]}"/"${PACKAGE[1]}"
	echo "Autoload generated"
done

if [ $? -ne 0 ]
then
	echo "Fatal error."
	exit 1
fi
