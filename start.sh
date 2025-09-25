#!/bin/bash
set -e

alembic upgrade head

python src/main.py
