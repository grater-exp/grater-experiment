(set-info :smt-lib-version 2.6)
(set-logic QF_FP)
(set-info :category "crafted")
(set-info :source |Alberto Griggio <griggio@fbk.eu>. These benchmarks were used for the evaluation in the following paper: L. Haller, A. Griggio, M. Brain, D. Kroening: Deciding floating-point logic with systematic abstraction. FMCAD 2012. Real-numbered literals have been automatically translated by MathSAT|)
(set-info :status sat)
;; MathSAT API call trace
;; generated on 05/20/15 17:24:52

(declare-fun b64 () (_ FloatingPoint 8 24))
(declare-fun b85 () (_ FloatingPoint 8 24))
(declare-fun b49 () (_ FloatingPoint 8 24))
(declare-fun b172 () (_ FloatingPoint 8 24))
(declare-fun b91 () (_ FloatingPoint 8 24))
(declare-fun b34 () (_ FloatingPoint 8 24))
(declare-fun b16 () (_ FloatingPoint 8 24))
(declare-fun b40 () (_ FloatingPoint 8 24))
(declare-fun b28 () (_ FloatingPoint 8 24))
(declare-fun b76 () (_ FloatingPoint 8 24))
(declare-fun b25 () (_ FloatingPoint 8 24))
(declare-fun b37 () (_ FloatingPoint 8 24))
(declare-fun b43 () (_ FloatingPoint 8 24))
(declare-fun b70 () (_ FloatingPoint 8 24))
(declare-fun b61 () (_ FloatingPoint 8 24))
(declare-fun b79 () (_ FloatingPoint 8 24))
(declare-fun b11 () (_ FloatingPoint 8 24))
(declare-fun b94 () (_ FloatingPoint 8 24))
(declare-fun b169 () (_ FloatingPoint 8 24))
(declare-fun b22 () (_ FloatingPoint 8 24))
(declare-fun b88 () (_ FloatingPoint 8 24))
(declare-fun b82 () (_ FloatingPoint 8 24))
(declare-fun b55 () (_ FloatingPoint 8 24))
(declare-fun b46 () (_ FloatingPoint 8 24))
(declare-fun b97 () (_ FloatingPoint 8 24))
(declare-fun b13 () (_ FloatingPoint 8 24))
(declare-fun b31 () (_ FloatingPoint 8 24))
(declare-fun b101 () (_ FloatingPoint 11 53))
(declare-fun b73 () (_ FloatingPoint 8 24))
(declare-fun b58 () (_ FloatingPoint 8 24))
(declare-fun b67 () (_ FloatingPoint 8 24))
(declare-fun b52 () (_ FloatingPoint 8 24))
(declare-fun b19 () (_ FloatingPoint 8 24))
(define-fun _t_3 () RoundingMode RNE)
(define-fun _t_9 () (_ FloatingPoint 8 24) b169)
(define-fun _t_10 () (_ FloatingPoint 8 24) b11)
(define-fun _t_11 () Bool (fp.lt _t_9 _t_10))
(define-fun _t_12 () (_ FloatingPoint 8 24) b13)
(define-fun _t_13 () (_ FloatingPoint 8 24) (fp.mul _t_3 _t_10 _t_12))
(define-fun _t_14 () (_ FloatingPoint 8 24) b16)
(define-fun _t_15 () (_ FloatingPoint 8 24) (fp.mul _t_3 _t_13 _t_14))
(define-fun _t_16 () (_ FloatingPoint 8 24) b19)
(define-fun _t_17 () (_ FloatingPoint 8 24) (fp.mul _t_3 _t_15 _t_16))
(define-fun _t_18 () (_ FloatingPoint 8 24) b22)
(define-fun _t_19 () (_ FloatingPoint 8 24) (fp.mul _t_3 _t_17 _t_18))
(define-fun _t_20 () (_ FloatingPoint 8 24) b25)
(define-fun _t_21 () (_ FloatingPoint 8 24) (fp.mul _t_3 _t_19 _t_20))
(define-fun _t_22 () (_ FloatingPoint 8 24) b28)
(define-fun _t_23 () (_ FloatingPoint 8 24) (fp.mul _t_3 _t_21 _t_22))
(define-fun _t_24 () (_ FloatingPoint 8 24) b31)
(define-fun _t_25 () (_ FloatingPoint 8 24) (fp.mul _t_3 _t_23 _t_24))
(define-fun _t_26 () (_ FloatingPoint 8 24) b34)
(define-fun _t_27 () (_ FloatingPoint 8 24) (fp.mul _t_3 _t_25 _t_26))
(define-fun _t_28 () (_ FloatingPoint 8 24) b37)
(define-fun _t_29 () (_ FloatingPoint 8 24) (fp.mul _t_3 _t_27 _t_28))
(define-fun _t_30 () (_ FloatingPoint 8 24) b40)
(define-fun _t_31 () (_ FloatingPoint 8 24) (fp.mul _t_3 _t_29 _t_30))
(define-fun _t_32 () (_ FloatingPoint 8 24) b43)
(define-fun _t_33 () (_ FloatingPoint 8 24) (fp.mul _t_3 _t_31 _t_32))
(define-fun _t_34 () (_ FloatingPoint 8 24) b46)
(define-fun _t_35 () (_ FloatingPoint 8 24) (fp.mul _t_3 _t_33 _t_34))
(define-fun _t_36 () (_ FloatingPoint 8 24) b49)
(define-fun _t_37 () (_ FloatingPoint 8 24) (fp.mul _t_3 _t_35 _t_36))
(define-fun _t_38 () (_ FloatingPoint 8 24) b52)
(define-fun _t_39 () (_ FloatingPoint 8 24) (fp.mul _t_3 _t_37 _t_38))
(define-fun _t_40 () (_ FloatingPoint 8 24) b55)
(define-fun _t_41 () (_ FloatingPoint 8 24) (fp.mul _t_3 _t_39 _t_40))
(define-fun _t_42 () (_ FloatingPoint 8 24) b58)
(define-fun _t_43 () (_ FloatingPoint 8 24) (fp.mul _t_3 _t_41 _t_42))
(define-fun _t_44 () (_ FloatingPoint 8 24) b61)
(define-fun _t_45 () (_ FloatingPoint 8 24) (fp.mul _t_3 _t_43 _t_44))
(define-fun _t_46 () (_ FloatingPoint 8 24) b64)
(define-fun _t_47 () (_ FloatingPoint 8 24) (fp.mul _t_3 _t_45 _t_46))
(define-fun _t_48 () (_ FloatingPoint 8 24) b67)
(define-fun _t_49 () (_ FloatingPoint 8 24) (fp.mul _t_3 _t_47 _t_48))
(define-fun _t_50 () (_ FloatingPoint 8 24) b70)
(define-fun _t_51 () (_ FloatingPoint 8 24) (fp.mul _t_3 _t_49 _t_50))
(define-fun _t_52 () (_ FloatingPoint 8 24) b73)
(define-fun _t_53 () (_ FloatingPoint 8 24) (fp.mul _t_3 _t_51 _t_52))
(define-fun _t_54 () (_ FloatingPoint 8 24) b76)
(define-fun _t_55 () (_ FloatingPoint 8 24) (fp.mul _t_3 _t_53 _t_54))
(define-fun _t_56 () (_ FloatingPoint 8 24) b79)
(define-fun _t_57 () (_ FloatingPoint 8 24) (fp.mul _t_3 _t_55 _t_56))
(define-fun _t_58 () (_ FloatingPoint 8 24) b82)
(define-fun _t_59 () (_ FloatingPoint 8 24) (fp.mul _t_3 _t_57 _t_58))
(define-fun _t_60 () (_ FloatingPoint 8 24) b85)
(define-fun _t_61 () (_ FloatingPoint 8 24) (fp.mul _t_3 _t_59 _t_60))
(define-fun _t_62 () (_ FloatingPoint 8 24) b88)
(define-fun _t_63 () (_ FloatingPoint 8 24) (fp.mul _t_3 _t_61 _t_62))
(define-fun _t_64 () (_ FloatingPoint 8 24) b91)
(define-fun _t_65 () (_ FloatingPoint 8 24) (fp.mul _t_3 _t_63 _t_64))
(define-fun _t_66 () (_ FloatingPoint 8 24) b94)
(define-fun _t_67 () (_ FloatingPoint 8 24) (fp.mul _t_3 _t_65 _t_66))
(define-fun _t_68 () (_ FloatingPoint 8 24) b97)
(define-fun _t_69 () (_ FloatingPoint 8 24) (fp.mul _t_3 _t_67 _t_68))
(define-fun _t_70 () (_ FloatingPoint 11 53) ((_ to_fp 11 53) _t_3 _t_69))
(define-fun _t_71 () (_ FloatingPoint 11 53) b101)
(define-fun _t_72 () Bool (fp.lt _t_71 _t_70))
(define-fun _t_73 () Bool (and _t_11 _t_72))
(define-fun _t_74 () (_ FloatingPoint 8 24) b172)
(define-fun _t_75 () Bool (fp.lt _t_10 _t_74))
(define-fun _t_76 () Bool (and _t_73 _t_75))
(define-fun _t_77 () Bool (fp.lt _t_9 _t_12))
(define-fun _t_78 () Bool (and _t_76 _t_77))
(define-fun _t_79 () Bool (fp.lt _t_12 _t_74))
(define-fun _t_80 () Bool (and _t_78 _t_79))
(define-fun _t_81 () Bool (fp.lt _t_9 _t_14))
(define-fun _t_82 () Bool (and _t_80 _t_81))
(define-fun _t_83 () Bool (fp.lt _t_14 _t_74))
(define-fun _t_84 () Bool (and _t_82 _t_83))
(define-fun _t_85 () Bool (fp.lt _t_9 _t_16))
(define-fun _t_86 () Bool (and _t_84 _t_85))
(define-fun _t_87 () Bool (fp.lt _t_16 _t_74))
(define-fun _t_88 () Bool (and _t_86 _t_87))
(define-fun _t_89 () Bool (fp.lt _t_9 _t_18))
(define-fun _t_90 () Bool (and _t_88 _t_89))
(define-fun _t_91 () Bool (fp.lt _t_18 _t_74))
(define-fun _t_92 () Bool (and _t_90 _t_91))
(define-fun _t_93 () Bool (fp.lt _t_9 _t_20))
(define-fun _t_94 () Bool (and _t_92 _t_93))
(define-fun _t_95 () Bool (fp.lt _t_20 _t_74))
(define-fun _t_96 () Bool (and _t_94 _t_95))
(define-fun _t_97 () Bool (fp.lt _t_9 _t_22))
(define-fun _t_98 () Bool (and _t_96 _t_97))
(define-fun _t_99 () Bool (fp.lt _t_22 _t_74))
(define-fun _t_100 () Bool (and _t_98 _t_99))
(define-fun _t_101 () Bool (fp.lt _t_9 _t_24))
(define-fun _t_102 () Bool (and _t_100 _t_101))
(define-fun _t_103 () Bool (fp.lt _t_24 _t_74))
(define-fun _t_104 () Bool (and _t_102 _t_103))
(define-fun _t_105 () Bool (fp.lt _t_9 _t_26))
(define-fun _t_106 () Bool (and _t_104 _t_105))
(define-fun _t_107 () Bool (fp.lt _t_26 _t_74))
(define-fun _t_108 () Bool (and _t_106 _t_107))
(define-fun _t_109 () Bool (fp.lt _t_9 _t_28))
(define-fun _t_110 () Bool (and _t_108 _t_109))
(define-fun _t_111 () Bool (fp.lt _t_28 _t_74))
(define-fun _t_112 () Bool (and _t_110 _t_111))
(define-fun _t_113 () Bool (fp.lt _t_9 _t_30))
(define-fun _t_114 () Bool (and _t_112 _t_113))
(define-fun _t_115 () Bool (fp.lt _t_30 _t_74))
(define-fun _t_116 () Bool (and _t_114 _t_115))
(define-fun _t_117 () Bool (fp.lt _t_9 _t_32))
(define-fun _t_118 () Bool (and _t_116 _t_117))
(define-fun _t_119 () Bool (fp.lt _t_32 _t_74))
(define-fun _t_120 () Bool (and _t_118 _t_119))
(define-fun _t_121 () Bool (fp.lt _t_9 _t_34))
(define-fun _t_122 () Bool (and _t_120 _t_121))
(define-fun _t_123 () Bool (fp.lt _t_34 _t_74))
(define-fun _t_124 () Bool (and _t_122 _t_123))
(define-fun _t_125 () Bool (fp.lt _t_9 _t_36))
(define-fun _t_126 () Bool (and _t_124 _t_125))
(define-fun _t_127 () Bool (fp.lt _t_36 _t_74))
(define-fun _t_128 () Bool (and _t_126 _t_127))
(define-fun _t_129 () Bool (fp.lt _t_9 _t_38))
(define-fun _t_130 () Bool (and _t_128 _t_129))
(define-fun _t_131 () Bool (fp.lt _t_38 _t_74))
(define-fun _t_132 () Bool (and _t_130 _t_131))
(define-fun _t_133 () Bool (fp.lt _t_9 _t_40))
(define-fun _t_134 () Bool (and _t_132 _t_133))
(define-fun _t_135 () Bool (fp.lt _t_40 _t_74))
(define-fun _t_136 () Bool (and _t_134 _t_135))
(define-fun _t_137 () Bool (fp.lt _t_9 _t_42))
(define-fun _t_138 () Bool (and _t_136 _t_137))
(define-fun _t_139 () Bool (fp.lt _t_42 _t_74))
(define-fun _t_140 () Bool (and _t_138 _t_139))
(define-fun _t_141 () Bool (fp.lt _t_9 _t_44))
(define-fun _t_142 () Bool (and _t_140 _t_141))
(define-fun _t_143 () Bool (fp.lt _t_44 _t_74))
(define-fun _t_144 () Bool (and _t_142 _t_143))
(define-fun _t_145 () Bool (fp.lt _t_9 _t_46))
(define-fun _t_146 () Bool (and _t_144 _t_145))
(define-fun _t_147 () Bool (fp.lt _t_46 _t_74))
(define-fun _t_148 () Bool (and _t_146 _t_147))
(define-fun _t_149 () Bool (fp.lt _t_9 _t_48))
(define-fun _t_150 () Bool (and _t_148 _t_149))
(define-fun _t_151 () Bool (fp.lt _t_48 _t_74))
(define-fun _t_152 () Bool (and _t_150 _t_151))
(define-fun _t_153 () Bool (fp.lt _t_9 _t_50))
(define-fun _t_154 () Bool (and _t_152 _t_153))
(define-fun _t_155 () Bool (fp.lt _t_50 _t_74))
(define-fun _t_156 () Bool (and _t_154 _t_155))
(define-fun _t_157 () Bool (fp.lt _t_9 _t_52))
(define-fun _t_158 () Bool (and _t_156 _t_157))
(define-fun _t_159 () Bool (fp.lt _t_52 _t_74))
(define-fun _t_160 () Bool (and _t_158 _t_159))
(define-fun _t_161 () Bool (fp.lt _t_9 _t_54))
(define-fun _t_162 () Bool (and _t_160 _t_161))
(define-fun _t_163 () Bool (fp.lt _t_54 _t_74))
(define-fun _t_164 () Bool (and _t_162 _t_163))
(define-fun _t_165 () Bool (fp.lt _t_9 _t_56))
(define-fun _t_166 () Bool (and _t_164 _t_165))
(define-fun _t_167 () Bool (fp.lt _t_56 _t_74))
(define-fun _t_168 () Bool (and _t_166 _t_167))
(define-fun _t_169 () Bool (fp.lt _t_9 _t_58))
(define-fun _t_170 () Bool (and _t_168 _t_169))
(define-fun _t_171 () Bool (fp.lt _t_58 _t_74))
(define-fun _t_172 () Bool (and _t_170 _t_171))
(define-fun _t_173 () Bool (fp.lt _t_9 _t_60))
(define-fun _t_174 () Bool (and _t_172 _t_173))
(define-fun _t_175 () Bool (fp.lt _t_60 _t_74))
(define-fun _t_176 () Bool (and _t_174 _t_175))
(define-fun _t_177 () Bool (fp.lt _t_9 _t_62))
(define-fun _t_178 () Bool (and _t_176 _t_177))
(define-fun _t_179 () Bool (fp.lt _t_62 _t_74))
(define-fun _t_180 () Bool (and _t_178 _t_179))
(define-fun _t_181 () Bool (fp.lt _t_9 _t_64))
(define-fun _t_182 () Bool (and _t_180 _t_181))
(define-fun _t_183 () Bool (fp.lt _t_64 _t_74))
(define-fun _t_184 () Bool (and _t_182 _t_183))
(define-fun _t_185 () Bool (fp.lt _t_9 _t_66))
(define-fun _t_186 () Bool (and _t_184 _t_185))
(define-fun _t_187 () Bool (fp.lt _t_66 _t_74))
(define-fun _t_188 () Bool (and _t_186 _t_187))
(define-fun _t_189 () Bool (fp.lt _t_9 _t_68))
(define-fun _t_190 () Bool (and _t_188 _t_189))
(define-fun _t_191 () Bool (fp.lt _t_68 _t_74))
(define-fun _t_192 () Bool (and _t_190 _t_191))
(assert _t_192)
(check-sat)
(exit)
