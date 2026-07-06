#!/bin/sh
while true; do
    AGORA=$(date +%H:%M)
    if [ "$AGORA" = "00:00" ]; then
        python /app/manage.py rotacionar_musica

        DIA_SEMANA=$(date +%u)
        if [ "$DIA_SEMANA" = "7" ]; then
            python /app/manage.py rotacionar_album
        fi

        sleep 60
    fi
    sleep 30
done
