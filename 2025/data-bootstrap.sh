#!/usr/bin/env bash

DIR_2025="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT="$( dirname ${DIR_2025} )"
DATA_2025="${ROOT}/data/2025"

cd $DATA_2025

kaggle competitions download \
  -c nfl-big-data-bowl-2025

unzip nfl-big-data-bowl-2025.zip

rm nfl-big-data-bowl-2025.zip
