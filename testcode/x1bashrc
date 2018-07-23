#  PS1 setting script, features:

#  Regular use: (opt1/opt2 means opt1 has precedence)
##   user@host|cmd_time/clock|pwd$exit_code/''>

## print in color (if available)
## first print user@host (green):
##   host color is bold if SSH session.
## cmd_time (green|yellow|red) || clock (green):
##   clock time or cmd_time (if cmd_time > 20s).
##   cmd_time colors: green(20-59s||exemptions in 
##   x1_formTime), yellow(1-59m), red(>1hr). If 
##   cmd_time > 1min and on alert list in x1_formTime,
##   a GUI alert is sent, > 10min alert is peristent.
## path (blue):
##   print abbreviated path that dynamically abbreviates 
##   the dir names to be shorter the longer the total path.
##   To adjust look in x1_PWD(). The pwd is shortened to 
##   only the current directory inside tmux.
## exit status (red): 
##   print the last exit status at the end if != 0.

#  Git & Conda environments:
## If a conda env is active or in a git repo then the
##   username is not displayed and the clock is turned off.
##   cmd_time still appears if > 20s. The git repo is 
##   displayed after the host with the color in the 
##   following order of precedence: red for dirty, yellow 
##   for clean but untracked files present, cyan for clean
##   but ahead/behind of remote, green for clean.
##   The conda env is displaed where the user would be.
##   (conda_env)@host(git_branch)|cmd_time|/''pwd$exit/''>

# Non-PS1 features:
## Set window title to last cmd


shopt -s extglob    # for pattern matching
X1_PRECNT=0         # counter to see if cmd was blank 
X1_CMDCNT=0         # previous count
X1_PRETIM=$SECONDS  # time tracker


# User configurable settings, can set here to permanently
# change settings, or can do `SETTING=false` after script is
# sourced to turn off for just that shell (not for colors)
X1_COLORS=true      # set to false to turn off colors
X1_GITSTAT=true     # whether to show git branch, useful
                    # to turn off when `git status` is slow
X1_TIMING=true      # set to false to turn off cmd timing
X1_DELAY='20'       # minimum cmd time (in secs) to print
X1_ALERTS=true      # set false to turn off GUI time alerts
X1_SSHALERT=false   # whether to try to send alerts over SSH
X1_USER='unameHere' # username on client machine for remote
		    # alerts, must be keygen ssh connection
X1_SSHPORT='22'     # ssh port for client machine


if $X1_TIMING; then

    if $X1_ALERTS && $X1_SSHALERT && [ -n "$SSH_CLIENT" ]; then
	# this logic assumes only 1 level of ssh tunnel deep
	X1_CLIENTIP=$(echo $SSH_CLIENT |cut -f1 -d' ')

	ssh -o BatchMode=yes -o ConnectTimeout=2 $X1_USER@$X1_CLIENTIP \
	    -p $X1_SSHPORT 'notify-send &>/dev/null; exit $?' &>/dev/null

	X1_SSHALERT=$?

	if [ "$X1_SSHALERT" = '1' ]; then
	    X1_SSHALERT=true
	elif [ "$X1_SSHALERT" = '127' ]; then
	    echo "SSH client: $X1_USER@$X1_CLIENTIP,"
	    echo "  did not have notify-send installed"
	    X1_SSHALERT=false
	else
	    echo "Unable to establish keygen ssh connection"
	    echo "with $X1_USER@$X1_CLIENTIP, GUI alerts diabled"
	    X1_SSHALERT=false
    fi; fi

    notify-send &>/dev/null  # check if GUI alerts installed
    [ $? -ne 1 ] && ! $X1_SSHALERT && X1_ALERTS=false

    x1_preexec() {
	# command to run before every 'simple' command, tracks cmd stats

	[ "$BASH_COMMAND" = "$PROMPT_COMMAND" ] && return # ignore PS1 func
	[ -n "$COMP_LINE" ] && return                # ignore auto-complete

	X1_PRECMD=$BASH_COMMAND  # store command
	((X1_PRECNT++))          # increment counter, tracks empty prompt
	X1_PRETIM=$SECONDS       # store time of command
	echo -e "\e]0;"; echo -n $BASH_COMMAND; echo -ne "\007" #set win title
    }
    # Trap DEBUG to exec before 'simple' commands, only in newer bash
    # this is unsupported in bash3.x?, DEBUG trap execs after
    trap 'x1_preexec' DEBUG # $> help trap; # for more info
fi

