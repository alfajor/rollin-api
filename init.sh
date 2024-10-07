#!/bin/bash

start_server() {
    pip install -r requirements.txt
    fastapi dev api/main.py 
}

setup_virtualenv() {
    local venv_dir=${1:-".venv"}

    if [[ -d "$venv_dir" ]]; then
        echo "Virtual environment found '$venv_dir'. Activating.."
        source "./$venv_dir/bin/activate"
        echo "$venv_dir activated" 
        which python3
        start_server
    else
        echo "Creaing a virtualenv.."
        python3 -m venv "$venv_dir"
        source "./$venv_dir/bin/activate"
        echo "$venv_dir created and activated" 
        start_server
    fi
}
setup_virtualenv
