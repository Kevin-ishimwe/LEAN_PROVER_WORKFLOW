import Mathlib
/- Copyright (c) Heather Macbeth, 2022.  All rights reserved. -/
/- please check semantics -/

example :2 ≤ 20 := by linarith
-- delete right tactic portion to prove left side or delete left tactic portion to prove right side
example {d1 s1 d2 s2 x1 x2 : ℝ} (h1 : d1 = 5) (h2 : s1 = 50) (h3 : d2 = 1) (h4 : s2 = 30)
(h5 : x1 = d1/s1) (h6 : x2 = d2/s2): x1 ≤ 0.3333 ∨  x2 ≤ 0.3333 := by
  left
  calc
    x1 = d1/s1 := by rw[h5]
    _ = 5/s1 := by rw [h1]
    _ = 5/50 := by rw [h2]
    _ ≤ 0.3333 := by norm_num







theorem square_expansion (a b : ℕ ):(a + b) ^ 2 = a ^ 2 + 2 * a * b + b ^ 2 := by ring

--test case
theorem gas_law_eq {p1 v1 p2 v2 n1 n2 r t1 t2 : ℝ}
(h1 : p1 * v1 = n1 * r * t1)
(h2: p2 * v2 = n2 * r * t2)
(h3: t1 = t2) (h4: n1 = n2)
: p1 * v1 = p2 * v2 :=
  calc
    p1 * v1 = n1 * r * t1 := by rw [h1]
    _= n2 * r * t1 := by rw [h4]
    _= n2 * r * t2 := by rw [← h3]
    _= p2 * v2 := by rw [h2]

--test case
theorem p1v1_is_p2v2 {p1 v1 p2 v2 n1 n2 r t1 t2 : ℝ}
(h1 : p1 * v1 = n1 * r * t1)
(h2 : p2 * v2 = n2 * r * t2)
(h3 : t1 = t2) (h4: n1 = n2) : p1 * v1 = p2 * v2 :=
calc
  p1 * v1 = n1 * r * t1 := by rw [h1]
  _ = n2 * r * t2 := by rw [h4, h3]
  _ = p2 * v2 := by rw  [h2]

--test case
theorem
ideal_gas_law
{p1 v1 p2 v2 n1 r t1 n2 t2 : ℝ}
(h1 : p1 * v1 = n1 * r * t1)
(h2 : p2 * v2 = n2 * r * t2)
(h3: t1 = t2) (h4: n1 = n2):
p1 * v1 = p2 * v2  :=
calc
p1 * v1 = n1 * r * t1 := by rw[h1]
  _=n2 * r * t2 := by rw [h4, h3]  _=p2 * v2 := by rw [←h2]


--test case
example {c:ℝ }:c*c=c^2:=by simp [sq]

example {a b:ℕ  }:(a+b)^2=a^2+2*a*b+b^2:=by
calc
(a+b)^2=(a+b)*(a+b):=by simp [sq]
_=(a*a)+a*b+b*a+(b*b):=by ring
_=(a^2)+a*b+b*a+(b^2):=by simp [sq]
_=(a^2)+2*a*b+(b^2):=by ring


def divme (c:ℝ ):Prop:=c/c=1
--test case
theorem pythagorean_triple {a b c : ℝ}
(h1 : sin =a/c)
(h2: cos =b/c)
(h3: sin^2 + cos^2 = 1)
(h5:c/c=1): c^2 = a^2 + b^2 :=
calc
(c^2) = 1 * c^2 := by ring
  _ = (sin^2 + cos^2) * c^2 := by rw[h3]
  _= sin^2 * c^2 + cos^2 * c^2 := by ring
  _= (a/c)^2 * c^2 + (b/c)^2 * c^2 := by rw [h1,h2]
  _= (a^2/c^2) * c^2 + (b^2/c^2) * c^2 := by simp
  _= a^2*(c^2/c^2) + b^2*(c^2/c^2) := by ring
  _=a^2*((c/c)^2) + b^2*((c/c)^2) := by simp
  _= a^2*(1^2) + b^2*(1^2) := by rw[h5]
  _=a^2+b^2:=by norm_num

--test case
example : 4 = 4 :=by norm_num

--test case
example {a b : ℕ} (h1: a = 5) (h2: b = 2) : a > b :=by simp [h1,h2]

--test case
example {a b :ℕ }(h1: a=5)(h2: b=2): a > b := by simp [h1, h2]

--test case
example : 9 = 9 := by norm_num
--test case
example {a b : ℕ} (h1: a = 3) (h2: b = 12): b - a = 9 :=
calc
  b - a = 12 - 3 := by rw [h2, h1]
  _= 9 := by linarith

--test case
theorem ke_is_p_ {m v ke p :ℝ }(h1 : ke = 1 / 2 * m * v ^ 2)(h2: p=m*v)(h5:v/v=1):ke = p ^ 2 / (2 * m) :=
calc
  ke = 1 / 2 * m * v ^ 2 := by rw[h1]
  _= 1 / 2 * m * (v * v):= by simp [sq]
  _ = 1 / 2 *( m * v )* v := by ring
  _=1 / 2 *( p)* v := by rw [h2]
  _=1/2 * (p ^2*1/p)*v := by simp [sq]
  _=1/2*(p^2*1/(m*v))*v :=by rw[h2]
  _=1/2*(p^2)*(v/v* 1/m):= by ring
  _=1/2*(p^2)*(1* 1/m):= by rw[h5]
  _ = p ^ 2 / (2 * m) := by ring

--test case
theorem square_eq_sq {a : ℝ} : a * a = a ^ 2 := by simp [sq]

