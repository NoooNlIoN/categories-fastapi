#!/bin/bash
set -e

alembic upgrade head
python src/utils/seed_db.py
python src/main.py


