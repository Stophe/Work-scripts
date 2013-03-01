#!/bin/bash
grep ALAT OUTCAR.* | awk '{printf "%.9f\n", $4}' > alat
tail -n 1 OSZICAR.* | grep E0 | awk '{printf "%.9f\n", $5}' > energy
paste -d "," alat energy > results.csv
rm alat energy
