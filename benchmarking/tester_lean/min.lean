import Mathlib



example {n M : Nat } (h1: 4*n + 2 = M) (h2: M = 6) : (Odd n) := by
simp [Odd]
have h : n = 1 :=
  calc
    n = (4*n + 2 - 2)/4 := by norm_num
    _ = (M - 2)/4 := by rw [← h1]
    _ = (6 - 2)/4 := by rw [h2]
    _ = 1 := by ring
rw [h]
use 0
norm_num

-- Huckel's rule describes conditions for aromaticity of cyclic molecules.

def aromatic (M : ℕ ) : Prop := ∃ n, ((M = 4*n + 2) ∧ (Odd n))

theorem Huckel_rule (h1 : b_M = 6) : aromatic b_M := by
  use 1
  constructor
  · -- Prove b_M s= 4*1 + 2
    calc
      b_M = 6     := by rw [h1]
      _   = 4*1+2 := by ring
  · --  Odd 1
    norm_num



#check Huckel_rule
