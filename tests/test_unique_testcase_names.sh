#!/bin/bash

grep "^class" tests/*.py | awk '{
    arr[$NF]++
  }
  END {
    for (word in arr) {
      if (arr[word] != "1") {
        printf "DUPLICATES: %s %d\n", word, arr[word]
      }
    }
  }' | grep -q "DUPLICATES"

if (( ! $? )); then
    echo "Error: Duplicate TestCase class names found"
    exit 1
fi
