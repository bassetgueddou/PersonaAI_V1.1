#!/bin/sh
set -e

# Si node_modules est vide (volume tout neuf), installe les deps
if [ ! -d node_modules ] || [ -z "$(ls -A node_modules 2>/dev/null)" ]; then
  echo "node_modules vide → npm install"
  npm install
fi

exec "$@"
