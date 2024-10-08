#!/bin/bash

# 指定数据集文件夹路径
experiment_dir="/root/benchmarks/benchmarks-500"

# 创建存储文件夹（如果不存在）
mkdir -p /root/output/output-500-48h/xsat

# 指定输出的结果文件路径
result_file="/root/output/output-500-48h/xsat/result-48h.csv"

# 指定命令的超时时间（秒）
timeout_seconds=$((48*60*60))

# 如果输出文件已存在，先删除以便重新创建
if [ -e "$result_file" ]; then
  rm "$result_file"
fi

echo "smt_file_path,smt_original_file_path,file_size,solving_results,solving_time,misc" >> "$result_file"

# 指定分类文件
select_files="$experiment_dir/select-48h-xsat.csv"

# 求解所有数据集文件
function run_solver(){
  # 遍历csv文件获取信息，对相应的smt2求解
  while read line
  do
    # 获取smt2文件信息
    IFS=',' read -r smt_file_path smt_original_file_path file_size <<< "$line"
  
    # 执行命令，限制执行时间，并捕获输出和执行时间
    cd /root/xsat
    start_time=$(date +%s.%N)
    solving_results=$(timeout "$timeout_seconds" make IN="$smt_file_path" 2>&1)
    return_code=$?
    end_time=$(date +%s.%N)

    # 计算命令执行时间
    solving_time=$(echo "$end_time - $start_time" | bc | awk '{printf "%.3f", $0}')
    
    # 检查IN的返回值，0 表示命令成功，124 表示超时，其他非零值表示出错
    if [ $return_code -eq 0 ]; then
      # 继续用xsat求解
      start_time=$(date +%s.%N)
      solving_results=$(timeout "$timeout_seconds" python xsat.py --bench 2>&1)
      return_code=$?
      end_time=$(date +%s.%N)

      # 计算命令执行时间
      solving_time=$(echo "$solving_time + $end_time - $start_time" | bc | awk '{printf "%.3f", $0}')
      
      # 检查xsat的返回值，0 表示命令成功，124 表示超时，其他非零值表示出错
      if [ $return_code -eq 0 ]; then
        # xsat成功执行
        echo "$smt_file_path,$smt_original_file_path,$file_size,$solving_results,$solving_time," >> "$result_file"
      elif [ $return_code -eq 124 ]; then
        # xsat执行超时
        echo "$smt_file_path,$smt_original_file_path,$file_size,,$solving_time,time out after $timeout_seconds seconds" >> "$result_file"
      else
        # xsat执行出错
        misc=$(echo "$solving_results" | tr ',' ';')
        misc=$(echo "$misc" | tr '\n' ';')
        echo "$smt_file_path,$smt_original_file_path,$file_size,,$solving_time,$misc" >> "$result_file"
      fi
      
    elif [ $return_code -eq 124 ]; then
      # IN超时
      echo "$smt_file_path,$smt_original_file_path,$file_size,,$solving_time,time out after $timeout_seconds seconds" >> "$result_file"
      
    else
      # IN出错
      tmp=$(echo "$solving_results" | grep -i -m 1 'error: ')
      misc=$(echo "$tmp" | tr ',' ';')
      misc=$(echo "$misc" | tr '\n' ';')
      echo "$smt_file_path,$smt_original_file_path,$file_size,,$solving_time,$misc" >> "$result_file"
    fi
    
  done < "$1"
}

# 调用函数
run_solver $select_files
