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
   -0.58*u + 0.02*v + 1.0*u^2 + -0.14*u*v + 0.05*v^2 <= 0.55
 and
   u in [-0.3,1.2]
   v in [-3.1,3.0]

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
 (let ((?x239 (fp.mul roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp #b0 #x7a #b10011001100110011001100) v!FP) v!FP)))
 (let ((?x164 (fp.add roundNearestTiesToEven ?x239 (fp.mul roundNearestTiesToEven (fp #b1 #x7e #b00101000111101011100001) u!FP))))
 (let ((?x113 (fp.mul roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp #b1 #x7c #b00011110101110000101000) u!FP) v!FP)))
 (let ((?x127 (fp.mul roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp #b0 #x7f #b00000000000000000000000) u!FP) u!FP)))
 (let ((?x204 (fp.add roundNearestTiesToEven ?x127 (fp.add roundNearestTiesToEven ?x113 ?x164))))
 (let ((?x185 (fp.add roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp #b0 #x79 #b01000111101011100001010) v!FP) ?x204)))
 (let (($x119 (fp.leq ?x185 (fp #b0 #x7e #b00011001100110011001100))))
 (let (($x123 (fp.leq v!FP (fp #b0 #x80 #b10000000000000000000000))))
 (let (($x165 (fp.leq (fp #b1 #x80 #b10001100110011001100110) v!FP)))
 (let (($x242 (fp.leq u!FP (fp #b0 #x7f #b00110011001100110011001))))
 (let (($x160 (fp.leq (fp #b1 #x7d #b00110011001100110011001) u!FP)))
 (let ((?x147 (fp.mul roundNearestTiesToEven (fp #b0 #x82 #b00111001111010111000010) uFP)))
 (let ((?x148 (fp.sub roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp.neg (fp #b0 #x7e #b00000000000000000000000)) vFP) ?x147)))
 (let ((?x150 (fp.add roundNearestTiesToEven vFP (fp.mul roundNearestTiesToEven (fp #b0 #x78 #b01000111101011100001010) ?x148))))
 (let ((?x141 (fp.add roundNearestTiesToEven uFP (fp.mul roundNearestTiesToEven (fp #b0 #x78 #b01000111101011100001010) vFP))))
 (let (($x142 (fp.eq u!FP ?x141)))
 (let ((?x100 (fp.mul roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp #b0 #x7a #b10011001100110011001100) vFP) vFP)))
 (let ((?x207 (fp.add roundNearestTiesToEven ?x100 (fp.mul roundNearestTiesToEven (fp #b1 #x7e #b00101000111101011100001) uFP))))
 (let ((?x107 (fp.mul roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp #b1 #x7c #b00011110101110000101000) uFP) vFP)))
 (let ((?x105 (fp.mul roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp #b0 #x7f #b00000000000000000000000) uFP) uFP)))
 (let ((?x226 (fp.add roundNearestTiesToEven ?x105 (fp.add roundNearestTiesToEven ?x107 ?x207))))
 (let ((?x217 (fp.add roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp #b0 #x79 #b01000111101011100001010) vFP) ?x226)))
 (let (($x252 (fp.leq ?x217 (fp #b0 #x7e #b00011001100110011001100))))
 (let (($x92 (fp.leq vFP (fp #b0 #x80 #b10000000000000000000000))))
 (let (($x180 (fp.leq (fp #b1 #x80 #b10001100110011001100110) vFP)))
 (let (($x208 (fp.leq uFP (fp #b0 #x7f #b00110011001100110011001))))
 (let (($x167 (fp.leq (fp #b1 #x7d #b00110011001100110011001) uFP)))
 (and (and (and $x167 $x208 $x180 $x92) $x252 ) (and $x142 (fp.eq v!FP ?x150)) (or (not $x160) (not $x242) (not $x165) (not $x123) (not $x119)))))))))))))))))))))))))))))))
(check-sat)
(exit)
