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
   -1.0*x1 + -0.31*x2 + 0.85*x1^2 + 0.15*x1*x2 + 0.71*x2^2 <= 0.44
 and
   x1 in [-0.4,1.4]
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
 (let ((?x89 (fp.mul roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp #b0 #x7e #b01101011100001010001111) x2!FP) x2!FP)))
 (let ((?x129 (fp.add roundNearestTiesToEven ?x89 (fp.mul roundNearestTiesToEven (fp #b1 #x7f #b00000000000000000000000) x1!FP))))
 (let ((?x46 (fp.mul roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp #b0 #x7c #b00110011001100110011001) x1!FP) x2!FP)))
 (let ((?x244 (fp.mul roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp #b0 #x7e #b10110011001100110011001) x1!FP) x1!FP)))
 (let ((?x126 (fp.add roundNearestTiesToEven ?x244 (fp.add roundNearestTiesToEven ?x46 ?x129))))
 (let ((?x241 (fp.add roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp #b1 #x7d #b00111101011100001010001) x2!FP) ?x126)))
 (let (($x67 (fp.leq ?x241 (fp #b0 #x7d #b11000010100011110101110))))
 (let (($x132 (fp.leq x2!FP (fp #b0 #x7f #b00000000000000000000000))))
 (let (($x127 (fp.leq (fp #b1 #x7e #b11001100110011001100110) x2!FP)))
 (let (($x183 (fp.leq x1!FP (fp #b0 #x7f #b01100110011001100110011))))
 (let (($x83 (fp.leq (fp #b1 #x7d #b10011001100110011001100) x1!FP)))
 (let ((?x58 (fp.mul roundNearestTiesToEven (fp #b0 #x7e #b11111010111000010100011) x2FP)))
 (let ((?x133 (fp.add roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp.neg (fp #b0 #x78 #b01000111101011100001010)) x1FP) ?x58)))
 (let ((?x109 (fp.add roundNearestTiesToEven x1FP (fp.mul roundNearestTiesToEven (fp #b0 #x78 #b01000111101011100001010) x2FP))))
 (let (($x111 (fp.eq x1!FP ?x109)))
 (let ((?x16 (fp.mul roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp #b0 #x7e #b01101011100001010001111) x2FP) x2FP)))
 (let ((?x8 (fp.add roundNearestTiesToEven ?x16 (fp.mul roundNearestTiesToEven (fp #b1 #x7f #b00000000000000000000000) x1FP))))
 (let ((?x125 (fp.mul roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp #b0 #x7c #b00110011001100110011001) x1FP) x2FP)))
 (let ((?x135 (fp.mul roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp #b0 #x7e #b10110011001100110011001) x1FP) x1FP)))
 (let ((?x213 (fp.add roundNearestTiesToEven ?x135 (fp.add roundNearestTiesToEven ?x125 ?x8))))
 (let ((?x136 (fp.add roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp #b1 #x7d #b00111101011100001010001) x2FP) ?x213)))
 (let (($x184 (fp.leq ?x136 (fp #b0 #x7d #b11000010100011110101110))))
 (let (($x17 (fp.leq x2FP (fp #b0 #x7f #b00000000000000000000000))))
 (let (($x172 (fp.leq (fp #b1 #x7e #b11001100110011001100110) x2FP)))
 (let (($x212 (fp.leq x1FP (fp #b0 #x7f #b01100110011001100110011))))
 (let (($x190 (fp.leq (fp #b1 #x7d #b10011001100110011001100) x1FP)))
 (and (and (and $x190 $x212 $x172 $x17) $x184 ) (and $x111 (fp.eq x2!FP ?x133)) (or (not $x83) (not $x183) (not $x127) (not $x132) (not $x67))))))))))))))))))))))))))))))
(check-sat)
(exit)
