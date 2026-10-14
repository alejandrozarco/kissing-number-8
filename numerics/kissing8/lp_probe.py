"""Probe: Delsarte LP certificates for kappa(8) = 240 and kappa(24) = 196560 (Levenshtein; Odlyzko-Sloane 1979),
in exact rational arithmetic. f(t) <= 0 on [-1, 1/2], f = sum_k f_k G_k (Gegenbauer of S^{n-1}, G_k(1) = 1) with
f_0 > 0 and f_k >= 0 give N <= f(1)/f_0. Also: float LP optimum by degree, to see the degree needed."""
from fractions import Fraction as Fr
import numpy as np, sys

def polymul(a, b):
    r = [Fr(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            r[i + j] += x * y
    return r

def geg(n, K):
    """Gegenbauer polynomials for S^{n-1}, normalised G_k(1) = 1, as coefficient lists (exact)."""
    lam = Fr(n - 2, 2)
    C = [[Fr(1)], [Fr(0), 2 * lam]]                      # C_k^lam
    for k in range(1, K):
        a = [Fr(0)] + [2 * (k + lam) * c for c in C[k]]
        b = [(k + 2 * lam - 1) * c for c in C[k - 1]] + [Fr(0)] * 2
        C.append([(x - y) / (k + 1) for x, y in zip(a + [Fr(0)] * (len(b) - len(a)), b)])
    return [[c / sum(Ck) for c in Ck] for Ck in C[:K + 1]]

def expand_in(G, f):
    """coefficients f_k with f = sum f_k G_k (triangular solve)."""
    f = list(f); K = len(f) - 1; out = [Fr(0)] * (K + 1)
    for k in range(K, -1, -1):
        c = f[k] / G[k][k] if k < len(f) else Fr(0)
        out[k] = c
        for i, g in enumerate(G[k]):
            f[i] -= c * g
    assert all(x == 0 for x in f)
    return out

def cert(n, roots):
    f = [Fr(1)]
    for r, m in roots:
        for _ in range(m):
            f = polymul(f, [-r, Fr(1)])
    K = len(f) - 1
    fk = expand_in(geg(n, K), f)
    f1 = sum(f)
    print(f"n = {n}: deg f = {K}; f_k >= 0: {all(x >= 0 for x in fk)}; zero coefficients at k = "
          f"{[k for k, x in enumerate(fk) if x == 0]}; bound f(1)/f_0 = {f1 / fk[0]}")
    print("   f_k =", [str(x) for x in fk])
    print("   max denominator of f_k:", max(x.denominator for x in fk))

h = Fr(1, 2); q = Fr(1, 4)
cert(8, [(-1, 1), (-h, 2), (0, 2), (h, 1)])
cert(24, [(-1, 1), (-h, 2), (-q, 2), (0, 2), (q, 2), (h, 1)])

# float LP by degree (sampled constraint f <= 0 on [-1, 1/2])
from scipy.optimize import linprog
for n, Ds in [(8, range(2, 9)), (24, range(4, 14))]:
    for D in Ds:
        G = [np.array([float(c) for c in g]) for g in geg(n, D)]
        ts = np.linspace(-1, 0.5, 4001)
        V = np.array([[np.polyval(g[::-1], t) for g in G] for t in ts])        # G_k(t)
        # variables f_1..f_D >= 0, f_0 = 1: minimise f(1) = 1 + sum f_k  s.t. 1 + sum f_k G_k(t) <= 0
        res = linprog(np.ones(D), A_ub=V[:, 1:], b_ub=-np.ones(len(ts)), bounds=[(0, None)] * D, method="highs")
        print(f"n = {n}, degree {D}: LP bound {1 + res.fun if res.status == 0 else res.message}")
