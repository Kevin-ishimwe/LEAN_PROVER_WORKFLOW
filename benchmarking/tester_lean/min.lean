import Mathlib

theorem square_expansion {a b:ℕ }:(a + b) ^2 = a ^ 2 + 2 * a * b + b ^ 2:= by ring

def pi : Float := 3.14
def area_circle (r :Float ):= pi*r^2
