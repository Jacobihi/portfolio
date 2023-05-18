setopt interactive_comments
# assume you source from `portfolio`
alias cli="python cli/run_cli.py"
# app aliases for common file types needed
alias pycharm="open -a PyCharm.app"
alias datagrip="open -a DataGrip.app"
alias sublime="open -a 'Sublime Text.app'"
alias excel="open -a 'Microsoft Excel.app'"
alias firefox="open -a Firefox.app"
alias drawio="open -a draw.io.app"

# misc
alias show_conflicts="git diff --name-only --diff-filter=U"
alias prune_remote_git="git remote prune origin"
alias prune_local_git="git branch -vv | grep ': gone]'|  grep -v '\*' | awk '{ print \$1; }' | xargs git branch -D"
