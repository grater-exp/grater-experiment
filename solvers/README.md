# Solvers

This directory contains the source code of Grater and adapted CoverMe.

## Grater

The source code of Grater is in [grater](https://github.com/grater-exp/grater-experiment/tree/master/solvers/grater). The way to run it has been introduced [here](https://github.com/grater-exp/grater-experiment?tab=readme-ov-file#running-grater). If you want to reproduce the [results](https://github.com/grater-exp/grater-experiment/tree/master/results) of Grater in our experiments, you can use command: 

```
python solvers/grater/parse.py -p ../../benchmarks/jfs-benchmarks -b jfs
python solvers/grater/solve-with-check.py -b jfs
```

and

```
python solvers/grater/parse.py -p ../../benchmarks/our-benchmarks -b our
python solvers/grater/solve-with-check.py -b our
```

to obtain the results of Grater on JFS's benchmarks and our benchmarks.

The files of objective functions and parsing results of these two benchmarks have already generated in `solvers/grater/objective_functions_jfs.py` and `solvers/grater/jfs/construct.csv`, `solvers/grater/objective_functions_our.py` and `solvers/grater/our/construct.csv`, which may be helpful for reproducibility.

## XSat

We adapt XSat for fair comparison without effecting its performance, because XSat sometimes incorrectly reports `unsat` when the constraint is actually satisfiable as described in XSat's paper. The code of adapted XSat is in [xsat](https://github.com/grater-exp/grater-experiment/tree/master/solvers/xsat).

## CoverMe

CoverMe is not originally designed for floating-point constraints solving, so we adapt it to function as a floating-point constraint solver. The source code of adapted CoverMe is in [coverme](https://github.com/grater-exp/grater-experiment/tree/master/solvers/coverme). The way to run it is the same as [XSat](https://github.com/zhoulaifu/xsat).

## Other solvers

We build other baseline solvers using their release version as introduced [here](https://github.com/grater-exp/grater-experiment?tab=readme-ov-file#baselines). The methods to build and run them are all in their homepages:

[XSat](https://github.com/zhoulaifu/xsat)

[JFS](https://github.com/mc-imperial/jfs)

[Z3](https://github.com/Z3Prover/z3)

[CVC5](https://github.com/cvc5/cvc5)

[Bitwuzla](https://github.com/bitwuzla/bitwuzla)