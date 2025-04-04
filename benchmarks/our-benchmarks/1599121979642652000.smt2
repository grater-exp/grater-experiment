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
   -0.1*u + -0.01*v + 1.0*u^2 + 0.03*u*v + 0.1*v^2 <= 1.64
 and
   u in [-1.3,1.3]
   v in [-4.0,3.7]

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
 (let ((?x258 (fp.mul roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp #b0 #x7b #b10011001100110011001100) v!FP) v!FP)))
 (let ((?x164 (fp.add roundNearestTiesToEven ?x258 (fp.mul roundNearestTiesToEven (fp #b1 #x7b #b10011001100110011001100) u!FP))))
 (let ((?x170 (fp.mul roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp #b0 #x79 #b11101011100001010001111) u!FP) v!FP)))
 (let ((?x55 (fp.mul roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp #b0 #x7f #b00000000000000000000000) u!FP) u!FP)))
 (let ((?x139 (fp.add roundNearestTiesToEven ?x55 (fp.add roundNearestTiesToEven ?x170 ?x164))))
 (let ((?x148 (fp.add roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp #b1 #x78 #b01000111101011100001010) v!FP) ?x139)))
 (let (($x200 (fp.leq ?x148 (fp #b0 #x7f #b10100011110101110000101))))
 (let (($x162 (fp.leq v!FP (fp #b0 #x80 #b11011001100110011001100))))
 (let (($x180 (fp.leq (fp #b1 #x81 #b00000000000000000000000) v!FP)))
 (let (($x165 (fp.leq u!FP (fp #b0 #x7f #b01001100110011001100110))))
 (let (($x219 (fp.leq (fp #b1 #x7f #b01001100110011001100110) u!FP)))
 (let ((?x206 (fp.mul roundNearestTiesToEven (fp #b0 #x82 #b00111001111010111000010) uFP)))
 (let ((?x212 (fp.sub roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp.neg (fp #b0 #x7e #b00000000000000000000000)) vFP) ?x206)))
 (let ((?x209 (fp.add roundNearestTiesToEven vFP (fp.mul roundNearestTiesToEven (fp #b0 #x78 #b01000111101011100001010) ?x212))))
 (let ((?x207 (fp.add roundNearestTiesToEven uFP (fp.mul roundNearestTiesToEven (fp #b0 #x78 #b01000111101011100001010) vFP))))
 (let (($x208 (fp.eq u!FP ?x207)))
 (let ((?x37 (fp.mul roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp #b0 #x7b #b10011001100110011001100) vFP) vFP)))
 (let ((?x123 (fp.add roundNearestTiesToEven ?x37 (fp.mul roundNearestTiesToEven (fp #b1 #x7b #b10011001100110011001100) uFP))))
 (let ((?x224 (fp.mul roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp #b0 #x79 #b11101011100001010001111) uFP) vFP)))
 (let ((?x67 (fp.mul roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp #b0 #x7f #b00000000000000000000000) uFP) uFP)))
 (let ((?x135 (fp.add roundNearestTiesToEven ?x67 (fp.add roundNearestTiesToEven ?x224 ?x123))))
 (let ((?x90 (fp.add roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp #b1 #x78 #b01000111101011100001010) vFP) ?x135)))
 (let (($x133 (fp.leq ?x90 (fp #b0 #x7f #b10100011110101110000101))))
 (let (($x111 (fp.leq vFP (fp #b0 #x80 #b11011001100110011001100))))
 (let (($x100 (fp.leq (fp #b1 #x81 #b00000000000000000000000) vFP)))
 (let (($x38 (fp.leq uFP (fp #b0 #x7f #b01001100110011001100110))))
 (let (($x110 (fp.leq (fp #b1 #x7f #b01001100110011001100110) uFP)))
 (and (and (and $x110 $x38 $x100 $x111) $x133 ) (and $x208 (fp.eq v!FP ?x209)) (or (not $x219) (not $x165) (not $x180) (not $x162) (not $x200)))))))))))))))))))))))))))))))
(check-sat)
(exit)
