#!/bin/sh
set -e
cd frontend
npm run build

cd ../backend
cp ../frontend/dist frontend -R
flask db upgrade
