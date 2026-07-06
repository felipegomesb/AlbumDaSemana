#!/bin/sh
while true; do
    AGORA=$(date +%H:%M)
    if [ "$AGORA" = "00:00" ]; then
        python /app/manage.py rotacionar_musica
        sleep 60
    fi
    sleep 30
done
