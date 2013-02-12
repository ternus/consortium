rm dev.db
./manage.py syncdb --noinput --migrate
./manage.py createsuperuser --username=cternus --email=ternus@cternus.net
./manage.py loaddata hexgrid.json
./manage.py loaddata territory/initial_data.json
