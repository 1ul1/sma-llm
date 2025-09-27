#!/bin/bash
path="$(dirname $(realpath $0))"
cd "$path"
# ACTIVATE CONDA ENV
# source /Users/$USER/GenericPathTo/conda.sh
conda activate ../../env
cd ..
python3 sma_llm/utils/gui/wait_screen.py &
pid=$!
python3 -m sma_llm.main.my_main $pid