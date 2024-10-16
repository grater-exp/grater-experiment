#!/bin/bash

mkdir -p results/jfs
mkdir -p results/our

timeout_seconds=$((48*60*60))

function run_solver(){

  if [ -e "$2" ]; then
    rm "$2"
  fi

  echo "smt_file_path,smt_original_file_path,file_msg,solving_results,solving_time,misc" >> "$2"

  while read line
  do

    IFS=',' read -r smt_file_path smt_original_file_path file_msg <<< "$line"
  
    start_time=$(date +%s.%N)
    solving_results=$(timeout "$timeout_seconds" cvc5 "$smt_file_path" 2>&1)
    return_code=$?
    end_time=$(date +%s.%N)

    solving_time=$(echo "$end_time - $start_time" | bc | awk '{printf "%.3f", $0}')
    
    line_num=$(echo -e "$solving_results" | wc -l)
    if [ $line_num -gt 1 ]; then
      solving_results=$(echo "$solving_results" | tr '\n' '; ')
    fi

    if [ $return_code -eq 0 ]; then
      echo "$smt_file_path,$smt_original_file_path,$file_msg,$solving_results,$solving_time," >> "$2"
    elif [ $return_code -eq 124 ]; then
      echo "$smt_file_path,$smt_original_file_path,$file_msg,,$solving_time,time out after $timeout_seconds seconds" >> "$2"
    else
      echo "$smt_file_path,$smt_original_file_path,$file_msg,,$solving_time,$solving_results" >> "$2"
    fi
  done < "$1"
}

run_solver "jfs-benchmark.csv" "results/jfs/cvc5.csv"
run_solver "our-benchmark.csv" "results/our/cvc5.csv"
