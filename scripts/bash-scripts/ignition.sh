#! /bin/bash

missing_directory_message(){
    echo
    echo -e "${lt_red}  ERROR!!!${clr}"
    echo
    echo -e "${lt_ylw}  Command requires you to pass a directory name"
    echo -e "  Use the following format:"
    echo
    echo -e "  ${lt_cyan}  $1 <<directory name>>${clr}  "
    echo
    echo -e "${lt_ylw}  To start project in the curent directory, use:"
    echo
    echo -e "  ${lt_cyan}  $1!${clr}  "
    echo
}
alias 'qs_missing_directory_message'="missing_directory_message"


react-build(){
  here=$(pwd)
  osascript -e "tell app \"Terminal\" to do script \"cd ${here} && npm run build-dev\""
}


start-node-server(){
  here=$(pwd)
  osascript -e "tell app \"Terminal\" to do script \"cd ${here} && npm start\""
}


init-react() {
  npm init -y
  npm install --save-dev webpack webpack-cli @babel/preset-react babel-loader @babel/core @babel/preset-env prettier jest babel-jest
  npm install react react-dom axios

  mkdir client
  mkdir client/src
  mkdir client/dist
  mkdir client/src/components
  touch client/dist/styles.css

  npe scripts.build-dev "webpack --mode development -w"
  npe scripts.build-prod "webpack --mode production"

  cp ~/quickstarter/dev-templates/wbpk-jsx.js webpack.config.js
  cp ~/quickstarter/dev-templates/babelrc .babelrc
  cp ~/quickstarter/dev-templates/indexjs.js client/src/index.js
  cp ~/quickstarter/dev-templates/appjs.js client/src/components/App.jsx
  cp ~/quickstarter/dev-templates/dist-html.html client/dist/index.html
  cp ~/quickstarter/dev-templates/testing.js app.test.js
}


add-server() {
  npm install express morgan nodemon
  mkdir server
  cp ~/quickstarter/dev-templates/server-index.js server/index.js
  npe scripts.start "nodemon server/index.js"
}


react-node(){
  init-react
  add-server
}


just-server-here(){
  npm init -y
  add-server
  code .
  start-node-server
}


just-server(){
  if [ -z $1 ]; then
    qs_missing_directory_message ndsv
  else
  mkdir $1
  cd $1
  just-server-here
  fi
}


react-node-here(){
  react-node
  code .
  react-build
  start-node-server
}


react-node-new-dir(){
  if [ -z $1 ]; then
    qs_missing_directory_message rnjsx
  else
  mkdir $1
  cd $1
  react-node-here
  fi
}


add-ts-server() {
  npm install express morgan nodemon
  mkdir server
  cp ~quickstarter/dev-templates/typescript-config.json tsconfig.json
  cp ~quickstarter/dev-templates/server-index.js server/index.tsx
  npe scripts.start "nodemon server/index.js"
}


just-ts-server-here(){
  npm init -y
  add-ts-server
  code .
  start-node-server
}


just-ts-server(){
  if [ -z $1 ]; then
    qs_missing_directory_message ndsvts
  else
  mkdir $1
  cd $1
  just-ts-server-here
  fi
}


react_node_typescript_here(){
  npm init -y
  npm install --save-dev webpack webpack-cli @types/react @types/react-dom @babel/preset-react babel-loader @babel/core @babel/preset-env prettier typescript ts-loader jest babel-jest
  npm install react react-dom express morgan nodemon axios

  npe scripts.build-dev "webpack --mode development -w"
  npe scripts.build-prod "webpack --mode production"
  npe scripts.start "nodemon server/index.tsx"

  mkdir server
  mkdir client
  mkdir client/dist
  mkdir client/src
  mkdir client/src/components
  touch client/dist/styles.css

  cp ~/quickstarter/dev-templates/wbpk-tsx.js webpack.config.js
  cp ~/quickstarter/dev-templates/babelrc .babelrc
  cp ~/quickstarter/dev-templates/index-tsx.tsx client/src/index.tsx
  cp ~/quickstarter/dev-templates/apptsx.tsx client/src/components/App.tsx
  cp ~/quickstarter/dev-templates/dist-html.html client/dist/index.html
  cp ~/quickstarter/dev-templates/server-index.js server/index.tsx
  cp ~/quickstarter/dev-templates/testing.js app.test.js
  cp ~/quickstarter/dev-templates/typescript-config.json tsconfig.json
  code .
  react-build
  start-node-server
}


