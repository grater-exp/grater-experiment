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
   u' := u + 0.01 * v
   v' := v + 0.01 * (-0.5 * v - 9.81 * u)

 Input ranges:
   u in [0.0,0.0]
   v in [2.0,3.0]

 Invariant:
   -1.0*u + 0.21*v + 0.94*u^2 + -0.11*u*v + 0.06*v^2 <= 1.27
 and
   u in [-0.6,1.9]
   v in [-6.3,3.0]

 Query: Loop and Invariant and not Invariant'
|)
(set-info :license "https://creativecommons.org/licenses/by/4.0/")
(set-info :category "industrial")
(set-info :status unknown)
(declare-fun u!FP () (_ FloatingPoint 8 24))
(declare-fun v!FP () (_ FloatingPoint 8 24))
(declare-fun uFP () (_ FloatingPoint 8 24))
(declare-fun vFP () (_ FloatingPoint 8 24))
(assert
 (let ((?x112 (fp.mul roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp #b0 #x7a #b11101011100001010001111) v!FP) v!FP)))
 (let ((?x125 (fp.add roundNearestTiesToEven ?x112 (fp.mul roundNearestTiesToEven (fp #b1 #x7f #b00000000000000000000000) u!FP))))
 (let ((?x195 (fp.mul roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp #b1 #x7b #b11000010100011110101110) u!FP) v!FP)))
 (let ((?x159 (fp.mul roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp #b0 #x7e #b11100001010001111010111) u!FP) u!FP)))
 (let ((?x221 (fp.add roundNearestTiesToEven ?x159 (fp.add roundNearestTiesToEven ?x195 ?x125))))
 (let ((?x201 (fp.add roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp #b0 #x7c #b10101110000101000111101) v!FP) ?x221)))
 (let (($x281 (fp.leq ?x201 (fp #b0 #x7f #b01000101000111101011100))))
 (let (($x123 (fp.leq v!FP (fp #b0 #x80 #b10000000000000000000000))))
 (let (($x228 (fp.leq (fp #b1 #x81 #b10010011001100110011001) v!FP)))
 (let (($x113 (fp.leq u!FP (fp #b0 #x7f #b11100110011001100110011))))
 (let (($x185 (fp.leq (fp #b1 #x7e #b00110011001100110011001) u!FP)))
 (let ((?x147 (fp.mul roundNearestTiesToEven (fp #b0 #x82 #b00111001111010111000010) uFP)))
 (let ((?x148 (fp.sub roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp.neg (fp #b0 #x7e #b00000000000000000000000)) vFP) ?x147)))
 (let ((?x150 (fp.add roundNearestTiesToEven vFP (fp.mul roundNearestTiesToEven (fp #b0 #x78 #b01000111101011100001010) ?x148))))
 (let ((?x141 (fp.add roundNearestTiesToEven uFP (fp.mul roundNearestTiesToEven (fp #b0 #x78 #b01000111101011100001010) vFP))))
 (let (($x142 (fp.eq u!FP ?x141)))
 (let ((?x290 (fp.mul roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp #b0 #x7a #b11101011100001010001111) vFP) vFP)))
 (let ((?x218 (fp.add roundNearestTiesToEven ?x290 (fp.mul roundNearestTiesToEven (fp #b1 #x7f #b00000000000000000000000) uFP))))
 (let ((?x280 (fp.mul roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp #b1 #x7b #b11000010100011110101110) uFP) vFP)))
 (let ((?x182 (fp.mul roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp #b0 #x7e #b11100001010001111010111) uFP) uFP)))
 (let ((?x35 (fp.add roundNearestTiesToEven ?x182 (fp.add roundNearestTiesToEven ?x280 ?x218))))
 (let ((?x222 (fp.add roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp #b0 #x7c #b10101110000101000111101) vFP) ?x35)))
 (let (($x64 (fp.leq ?x222 (fp #b0 #x7f #b01000101000111101011100))))
 (let (($x92 (fp.leq vFP (fp #b0 #x80 #b10000000000000000000000))))
 (let (($x104 (fp.leq (fp #b1 #x81 #b10010011001100110011001) vFP)))
 (let (($x107 (fp.leq uFP (fp #b0 #x7f #b11100110011001100110011))))
 (let (($x102 (fp.leq (fp #b1 #x7e #b00110011001100110011001) uFP)))
 (and (and (and $x102 $x107 $x104 $x92) $x64 ) (and $x142 (fp.eq v!FP ?x150)) (or (not $x185) (not $x113) (not $x228) (not $x123) (not $x281)))))))))))))))))))))))))))))))
(check-sat)
(exit)
