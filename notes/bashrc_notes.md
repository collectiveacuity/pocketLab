## Alias Home Command
alias home='function _home(){ file_path="$(lab home --print_path $1)"; cd "$file_path"; };_home'