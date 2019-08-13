SOURCE="${BASH_SOURCE[0]}" # Path of this sourced file
GOTOFOLDER_SCRIPT_PATH=`dirname $SOURCE`

_goto_comp() {
	local cur
	COMPREPLY=()
	cur="${COMP_WORDS[COMP_CWORD]}"

	COMPREPLY=($(compgen -W "$("$GOTOFOLDER_SCRIPT_PATH"/goto-completion.py "$@")" -- ${cur}))
	return 0
}

complete -F _goto_comp goto
