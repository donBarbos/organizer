#!/bin/bash

cd /usr/src/app

echo "Installing dependencies from Pipfile.lock"
pipenv sync
echo "Done"

echo "Running project"
python3 -m /usr/src/app/organizer
echo "Done"

exec "$@"
