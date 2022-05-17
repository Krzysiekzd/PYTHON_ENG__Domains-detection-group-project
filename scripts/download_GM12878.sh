#!/bin/bash

PARENT_DIR=$(git rev-parse --show-toplevel)
DATA_DIR="${PARENT_DIR}/data"
mkdir -p "${DATA_DIR}"

wget -r --no-clobber --no-check-certificate --no-parent -A .RAWobserved -l0 http://www.lcqb.upmc.fr/meetu/dataforstudent/HiC/GM12878/25kb_resolution_intrachromosomal/ -P "${DATA_DIR}"
wget -r --no-clobber --no-check-certificate --no-parent -A .RAWobserved -l0 http://www.lcqb.upmc.fr/meetu/dataforstudent/HiC/GM12878/100kb_resolution_interchromosomal/ -P "${DATA_DIR}"
wget -r --no-clobber --no-check-certificate --no-parent -A .RAWobserved -l0 http://www.lcqb.upmc.fr/meetu/dataforstudent/HiC/GM12878/100kb_resolution_intrachromosomal/ -P "${DATA_DIR}"

wget -r --no-clobber --no-check-certificate --no-parent -A .gz -l0 http://www.lcqb.upmc.fr/meetu/dataforstudent/TAD/ -P "${DATA_DIR}"

wget -r --no-clobber --no-check-certificate --no-parent -A .txt -l0 http://www.lcqb.upmc.fr/meetu/dataforstudent/comp/GM12878/25kb/ -P "${DATA_DIR}"
wget -r --no-clobber --no-check-certificate --no-parent -A .txt -l0 http://www.lcqb.upmc.fr/meetu/dataforstudent/comp/GM12878/100kb/ -P "${DATA_DIR}"

wget -r --no-clobber --no-check-certificate --no-parent -A .hdf5 -l0 http://www.lcqb.upmc.fr/meetu/dataforstudent/genedensity/25kb/ -P "${DATA_DIR}"
wget -r --no-clobber --no-check-certificate --no-parent -A .hdf5 -l0 http://www.lcqb.upmc.fr/meetu/dataforstudent/genedensity/100kb/ -P "${DATA_DIR}"

wget --no-clobber --no-check-certificate http://www.lcqb.upmc.fr/meetu/dataforstudent/E116_15_coreMarks_dense -P "${DATA_DIR}"
