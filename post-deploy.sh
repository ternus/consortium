#!/bin/bash

source /home/gm/virtualenvs/consortium/bin/activate

export REPO_DIR="/home/gm/repos/consortium/"
export DJANGO_SETTINGS_MODULE="consortium.settings"
export PYTHONPATH="$REPO_DIR:$PYTHONPATH"

cd $REPO_DIR
python manage.py collectstatic --noinput

echo `date` >> /home/gm/www/last_updated.html
