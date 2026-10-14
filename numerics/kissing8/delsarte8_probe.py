"""f(t) = (t+1)(t+1/2)^2 t^2 (t-1/2) = sum_k alpha_k Z^8_k(t,1,1) (k!-scaled solid Gegenbauer C^3); check alpha_k >= 0,
f(1)/alpha_0 = 240. And the 240 points of sqrt2*E8 by Construction A from the extended Hamming code [8,4,4]."""
import sympy as sp, itertools
from addition8_probe import Z
t = sp.symbols("t")
f = sp.expand((t + 1) * (t + sp.Rational(1, 2))**2 * t**2 * (t - sp.Rational(1, 2)))
al = sp.symbols("al0:7")
sol = sp.solve(sp.Poly(f - sum(al[k] * Z(8, k, t, 1, 1) for k in range(7)), t).coeffs(), al, dict=True)[0]
A = [sol[x] for x in al]
print("alpha =", A, "nonneg:", all(x >= 0 for x in A), " f(1) =", f.subs(t, 1), " f(1)/alpha0 =", f.subs(t, 1) / A[0])
# Construction A: x in Z^8, x mod 2 in H8 (extended Hamming), norm^2 = 4
G = [[1,1,1,1,0,0,0,0],[0,0,1,1,1,1,0,0],[0,0,0,0,1,1,1,1],[1,0,1,0,1,0,1,0]]
H = {tuple(sum(c * g[i] for c, g in zip(cs, G)) % 2 for i in range(8)) for cs in itertools.product([0,1], repeat=4)}
assert len(H) == 16 and sorted(sum(h) for h in H) == [0] + [4]*14 + [8]
pts = [v for v in itertools.product(range(-2, 3), repeat=8) if sum(x*x for x in v) == 4 and tuple(x % 2 for x in v) in H]
print("points:", len(pts), " min dist^2:", min(sum((x-y)**2 for x, y in zip(u, v)) for u, v in itertools.combinations(pts, 2)))