--test case
theorem add_sq_eq_expanded {a b : ℝ} : (a + b) ^ 2 = a ^ 2 + 2 * a * b + b ^ 2 :=
calc
  (a + b) ^ 2 = a ^ 2 + 2 * a * b + b ^ 2 := by simp[sq];ring

--test case
theorem four_eq_four : 4 = 4 := by norm_num
theorem sq_identity{a b  : ℝ} : (a + b) ^ 2 = a ^ 2 + 2 * a * b + b ^ 2 :=
calc
(a + b) ^ 2 = (a + b) * (a + b) := by simp[sq]
_ = a * (a + b) + b * (a + b) := by ring
_ = a * a + a * b + b * a + b * b := by rcases; ring
_ = a^2 + a * b + a * b + b^2 := by simp[sq]; ring
_ = a^2 + 2 * a * b + b^2 := by ring

theorem square_of_sum
(a b : Int) : (a + b) ^ 2 = a ^ 2 + 2 * a * b + b ^ 2 :=
by ring

--test case
theorem square_of_sums (a b : ℝ) : (a + b) ^ 2 = a ^ 2 + 2 * a * b + b ^ 2 :=
calc
  (a + b) ^ 2 = (a+b)*(a+b) := by simp[sq]
  _ = a^2 + 2*a*b + b^2 := by rcases;ring_nf;simp[sq]

--test case
theorem squarexpansionw (a b : Nat) : (a + b) ^ 2 = a ^ 2 + 2 * a * b + b ^ 2 := by ring

--test case
variable {ke m v p :ℝ }
theorem ke_eq_psq_over_2m
(h1 : ke = 1 / 2 * m * v^2)
(h2: p = m * v)
(h3: m / m = 1): ke = p^2 / (2 * m) :=
calc
  ke = 1 / 2 * m * v ^ 2 := by rw[h1] --start with h1 because it can work other wise you start with an expresion that is alwas mathematically true
  _ = 1 / 2 * (m * v) * v := by simp [sq];ring --also the left hand is used as _ now and the first tactic disect ^2 and regroup (m*v) from m*v*v using ring
  _ = 1 / 2 * p * v *1:= by rw[h2];ring; --rewrite and add *1 we need this to be there explicitly because we will be using it for m/m
  _ = 1 / 2 * p * v * (m / m) := by rw[h3] --rw 1 to m*m
  _ = 1 / 2 * p * (m * v) / m := by ring --regroup
  _ = 1 / 2 * p * p / m := by rw[h2] --rw part to p
  _ = p ^ 2 / (2 * m) := by simp[sq];ring --p*p=p^2 using simp[sq] and regroup to match final proof goal

--test case
theorem twelve_equals_twelve : 12 = 12 := by norm_num

theorem test: 3*2=6 := by simp
--test case
theorem ideal_gas_law_equal_conditions (p1 v1 n1 r t1 p2 v2 n2 t2: ℝ) (h1: p1 * v1 = n1 * r * t1) (h2: p2 * v2 = n2 * r * t2) (h3: t1 = t2) (h4: n1 = n2) : p1 * v1 = p2 * v2 := by rw [h1, h4, h3, h2]

--test case
theorem show_128_eq_128 : 128 = 128 := by rfl

--test case
variable (p1 v1 n1 r t1 p2 v2 n2 t2: Real)
theorem ideal_gas_law_equivalence (h1 : p1 * v1 = n1 * r * t1) (h2 : p2 * v2 = n2 * r * t2) (h3 : t1 = t2) (h4 : n1 = n2) : p1 * v1 = p2 * v2 :=
calc
  p1 * v1 = n1 * r * t1 := by rw[h1]
  _ = n2 * r * t1 := by rw[h4]
  _ = n2 * r * t2 := by rw[h3]
  _ = p2 * v2 := by rw[h2]

--test case
variable (p1 v1 p2 v2 n1 n2 r t1 t2 : ℝ)
theorem ideal_gvas_law (h1 : p1 * v1 = n1 * r * t1) (h2 : p2 * v2 = n2 * r * t2) (h3 : t1 = t2) (h4 : n1 = n2) : p1 * v1 = p2 * v2 :=
calc
  p1 * v1 = n1 * r * t1 := by rw[h1]
  _ = n2 * r * t1 := by rw[h4]
  _ = n2 * r * t2 := by rw[h3]
  _ = p2 * v2 := by rw[h2]


--test case
theorem seventy_five_equals : 75 = 75 := by rfl
--test case
theorem equal_pv (h1: p1 * v1 = n1 * r * t1) (h2: p2 * v2 = n2 * r * t2) (h3: t1 = t2) (h4: n1 = n2) : p1 * v1 = p2 * v2 :=
    by rw [h1, h4, h3, h2]
--test case
theorem show_b_two (a b : Nat) (h1 : a + b = 12) (h2 : a = 10) : b = 2 := by rw [h2] at h1; linarith
--test case
theorem square_of_msum (a b : Int) : (a + b) ^ 2 = a ^ 2 + 2 * a * b + b ^ 2 :=
by calc
      (a + b) ^ 2= (a + b) * (a + b) := by ring
      _ = a * (a + b) + b * (a + b) := by ring
      _ = a * a + a * b + b * a + b * b := by ring
      _ = a^2 + a * b + a * b + b^2 := by ring
      _ = a^2 + 2 * a * b + b^2 := by ring

--test case
theorem trivial_equality : 3 = 3 := by rfl

--test case
theorem four_equals_four : 4 = 4 := by rfl
