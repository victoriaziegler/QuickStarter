
lt_red="\033[01;91m"     # Light Red
lt_green="\033[01;92m"   # Light Green
lt_ylw="\033[01;93m"     # Light Yellow
lt_purp="\033[01;95m"    # Light Purple
lt_cyan="\033[01;96m"    # Light Cyan

undl="\033[04m"      # Underlined
res_undl="\033[24m"      # Underlined reset

clr="\033[00m"      # Reset

alias 'python'="python3"
alias 'bashrc'="code -r ~/.bashrc"

source ~quickstarter/scripts/bash-scripts/ignition.sh
source ~quickstarter/scripts/bash-scripts/die-docker-die.sh
source ~quickstarter/scripts/bash-scripts/list_commands.sh

echo -e "${lt_ylw} For a list of project quick start commands, use command: coms"