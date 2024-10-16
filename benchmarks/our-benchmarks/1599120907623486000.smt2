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
   x' := x + 0.01 * (-2*x - 3*y + x*x)
   y' := y + 0.01 * (x + y)

 Input ranges:
   x in [0.0,0.1]
   y in [0.0,0.1]

 Invariant:
   -0.02*x + -0.13*y + 0.54*x^2 + 1.0*x*y + 0.93*y^2 <= 0.02
 and
   x in [-0.4,0.2]
   y in [-0.2,0.4]

 Query: Loop and Invariant and not Invariant'
|)
(set-info :license "https://creativecommons.org/licenses/by/4.0/")
(set-info :category "industrial")
(set-info :status unknown)
(declare-fun x!FP () (_ FloatingPoint 8 24))
(declare-fun y!FP () (_ FloatingPoint 8 24))
(declare-fun yFP () (_ FloatingPoint 8 24))
(declare-fun xFP () (_ FloatingPoint 8 24))
(assert
 (let ((?x234 (fp.mul roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp #b0 #x7e #b11011100001010001111010) y!FP) y!FP)))
 (let ((?x241 (fp.add roundNearestTiesToEven ?x234 (fp.mul roundNearestTiesToEven (fp #b1 #x79 #b01000111101011100001010) x!FP))))
 (let ((?x240 (fp.mul roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp #b0 #x7f #b00000000000000000000000) x!FP) y!FP)))
 (let ((?x239 (fp.mul roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp #b0 #x7e #b00010100011110101110000) x!FP) x!FP)))
 (let ((?x236 (fp.add roundNearestTiesToEven ?x239 (fp.add roundNearestTiesToEven ?x240 ?x241))))
 (let ((?x228 (fp.add roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp #b1 #x7c #b00001010001111010111000) y!FP) ?x236)))
 (let (($x242 (fp.leq ?x228 (fp #b0 #x79 #b01000111101011100001010))))
 (let (($x210 (fp.leq y!FP (fp #b0 #x7d #b10011001100110011001100))))
 (let (($x222 (fp.leq (fp #b1 #x7c #b10011001100110011001100) y!FP)))
 (let (($x165 (fp.leq x!FP (fp #b0 #x7c #b10011001100110011001100))))
 (let (($x140 (fp.leq (fp #b1 #x7d #b10011001100110011001100) x!FP)))
 (let ((?x155 (fp.mul roundNearestTiesToEven (fp #b0 #x78 #b01000111101011100001010) (fp.add roundNearestTiesToEven xFP yFP))))
 (let (($x157 (fp.eq y!FP (fp.add roundNearestTiesToEven yFP ?x155))))
 (let ((?x149 (fp.mul roundNearestTiesToEven xFP xFP)))
 (let ((?x147 (fp.mul roundNearestTiesToEven (fp #b0 #x80 #b10000000000000000000000) yFP)))
 (let ((?x148 (fp.sub roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp.neg (fp #b0 #x80 #b00000000000000000000000)) xFP) ?x147)))
 (let ((?x151 (fp.mul roundNearestTiesToEven (fp #b0 #x78 #b01000111101011100001010) (fp.add roundNearestTiesToEven ?x148 ?x149))))
 (let (($x159 (and (fp.eq x!FP (fp.add roundNearestTiesToEven xFP ?x151)) $x157)))
 (let ((?x123 (fp.mul roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp #b0 #x7e #b11011100001010001111010) yFP) yFP)))
 (let ((?x127 (fp.add roundNearestTiesToEven ?x123 (fp.mul roundNearestTiesToEven (fp #b1 #x79 #b01000111101011100001010) xFP))))
 (let ((?x169 (fp.mul roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp #b0 #x7f #b00000000000000000000000) xFP) yFP)))
 (let ((?x176 (fp.mul roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp #b0 #x7e #b00010100011110101110000) xFP) xFP)))
 (let ((?x132 (fp.add roundNearestTiesToEven ?x176 (fp.add roundNearestTiesToEven ?x169 ?x127))))
 (let ((?x136 (fp.add roundNearestTiesToEven (fp.mul roundNearestTiesToEven (fp #b1 #x7c #b00001010001111010111000) yFP) ?x132)))
 (let (($x137 (fp.leq ?x136 (fp #b0 #x79 #b01000111101011100001010))))
 (let (($x163 (fp.leq yFP (fp #b0 #x7d #b10011001100110011001100))))
 (let (($x258 (fp.leq (fp #b1 #x7c #b10011001100110011001100) yFP)))
 (let (($x179 (fp.leq xFP (fp #b0 #x7c #b10011001100110011001100))))
 (let (($x164 (fp.leq (fp #b1 #x7d #b10011001100110011001100) xFP)))
 (and (and (and $x164 $x179 $x258 $x163) $x137 ) $x159 (or (not $x140) (not $x165) (not $x222) (not $x210) (not $x242)))))))))))))))))))))))))))))))))
(check-sat)
(exit)