tput colors &>/dev/null      # check for colors 
if [ $? -eq 0 ] && $X1_COLORS; then
    X1_COLG='\[\e[1;32m\]'   # green
    X1_COLG0='\[\e[0;32m\]'  # green unbold
    X1_COLY='\[\e[0;33m\]'   # yellow
    X1_COLC='\[\e[1;36m\]'   # cyan
    X1_COLB='\[\e[1;34m\]'   # blue
    X1_COLR='\[\e[1;31m\]'   # red
    X1_ECOL='\[\e[00m\]'     # end color
fi


x1_formTime(){ 
    # Convert sec to hr+min or min+sec for color display

    # Sends GUI alert if time > 1min and on the first
    # list in the 'case' section below. 
    # alert is persistant (must be cleared) if time > 10 min
    # alert is transient (cleared after fades) for < 10 min
    
    # Some common interactive commands will always be
    # green, such as editors, in the second list of the 
    # 'case' section below.

    # @parameters
    # arg1 (int): seconds to convert
    #
    # @returns
    # X1_CMDTIME (str): stores output in this global
    #   green for < 1 min and exemptions
    #   yellow for 1-59 min
    #   red for > 1 hour

    local min=$(( ($1/60) ))
    local sec=$(( $1 - ($min*60) ))
    local x1col="$X1_COLG0"             # green default
    local x1alertlvl=0                  # alert off default
    printf -v X1_CMDTIME "%dm%02ds" $min $sec

    if [ $1 -gt 59 ] && [ $1 -lt 600 ]; then     # 1-10 min
	x1col="$X1_COLY"
	x1alertlvl=1
    elif [ $1 -gt 599 ] && [ $1 -lt 3600 ]; then # 10-59 min
	x1col="$X1_COLY"
	x1alertlvl=2
    elif [ $1 -gt 3599 ]; then                   # > 1 hour
	x1alertlvl=2
	x1col="$X1_COLR"
	sec=$(( $1/3600 )) # repurpose sec to hours
	min=$(( ($1/60) - ($sec*60) ))
	printf -v X1_CMDTIME "%dh%02dm" $sec $min
    fi

    if $X1_ALERTS; then
    case "$X1_PRECMD" in # check alert lists

	# list for GUI alerts: (c)make, *.(sh|x|py),
	#  (i)python & shells (non-interactive),
        #  SECONDS= for testing
	?(c)make?( *)|?(ba|da|z)sh@( *)|?(i)python@( *)|\
	+([-a-zA-Z0-9_./()]).@(?(ba|z|c)sh|x|py)|\
	'SECONDS='*);;

	# list for no GUI alerts & green color always
	vi?(m)?( *)|nano?( *)|pico?( *)|gedit?( *)|emacs?( *)|\
	ssh?( *)|tmux?( *)|less?( *)|man?( *)|bc?( *)|htop?( *)|\
	gdb?(-ia)?( *)|vimdiff?( *)|tail?( *)|gnuplot?( *))
	    x1alertlvl=0
	    x1col="$X1_COLG0";;

	*) # defaults, no alert but keep color
	    x1alertlvl=0;;
    esac; fi

    # send alert if needed 
    if [ $x1alertlvl -gt 0 ]; then
	if $X1_ALERTS && ! $X1_SSHALERT; then
	    notify-send --hint=int:transient:$x1alertlvl --urgency=low \
			-i terminal "$X1_PRECMD took $X1_CMDTIME"
	elif $X1_ALERTS && $X1_SSHALERT; then
	    local notecmd="notify-send --hint=int:transient:$x1alertlvl"
	    notecmd="$notecmd --urgency=low -i network"
	    notecmd="$notecmd '$X1_PRECMD @$HOSTNAME took $X1_CMDTIME'"
	    ssh $X1_USER@$X1_CLIENTIP -p $X1_SSHPORT "$notecmd"
    fi; fi

    # store colored output in X1_CMDTIME
    printf -v X1_CMDTIME "$x1col$X1_CMDTIME$X1_ECOL"
}


