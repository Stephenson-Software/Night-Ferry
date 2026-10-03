#!/bin/bash
# Usage: ./run.sh            (console)
#        ./run.sh web        (server-backed browser front-end)
cd "$(dirname "$0")"
if [ "$1" = "web" ]; then
    PYTHONPATH=src python3 -c "from tak.ui import UIType; from nightferry.game import NightFerry; NightFerry(UIType.WEB).play()"
else
    PYTHONPATH=src python3 -m nightferry
fi
