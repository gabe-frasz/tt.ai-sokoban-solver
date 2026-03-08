#!/usr/bin/env bash

SESSION="ai-sokoban-solver"
VENV="$(pwd)/venv/bin/activate"

if [ ! -f "$VENV" ]; then
    echo -e "No venv found.\nMake sure you are in the project root directory and venv is exists."
    exit 1
fi

tmux has-session -t $SESSION 2> /dev/null

if [ $? != 0 ]; then
  tmux new-session -d -s $SESSION -n "nvim"
  tmux send-keys -t $SESSION:nvim "source $VENV && nvim ." C-m

  tmux new-window -t $SESSION -n "shell"
  tmux send-keys -t $SESSION:shell "source $VENV && clear" C-m

  tmux select-window -t $SESSION:nvim
fi

tmux attach -t $SESSION

