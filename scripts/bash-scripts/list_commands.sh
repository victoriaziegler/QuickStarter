#! /bin/bash

list_coms(){
  echo
  echo -e "  ${undl}${lt_purp}Command${res_undl}        ${undl}Req Args${res_undl}          ${undl}Description${res_undl}"

  echo
  echo -e "  ${lt_ylw}lpro           ${lt_green}None              ${lt_cyan}- List all project quick-start commands"

  echo
  echo -e "  ${lt_ylw}ndsv           ${lt_red}dir name          ${lt_cyan}- Create a stand alone node/express server"
  echo "                                     in a new directory and start the server"
  echo "                                     in a new terminal window"

  echo
  echo -e "  ${lt_ylw}ndsv!          ${lt_green}None              ${lt_cyan}- Create a stand alone node/express server"
  echo "                                     in the current directory and start the"
  echo "                                     server in a new terminal window"

  echo
  echo -e "  ${lt_ylw}rnjsx          ${lt_red}dir name          ${lt_cyan}- Create a node express/react project in a "
  echo "                                     new directory. Opens and starts a new  "
  echo "                                     webpack build terminal and a server"
  echo "                                     terminal."

  echo
  echo -e "  ${lt_ylw}rnjsx!         ${lt_green}None              ${lt_cyan}- Create a node express/react project in"
  echo "                                     the current directory. Open and start"
  echo "                                     a new webpack build terminal and a"
  echo "                                     server terminal."

  echo
  echo -e "  ${lt_ylw}ndsvts         ${lt_red}dir name          ${lt_cyan}- Create a stand alone "
  echo "                                     node/express server in a new directory"
  echo "                                     and start the serverin a new terminal"
  echo "                                     window"

  echo
  echo -e "  ${lt_ylw}ndsvts!        ${lt_green}None              ${lt_cyan}- Create a stand alone"
  echo "                                     node/express server in the current "
  echo "                                     directory and start the server in a new "
  echo "                                     terminal window"

  echo
  echo -e "  ${lt_ylw}rntsx          ${lt_red}dir name          ${lt_cyan}- Create a typescript node express/react "
  echo "                                     project in a new directory. Opens and "
  echo "                                     starts a new webpack build terminal and a "
  echo "                                     server terminal."

  echo
  echo -e "  ${lt_ylw}rntsx!         ${lt_green}None              ${lt_cyan}- Create a typscript node express/react"
  echo "                                     project in the current directory. Opens "
  echo "                                     and starts a new webpack build terminal "
  echo "                                     and a server terminal."

  echo
  echo -e "  ${lt_ylw}djpr           ${lt_red}dir name          ${lt_cyan}- Create a complete django microservices"
  echo "                                     project structure."

  echo
  echo -e "  ${lt_ylw}phaser         ${lt_red}dir name          ${lt_cyan}- Create a game with phaser.js"
  echo
  echo -e "  ${lt_ylw}phaser!        ${lt_green}None              ${lt_cyan}- Create a game with phaser.js in the"
  echo "                                     current directory."
}

alias 'coms'="list_coms"