import Mathlib


-- --test case
-- variable (a b : Nat)
-- theorem square_of_sum : (a + b) ^ 2 = a ^ 2 + 2 * a * b + b ^ 2 := by {
--   calc
--       (a + b) ^ 2 = (a + b) * (a + b)        := by rw [pow_two]
--        _ = a * (a + b) + b * (a + b)  := by ring
--        _ = a * a + a * b + (b * a + b * b) := by ring
--        _ = a^2 + a*b + b*a + b^2     := by rw [pow_two, pow_two]
--        _ = a^2 + 2*a*b + b^2         := by rw [Nat.add_assoc, Nat.mul_comm b, ←Nat.add_assoc];
-- }


--test case
theorem square_binomial (a b : Int) : (a + b)^2 = a^2 + 2*a*b + b^2 :=
  by calc
    (a + b)^2 = (a + b) * (a + b)         := by rfl
        _ = a * (a + b) + b * (a + b)   := by rw [Int.mul_add]
        _ = a * a + a * b + b * (a + b) := by rw [Int.add_mul]
        _ = a * a + a * b + (b * a + b * b) := by rw [Int.add_mul]
        _ = a^2 + a * b + b * a + b^2   := by rfl
        _ = a^2 + a * b + a * b + b^2   := by rw [Int.mul_comm b a]
        _ = a^2 + 2 * a * b + b^2       := by rw [Int.mul_two]

--test case
variable (a b : Int)
theorem binomial_expansion : (a + b)^2 = a^2 + 2*a*b + b^2 := by
  calc (a + b)^2
      _ = (a + b) * (a + b) : by ring
      _ = a^2 + a*b + b*a + b^2 : by ring
      _ = a^2 + a*b + a*b + b^2 : by rw [Int.mul_comm b a]
      _ = a^2 + 2*a*b + b^2 : by ring
