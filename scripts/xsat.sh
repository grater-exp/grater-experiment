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
  
    cd /root/xsat # folder path of xsat
    start_time=$(date +%s.%N)
    solving_results=$(timeout "$timeout_seconds" make IN="$smt_file_path" 2>&1)
    return_code=$?
    end_time=$(date +%s.%N)

    solving_time=$(echo "$end_time - $start_time" | bc | awk '{printf "%.3f", $0}')
    
    if [ $return_code -eq 0 ]; then
      start_time=$(date +%s.%N)
      solving_results=$(timeout "$timeout_seconds" python xsat.py --bench 2>&1)
      return_code=$?
      end_time=$(date +%s.%N)

      solving_time=$(echo "$solving_time + $end_time - $start_time" | bc | awk '{printf "%.3f", $0}')
      
      if [ $return_code -eq 0 ]; then
        echo "$smt_file_path,$smt_original_file_path,$file_msg,$solving_results,$solving_time," >> "$2"
      elif [ $return_code -eq 124 ]; then
        echo "$smt_file_path,$smt_original_file_path,$file_msg,,$solving_time,time out after $timeout_seconds seconds" >> "$2"
      else
        misc=$(echo "$solving_results" | tr ',' ';')
        misc=$(echo "$misc" | tr '\n' ';')
        echo "$smt_file_path,$smt_original_file_path,$file_msg,,$solving_time,$misc" >> "$2"
      fi
      
    elif [ $return_code -eq 124 ]; then
      echo "$smt_file_path,$smt_original_file_path,$file_msg,,$solving_time,time out after $timeout_seconds seconds" >> "$2"
      
    else
      tmp=$(echo "$solving_results" | grep -i -m 1 'error: ')
      misc=$(echo "$tmp" | tr ',' ';')
      misc=$(echo "$misc" | tr '\n' ';')
      echo "$smt_file_path,$smt_original_file_path,$file_msg,,$solving_time,$misc" >> "$2"
    fi
    
  done < "$1"
}

run_solver "jfs-benchmark.csv" "results/jfs/xsat.csv"
run_solver "our-benchmark.csv" "results/our/xsat.csv"
