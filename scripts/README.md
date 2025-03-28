# Scripts

This directory contains the scripts we used to run experiments. The two csv files `jfs-benchmark.csv` and `our-benchmark.csv` provide the file paths and other information (such as variable number or file size) of benchmarks to guide the baseline solvers solving benchmarks in order. 



The scripts can be run directly if you want to reproduce the [results](https://github.com/grater-exp/grater-experiment/tree/master/results) of baselines in our experiments, like: 

```
./bitwuzla.sh
```

after Bitwuzla has been installed successfully. Other solvers are the same.

Note that the [line 22](https://github.com/grater-exp/grater-experiment/blob/master/scripts/jfs.sh#L22) of `jfs.sh`, [line 21](https://github.com/grater-exp/grater-experiment/blob/master/scripts/xsat.sh#L21) of `xsat.sh`, and [line 21](https://github.com/grater-exp/grater-experiment/blob/master/scripts/coverme.sh#L21) of `coverme.sh` need specify the build path of JFS, XSat and CoverMe. And we have adapted XSat and CoverMe for fair comparison without effecting performance. The code of adapted XSat and CoverMe are in [slovers/xsat](https://github.com/grater-exp/grater-experiment/tree/master/solvers/xsat) and [slovers/coverme](https://github.com/grater-exp/grater-experiment/tree/master/solvers/coverme).