#! /bin/bash

  if [ -n "$ZSH_VERSION" ]; then
      if [ -f ~/.zshrc ]; then
        cat ~/quickstarter/install/rc_update.sh >> ~/.zshrc
      elif [ -f ~/.zshenv]; then
        cat ~/quickstarter/install/profile_update.sh >> ~/.zshenv
        touch ~/.zshrc
        cat ~/quickstarter/install/rc_update.sh >> ~/.zshrc
      else
        touch ~/.zshrc
        cat ~/quickstarter/install/rc_update.sh >> ~/.zshrc
      fi
  elif [ -n "$BASH_VERSION" ]; then
      if [ -f ~/.bashrc ]; then
        cat ~/quickstarter/install/rc_update.sh >> ~/.bashrc
      elif [ -f ~/.bash_profile ]; then
        cat ~/quickstarter/install/profile_update.sh >> ~/.bash_profile
        touch ~/.bashrc
       cat ~/quickstarter/install/rc_update.sh >> ~/.bashrc
      else
        touch ~/.bashrc
        cat ~/quickstarter/install/rc_update.sh >> ~/.bashrc
      fi
  else
    echo "Not bash or zsh"
  fi

