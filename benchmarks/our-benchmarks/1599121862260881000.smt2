(set-info :smt-lib-version 2.6)
(set-logic QF_FP)
(set-info :source |
Generated by: Anastasiia Izycheva, Eva Darulova
Generated on: 2020-09-11
Generator: Pine (using Z3 Python API)
Application: Check inductiveness of a loop invariant
Target solver: CVC4

These benchmarks were generated while developing the tool Pine [1], which uses
CVC4/Z3 to check inductiveness of invariants. The work is described in [2].

[1] https://github.com/izycheva/pine
[2] A.Izycheva, E.Darulova, H.Seidl, SAS'20, "Counterexample- and Simulation-Guided Floating-Point Loop Invariant Synthesis"

 Loop:
   x1' := x1 + 0.01 * x2
   x2' := -0.01 * x1 + 0.99 * x2

 Input ranges:
   x1 in [0.0,1.0]
   x2 in [0.0,1.0]

 Invariant:
   -1.0*x1 + -0.32*x2 + 0.88*x1^2 + 0.19*x1*x2 + 0.73*x2^2 <= 0.54
 and
   x1 in [-0.4,1.5]
   x2 in [-0.9,1.0]

 Query: Loop and Invariant and not Invariant'
|)
(set-info :license "https://creativecommons.org/licenses/by/4.0/")
(set-info :category "industrial")
(set-info :status unknown)
(declare-fun x1!FP () (_ FloatingPoint 8 24))
(declare-fun x2!FP () (_ FloatingPoint 8 24))
(declare-fun x2FP () (_ FloatingPoint 8 24))
(declare-fun x1FP () (_ FloatingPoint 8 24))
(assert
 (let ((?x149 (fp.mul roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp #b0 #x7e #b01110101110000101000111) x2!FP) x2!FP)))
 (let ((?x15 (fp.add roundNearestTiesToEven ?x149 (fp.mul roundNearestTiesToEven (fp #b1 #x7f #b00000000000000000000000) x1!FP))))
 (let ((?x126 (fp.mul roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp #b0 #x7c #b10000101000111101011100) x1!FP) x2!FP)))
 (let ((?x19 (fp.mul roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp #b0 #x7e #b11000010100011110101110) x1!FP) x1!FP)))
 (let ((?x26 (fp.add roundNearestTiesToEven ?x19 (fp.add roundNearestTiesToEven ?x126 ?x15))))
 (let ((?x261 (fp.add roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp #b1 #x7d #b01000111101011100001010) x2!FP) ?x26)))
 (let (($x147 (fp.leq ?x261 (fp #b0 #x7e #b00010100011110101110000))))
 (let (($x132 (fp.leq x2!FP (fp #b0 #x7f #b00000000000000000000000))))
 (let (($x127 (fp.leq (fp #b1 #x7e #b11001100110011001100110) x2!FP)))
 (let (($x161 (fp.leq x1!FP (fp #b0 #x7f #b10000000000000000000000))))
 (let (($x83 (fp.leq (fp #b1 #x7d #b10011001100110011001100) x1!FP)))
 (let ((?x58 (fp.mul roundNearestTiesToEven (fp #b0 #x7e #b11111010111000010100011) x2FP)))
 (let ((?x133 (fp.add roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp.neg (fp #b0 #x78 #b01000111101011100001010)) x1FP) ?x58)))
 (let ((?x109 (fp.add roundNearestTiesToEven x1FP (fp.mul roundNearestTiesToEven (fp #b0 #x78 #b01000111101011100001010) x2FP))))
 (let (($x111 (fp.eq x1!FP ?x109)))
 (let ((?x46 (fp.mul roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp #b0 #x7e #b01110101110000101000111) x2FP) x2FP)))
 (let ((?x183 (fp.add roundNearestTiesToEven ?x46 (fp.mul roundNearestTiesToEven (fp #b1 #x7f #b00000000000000000000000) x1FP))))
 (let ((?x144 (fp.mul roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp #b0 #x7c #b10000101000111101011100) x1FP) x2FP)))
 (let ((?x39 (fp.mul roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp #b0 #x7e #b11000010100011110101110) x1FP) x1FP)))
 (let ((?x82 (fp.add roundNearestTiesToEven ?x39 (fp.add roundNearestTiesToEven ?x144 ?x183))))
 (let ((?x200 (fp.add roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp #b1 #x7d #b01000111101011100001010) x2FP) ?x82)))
 (let (($x84 (fp.leq ?x200 (fp #b0 #x7e #b00010100011110101110000))))
 (let (($x17 (fp.leq x2FP (fp #b0 #x7f #b00000000000000000000000))))
 (let (($x172 (fp.leq (fp #b1 #x7e #b11001100110011001100110) x2FP)))
 (let (($x106 (fp.leq x1FP (fp #b0 #x7f #b10000000000000000000000))))
 (let (($x190 (fp.leq (fp #b1 #x7d #b10011001100110011001100) x1FP)))
 (and (and (and $x190 $x106 $x172 $x17) $x84 ) (and $x111 (fp.eq x2!FP ?x133)) (or (not $x83) (not $x161) (not $x127) (not $x132) (not $x147))))))))))))))))))))))))))))))
(check-sat)
(exit)
