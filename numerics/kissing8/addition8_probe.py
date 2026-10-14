"""Find nonnegative c_{d,k,m} with the solid Gegenbauer addition identity
   Z^d_k(a a' + w, a^2 + P, a'^2 + Q) = sum_m c * B(a, a^2+P) * B(a', a'^2+Q) * Z^{d-1}_m(w, P, Q),
   B = Z^{d+2m}_{k-m}(a, r2, 1), for d = 3..8, k <= 6. Z^d (d >= 3): k!-scaled Gegenbauer C^{(d-2)/2}, solid form;
   Z^2: Chebyshev T, solid form."""
import sympy as sp
s, p, q, a, a2, w, P, Q = sp.symbols("s p q a a2 w P Q")

def Z(d, k, s, p, q):
    if d == 2:
        z = [sp.Integer(1), s]
        for j in range(1, k):
            z.append(sp.expand(2 * s * z[j] - p * q * z[j - 1]))
        return z[k]
    z = [sp.Integer(1), (d - 2) * s]
    for j in range(1, k):                       # C~_{j+1} = (2j+d-2) s C~_j - j (j+d-3) pq C~_{j-1}
        z.append(sp.expand((2 * j + d - 2) * s * z[j] - j * (j + d - 3) * p * q * z[j - 1]))
    return z[k]

if __name__ == "__main__":
    ok = True
    for d in range(3, 9):
        for k in range(0, 7):
            lhs = sp.expand(Z(d, k, a * a2 + w, a**2 + P, a2**2 + Q))
            cs = sp.symbols(f"c0:{k+1}")
            rhs = sum(cs[m] * Z(d + 2 * m, k - m, a, a**2 + P, 1) * Z(d + 2 * m, k - m, a2, a2**2 + Q, 1)
                      * Z(d - 1, m, w, P, Q) for m in range(k + 1))
            eqs = sp.Poly(sp.expand(lhs - rhs), a, a2, w, P, Q).coeffs()
            sol = sp.solve(eqs, cs, dict=True)
            if not sol:
                print(d, k, "NO SOLUTION"); ok = False; continue
            c = [sol[0].get(x, None) for x in cs]
            nonneg = all(x is not None and x >= 0 for x in c)
            ok &= nonneg
            print(d, k, c, "nonneg" if nonneg else "NEGATIVE/FREE")
    print("ALL OK" if ok else "PROBLEM")
