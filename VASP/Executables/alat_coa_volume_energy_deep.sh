#!/bin/bash
tail -n 500 */OUTCAR | grep -A 1 "length of vectors" | grep 0 | awk '{printf $1"\n"}' > alat
tail -n 500 */OUTCAR | grep -A 1 "length of vectors" | grep 0 | awk '{printf $3/$1"\n"}' > coa
grep -m 1 "volume of cell" */OUTCAR | awk '{print $6}' > volume
tail -n 1 */OSZICAR | grep E0 | awk '{printf "%.9f\n", $5}' > energy
paste -d "," alat coa volume energy > results.csv
rm alat coa volume energy
