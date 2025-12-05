#!/bin/bash
set -e

# wait & run migrations then start app
python3 commerce-db/run_migrations.py

exec gunicorn -b 0.0.0.0:5000 TheSpicedMocha:app