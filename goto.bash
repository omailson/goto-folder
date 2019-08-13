SOURCE="${BASH_SOURCE[0]}" # Path of this sourced file
GOTOFOLDER_SCRIPT_PATH=`dirname $SOURCE`

goto() {
	local result

	result=$("$GOTOFOLDER_SCRIPT_PATH"/goto.py "$@")
	error_code="$?"
	if [ "$error_code" -eq 0 ]
	then
		if [ "$#" -eq 0 ]
		then
			echo "$result"
		else
			echo "$result"
			cd "$result"
		fi
	fi

	return "$error_code"
}

export -f goto
