# Exact checks for dimension 8

| file | content |
|---|---|
| `addition8_probe.py` | for $`d = 3, \dots, 8`$ and $`k \le 6`$: solves for the coefficients of the splitting identities used in `lean/Kissing8/Addition*.lean` and checks that they are unique and nonnegative (sympy, exact) |
| `delsarte8_probe.py` | the coefficients of $`f(t) = (t+1)(t+1/2)^2 t^2 (t-1/2)`$ in the scaled Gegenbauer polynomials of `lean/Kissing8/Delsarte.lean`, $`f(1)/f_0 = 240`$; the 240 points of Construction A and their minimum distance |
| `lp_probe.py` | the classical certificates for dimensions 8 and 24 in exact rationals ($`f(1)/f_0 = 240`$ and $`196560`$), and the floating-point linear programming bound by degree |
| `*.log` | their outputs |
