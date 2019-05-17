#!/bin/bash

set -e

rm -f /home/certjobs/eventdownload/*
/usr/local/bin/cronjob_eventdownload.py

BACKEND_SERVER=<SERVER>

ssh -i .ssh/id_ed25519 $BACKEND_SERVER "rm -f /home/cp-server/do-portal/backend/app/static/data/*"
scp -i .ssh/id_ed25519 /home/certjobs/eventdownload/* $BACKEND_SERVER:/home/cp-server/do-portal/backend/app/static/data/

