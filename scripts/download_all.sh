#!/bin/bash

PARENT_DIR=$(git rev-parse --show-toplevel)
DATA_DIR="${PARENT_DIR}/data"
mkdir -p "${DATA_DIR}"

wget -r --no-clobber --no-check-certificate --no-parent -A .RAWobserved https://www.lcqb.upmc.fr/meetu/dataforstudent -P "${DATA_DIR}"
wget -r --no-clobber --no-check-certificate --no-parent -A .gz https://www.lcqb.upmc.fr/meetu/dataforstudent -P "${DATA_DIR}"
wget -r --no-clobber --no-check-certificate --no-parent -A .txt https://www.lcqb.upmc.fr/meetu/dataforstudent -P "${DATA_DIR}"

wget --no-clobber --no-check-certificate http://www.lcqb.upmc.fr/meetu/dataforstudent/E116_15_coreMarks_dense -P "${DATA_DIR}"
