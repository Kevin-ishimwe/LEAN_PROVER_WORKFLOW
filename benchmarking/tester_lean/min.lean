import Mathlib

/- A toy mouse changes speed from a constant 2 m/s to 0 m/s in the span of two seconds. It's mass is
  estimated to be around 0.1 kg. The toy can only handle two Newtons of force. Prove that the force
  it experiences is below this limit. -/

theorem toy_mouse_force_limit {f :ℝ }
(h1:v₀=2)
(h2:v₁=0)
(h3:m=0.1)
(h4:t=2)
(h5:a=(v₁ - v₀) / t)
(h6:f= m *a) :f < 2 := by
calc
f=m * a := by rw[h6]
_=m*((v₁ - v₀) / t ):= by rw [h5]
_= m*((0  - 2) / 2 ) := by rw[h2,h1,h4]
_=0.1*-1:=by rw[h3];ring
_=-0.1 :=by ring
_<2 :=by norm_num


/- A ball is dropped from a height of three meters with no initial velocity. Prove that it takes
  less than one second for it to hit the ground. -/
theorem less_3ms {h t v:ℝ }
(h1:h=3)
(h2:v₀=0)
(h3:a=9.8)
(h4:h=a*t): t<1:=
have time:t=h/a :=
calc
t=h/a := by rw[time]
_=3/9.8 := by rw[h1,h3];ring
_<1 :=by norm_num


/- Prove there does not exist a resistor with resistance x such that when placed in parallel with
  itself will obtain the same total resistance as when placed in series. -/

/- Note : This is an interesting problem because it showcases Lean's faithfulness to pure
-- mathematics. Technically, there does exist a real number that allows parallel resistance to equal
-- series; that number is zero. However, 1 / 0 in Lean just calculates to 0 which does not correlate
-- with the real world. Additionally, zero and negative resistance(as far as I know) don't exist.
  -/

/- Hooke's Law states that the force of a compressed / stretched spring is proportional to the
  distance from equilibrium. Prove that the force of the spring is the negative derivative of the
  energy with respect to the distance. -/
