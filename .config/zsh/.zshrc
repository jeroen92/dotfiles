# General zsh config
export ZSH="/home/jschutrup/.oh-my-zsh"

ZSH_THEME="ys"

DISABLE_AUTO_UPDATE="true"

# Standard plugins can be found in ~/.oh-my-zsh/plugins/*
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
plugins=(archlinux kubectl docker git)

source $ZSH/oh-my-zsh.sh

export LANG=en_US.UTF-8

# Sourcery
source /usr/bin/virtualenvwrapper_lazy.sh

# Personal aliases
alias dotfiles="/usr/bin/git --git-dir=$HOME/.dotfiles --work-tree=$HOME"

# Environment vars
GPG_TTY=$(tty)
export GPG_TTY

export WORKON_HOME=~/.virtualenvs

export SSH_AUTH_SOCK=$(gpgconf --list-dirs agent-ssh-socket)

# Without this line, hitting enter in a read prompt sometimes results in a literal ^M
# See: https://bbs.archlinux.org/viewtopic.php?id=150097
stty icrnl
