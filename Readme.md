Python 3.9

Run chmod +x ./start_panel_process.sh to make the script executable
Run chmod +x ./kill_panel_process.sh to make the script executable

Use ./kill_panel_process.sh to kill the panel process. Make sure to always do this before running ./start_panel_process.sh manually.

Add the following to your .bashrc file to start the script on startup and allow them to be run from anywhere:
alias start_panel_process='~/path/to/start_panel_process.sh'
alias kill_panel_process='~/path/to/kill_panel_process.sh'
~/path/to/start_panel_process.sh
