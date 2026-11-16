#!/bin/bash
# Usage: ./run.sh            (console)
#        ./run.sh web        (server-backed browser front-end)
usage() {
    echo "Usage: ./run.sh            play Night Ferry in this terminal"
    echo "       ./run.sh web        serve it to a browser at http://127.0.0.1:8000"
    echo "                           (NIGHTFERRY_WEB_HOST / NIGHTFERRY_WEB_PORT move it)"
}
cd "$(dirname "$0")"
if [ "$#" -gt 1 ]; then
    usage >&2
    exit 2
fi
case "$1" in
    "")
        PYTHONPATH=src python3 -m nightferry
        ;;
    web)
        PYTHONPATH=src python3 -c "from tak.ui import UIType; from nightferry.game import NightFerry; NightFerry(UIType.WEB).play()"
        ;;
    -h|--help)
        usage
        ;;
    *)
        usage >&2
        exit 2
        ;;
esac
