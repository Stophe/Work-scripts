#!/bin/bash
tail -n 100 OUTCAR.* | grep -A 1 "length of vectors" | grep 0 | awk '{printf $1"\n"}' > alat
tail -n 100 OUTCAR.* | grep -A 1 "length of vectors" | grep 0 | awk '{printf $3/$1"\n"}' > coa
tail -n 1 OSZICAR.* | grep E0 | awk '{printf "%.9f\n", $5}' > energy
paste -d "," alat coa energy > results.csv
rm alat coa energy