react_node_typescript(){
  if [ -z $1 ]; then
    qs_missing_directory_message ndsv
  else
  mkdir $1
  cd $1
  react_node_typescript_here
  fi
}


init-phaser-here() {
  npm init -y
  npm install express phaser nodemon

  mkdir server
  mkdir public

  cp ~/quickstarter/dev-templates/phaser-server.js ./server/index.js
  cp ~/quickstarter/dev-templates/phaserhtml.html ./public/index.html

  npe scripts.start "nodemon server/index.js"
  here=$(pwd)
  code .
  osascript -e "tell app \"Terminal\" to do script \"cd ${here} && npm start\""
  osascript -e "tell app \"Terminal\" to do script \"cd ~/quickstarter/phaser_examples && code . && npm start\""
  open "http://localhost:3000"
  open "http://localhost:3100"
}


init-phaser(){
  if [ -z $1 ]; then
    qs_missing_directory_message phaser
  else
  mkdir $1
  cd $1
  init-phaser-here
  fi
}


create_python_project_here() {
  python3 -m venv .venv
  source ./.venv/bin/activate
  python3 -m pip install --upgrade pip
  pip freeze > requirements.txt
  code .
}


create_python_project() {
  if [ -z $1 ]; then
    qs_missing_directory_message pypr
  else
  directory=$1
  mkdir $directory
  cd $directory
  create_python_project_here
  fi
}



create_django_microservices() {
  if [ -z $1 ]; then
    echo
    echo
    echo -e "${lt_red}  ERROR!!!${clr}"
    echo
    echo -e "${lt_ylw}  Command requires you to pass a directory name"
    echo -e "  Use the following format:"
    echo
    echo -e "  ${lt_cyan}  djpr <<directory name>>${clr}  "
    echo
    echo
  else
  directory=$1
  mkdir $directory
  location=$(pwd)
  if [ -n "~/quickstarter/configs/$2" ]; then
    if [[ $2 == *.json ]]; then
      cp ~/quickstarter/configs/$2 "$directory/config.json"
    elif [[ $2 == *.yaml ]]; then
      cp ~/quickstarter/configs/$2 "$directory/config.yaml"
    fi
  fi
  cd $directory
  here=$(pwd)
  echo
  echo -e "${lt_ylw}  Starting a Django microservice project at $here... "
  echo -e "${lt_cyan}${blink}  preparing project... ${clr}"
  echo
  python3 -m venv .venv
  source ./.venv/bin/activate
  python3 -m pip install --upgrade pip
  mkdir db
  cp ~/quickstarter/dev-templates/create-multiple-databases.sh db/create-multiple-databases.sh
  cp ~/quickstarter/dev-templates/dj_api_require.txt requirements.txt
  cp ~/quickstarter/dev-templates/python-gitignore.txt .gitignore
  cp ~/quickstarter/dev-templates/git-attributes.txt .gitattributes
  chmod +x db/create-multiple-databases.sh
  pip install -r requirements.txt
  python ~/quickstarter/scripts/py-scripts/microservices.py
  deactivate
  code .
  osascript -e "tell app \"Terminal\" to do script \"cd ${here} && docker compose build && docker compose up\""
  fi
}


alias 'ndsv'="just-server"
alias 'ndsv!'="just-server-here"
alias 'ndsvts'="just-ts-server"
alias 'ndsvts!'="just-ts-server-here"
alias 'rnjsx'="react-node-new-dir"
alias 'rnjsx!'="react-node-here"
alias 'rntsx'="react_node_typescript"
alias 'rntsx!'="react_node_typescript_here"
alias 'phaser'="init-phaser"
alias 'phaser!'="init-phaser-here"
alias 'pypr'="create_python_project"
alias 'pypr!'="create_python_project_here"
alias 'djpr'="create_django_microservices"

