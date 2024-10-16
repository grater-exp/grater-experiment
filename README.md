# Grater-experiment

Grater is a floating-point constraints solver based on a new MO-based method. This repository contains the source code of Grater, along with all evaluation data, including detailed comparisons of Grater against each baseline solver.



## Running Grater

#### Dependencies

Grater has the following dependencies:

- python 3.9
- python packages: numpy, scipy, autograd, pandas, bitstring, func-timeout
- Z3 (for parsing SMT2 files)

Once python 3.9 (or higher version) is installed, other dependencies can be installed easily by using `pip`: 

```
pip install numpy scipy autograd pandas bitstring func-timeout z3-solver
```

#### Running from the source code

The `slovers/grater` directory contains the source code of Grater. We recommend running Grater on Linux to prevent bugs on other systems.

Consider the benchmark constraints located at `benchmarks/our-benchmarks` (i.e., the "our benchmarks" used in Grater's paper) as an example. You can use commands like

```
python solvers/grater/parse.py --path ../../benchmarks/our-benchmarks
python solvers/grater/solve-with-check.py
```

after cloning this repository. 

The first command is to generate objective functions of the constraints which need to be solved. The option `--path` (or `-p`) in the command is to specify the folder path where the constraints are stored (absolute path or relative path to `parse.py`). The files of objective functions and parsing results will be in `solvers/grater/objective_functions.py` and `solvers/grater/output/construct.csv`. The parsing results contain the file path, variable number and parsing time of constraints.

The second command is to run grater to solve these constraints. The solving results will be in `solvers/grater/output/solving_results.csv`. The solving results add the solving time, total time (parsing time + solving time), solving result (sat or unknown) based on parsing results.

Additionally, you can specify the output directory of benchmark to run using `--benchmark` option (or `-b`). For example, `--benchmark our`, the parsing results and solving results will be in `solvers/grater/our`. Note that the output directory of `parse.py` and `solve-with-check.py` need to be same.



## Baselines

We compare Grater with following solvers:

|                      Solver                      |                     Version / SHA Commit                     |
| :----------------------------------------------: | :----------------------------------------------------------: |
|    [XSat](https://github.com/zhoulaifu/xsat)     | [r50f1766](https://github.com/zhoulaifu/xsat/commit/50f1766890b0a5c92aacd86491f5fc94a0ba574d) |
| [CoverMe](https://github.com/zhoulaifu/coverme/) | [r8f834be](https://github.com/zhoulaifu/coverme/commit/8f834be367fd19dbe75c17f3d3efc773f2eabc73) |
|    [JFS](https://github.com/mc-imperial/jfs)     | [rc45b12c](https://github.com/mc-imperial/jfs/commit/c45b12c5383e0242099b645cac4376fb0216a60d) |
|       [Z3](https://github.com/Z3Prover/z3)       | [v4.13.0](https://github.com/Z3Prover/z3/releases/tag/z3-4.13.0) |
|       [CVC5](https://github.com/cvc5/cvc5)       | [v1.2.0](https://github.com/cvc5/cvc5/releases/tag/cvc5-1.2.0) |
| [Bitwuzla](https://github.com/bitwuzla/bitwuzla) | [v0.5.0](https://github.com/bitwuzla/bitwuzla/releases/tag/0.5.0) |

NOTE: CoverMe is not originally designed for floating-point constraints solving, so we adapt it to function as a floating-point constraint solver. The source code of adapted CoverMe is in `slovers/coverme`. The way to run it is the same as [XSat](https://github.com/zhoulaifu/xsat).



## Benchmarks

The directory `benchmarks` contains the benchmarks used in Grater's paper. `benchmarks/jfs-benchmarks` is [JFS's benchmark](https://github.com/mc-imperial/jfs-fse-2019-artifact/tree/master/data/benchmarks/3-stratified-random-sampling/benchmarks/QF_FP), and `benchmarks/our-benchmarks` is "our benchmarks" mentioned in Grater's paper. 

The files of objective functions and parsing results of these two benchmarks have already generated in `solvers/grater/objective_functions_jfs.py` and `solvers/grater/jfs/construct.csv`,  `solvers/grater/objective_functions_our.py` and `solvers/grater/our/construct.csv`.