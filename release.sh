#!/bin/sh
set -e

cd backend
cp ../frontend/dist frontend -R
flask db upgrade