x1_PWD() {
    # dynamically abbreviate the pwd
    #
    # @params
    # arg1 (str): path string, seperated by '/'
    #
    # @returns
    # X1_DISPPWD (str): global var

    [ "$1" = '/' ] && X1_DISPPWD='/' && return # root dir case
    local IFS="/"      # local field seperator for paths
    local PARTS=()     # pwd split into dirs
    X1_DISPPWD=''

    if [ -n "$HOME" ]; then # check if in HOME dir
	[ "$1" = "$HOME" ] && X1_DISPPWD='~' && return
	case "$1" in
	    "$HOME"?(/*))
		X1_DISPPWD='~'
		read -ra PARTS <<< "${1/"$HOME"/}";;
	    *)
	      	read -ra PARTS <<< "${1}";;
	esac
    else
	read -ra PARTS <<< "${1}"
    fi

    local plast=$((${#PARTS[@]} - 1))      # current dir index
    [ -z "${PARTS[0]}" ] && unset PARTS[0] # unset blank from read

    local cdir="${PARTS[$plast]}" 
    unset PARTS[$plast]

    local lenmax=3 # max dir name length of parent dirs
    local plen=$(($lenmax*$plast + ${#cdir}))
    if [ $plen -gt 24 ]; then #set how much to shorten dir names
	lenmax=$(($lenmax - 1))
	plen=$(($lenmax*$plast + ${#cdir}))
	if [ $plen -gt 30 ]; then
	    lenmax=$(($lenmax - 1))
            if [ "${#cdir}" -gt 14 ]; then
                cdir="${cdir::5}[~]${cdir:$((${#cdir}-5))}"
    fi; fi; fi

    #now set the directory to store in X1_DISPPWD
    for i in "${PARTS[@]}"; do
	if [ "${#i}" -gt $lenmax ]; then
	    X1_DISPPWD="$X1_DISPPWD/${i::$lenmax}"
	else
	    X1_DISPPWD="${X1_DISPPWD}/$i"
	fi
    done
    [ -n "$cdir" ] && X1_DISPPWD="$X1_DISPPWD/$cdir"
}


x1_get_PS1() {
    # Function that makes and sets PS1

    # Get last exit value + color
    local stat="$?"
    if [ $stat = 0 ]; then
        stat=""
    else
        stat="${X1_COLR}${stat}${X1_ECOL}"
    fi

    # Find if last cmd took > $X1_DELAY
    local x1time=''
    local gsep="$X1_COLG0|$X1_ECOL"             # green vert
    if $X1_TIMING; then
        if [ $(($SECONDS - $X1_PRETIM)) -gt $X1_DELAY ] && \
           [ "$X1_PRECNT" != "$X1_CMDCNT" ]; then

	    x1_formTime $(($SECONDS -$X1_PRETIM))
	    x1time="$X1_CMDTIME$gsep"
	fi
	X1_CMDCNT=$X1_PRECNT #update outside if[] for ctrl-c
    fi

    # Check git status (porcelain), show branch & top level untracked
    if $X1_GITSTAT; then
	local gitstat="$(git status -b -unormal --porcelain 2>/dev/null)"
    else
	local gitstat=''
    fi
    if [ -n "$gitstat" ]; then
	local lin1="${gitstat%%$'\n'*}"   
	local bnam="${lin1#'## '}"      # branchname
	bnam="${bnam%%'...'*}"          # finish extraction
	local bcol="$X1_COLG0"          # branch color
	if [ "${lin1%'[ahead '*}" != "$lin1" ] || \
	   [ "${lin1%'[behind '*}" != "$lin1" ]; then
	    bcol="$X1_COLC" # ahead/behind of remote, cyan
	fi
	lin1="${gitstat/"$lin1"/}" # remove lin1 from gitstat
	gitstat="$X1_COLG0($X1_ECOL"
	if [ "${lin1:1:2}" = '??' ]; then # Untracked
	    bcol="$X1_COLY"
	elif [ "${#lin1}" -gt 0 ]; then   # Dirty
	    bcol="$X1_COLR"
	fi
	gitstat="$gitstat$bcol$bnam$X1_ECOL$X1_COLG0)$X1_ECOL"
    fi

    # Check for a conda environment
    local condaenv=''
    [ -n "$CONDA_PREFIX" ] && condaenv="(${CONDA_PREFIX##*/})"

    # Only use current working dir if in tmux
    [ -z "$TMUX" ] && x1_PWD "$PWD" || X1_DISPPWD='\W'

    #check if we're in an ssh session
    local host=''
    [ -n "$SSH_CLIENT" ] && host="$X1_COLG" || host="$X1_COLG0"
    host="$host\h$X1_ECOL"

    # Form the pwd color, user, & clock if needed
    local dispdir="$X1_COLB$X1_DISPPWD$X1_ECOL" # blue pwd
    local user="$condaenv$X1_COLG0@$X1_ECOL"
    if [ -z "$gitstat" ] && [ -z "$condaenv" ]; then
	user="$X1_COLG0\u@$X1_ECOL"            # green user
	[ -z "$x1time" ] &&\
	    x1time="$X1_COLG0\A$X1_ECOL$gsep" # green clock
    fi

    PS1="$user$host$gitstat$gsep$x1time$dispdir\\\$$stat> "
    #echo "$user$host$gsep$time$gsep$dispdir\$$stat> "
}
PROMPT_COMMAND=x1_get_PS1


#Run any command line args as a command for tmux
"$@"
