# editor
export EDITOR=vim

# starship
eval "$(starship init zsh)"

# word jumping
bindkey "^[[1;5C" forward-word
bindkey "^[[1;5D" backward-word

# For some others (tmux alters sequences)
bindkey "^[Od" backward-word
bindkey "^[Oc" forward-word

# bat
alias cat="bat"

# ls
alias ls='ls --color=auto --group-directories-first'
alias l='ls -lh'
alias la='ls -lAh'
alias lt='ls -lht'
alias lS='ls -lhS'
alias l.='ls -lhd .*'

# History
export HISTFILE="$HOME/.zsh_history"
export HISTSIZE=10000
export SAVEHIST=10000
setopt INC_APPEND_HISTORY   # write to HISTFILE immediately, not on shell exit
setopt HIST_IGNORE_DUPS     # don't record consecutive duplicates
setopt HIST_IGNORE_SPACE    # don't record commands prefixed with a space
setopt HIST_REDUCE_BLANKS   # strip superfluous blanks

# zsh-autocomplete
source /usr/share/zsh/plugins/zsh-autocomplete/zsh-autocomplete.plugin.zsh

# zsh-autosuggestions
source /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.plugin.zsh

# zsh-autopair
source /usr/share/zsh/plugins/zsh-autopair/zsh-autopair.plugin.zsh

# Ctrl+F: accept autosuggestion
bindkey '^F' autosuggest-accept

# zsh-syntax-highlighting
source /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.plugin.zsh

# zsh-history-substring-search
source /usr/share/zsh/plugins/zsh-history-substring-search/zsh-history-substring-search.zsh

# fzf
source <(fzf --zsh)

# syswatch
source ~/.zsh_user_functions/syswatch.zsh

# ollama-cuda
source /etc/profile
