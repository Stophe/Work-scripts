#!/bin/bash
grep ALAT */OUTCAR | awk '{print $4/4}' > alat
tail -n 1 */OSZICAR | grep E0 | awk '{printf "%f\n",$5}' > energy
paste alat energy -d "," > results.csv
rm alat energy
