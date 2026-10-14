#!/usr/bin/env python3
"""Figures from the repository data only (light and dark SVG variants):

  angles      lean/Kissing8/TwoForty.lean           the 28680 angles between the 240 centres of the lower bound
  polynomial  lean/Kissing8/Delsarte.lean            the polynomial of the two-point bound and its Gegenbauer coefficients
  degree      numerics/kissing8/lp_probe.log         floating-point two-point bound by degree

Usage: python3 figures/make_figures.py   (matplotlib 3.9.4, numpy)"""
import math, os, re
from collections import Counter
from fractions import Fraction as Fr
import numpy as np
import matplotlib
matplotlib.use("svg")
matplotlib.rcParams["svg.hashsalt"] = "kissing-number-8"   # deterministic SVG ids
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def theme(dark):
    if dark:
        return dict(fg="#e6e6e6", bg="#0d1117", c1="#79c0ff", c2="#ffa657", c3="#7ee787", grid="#30363d")
    return dict(fg="#1f2328", bg="#ffffff", c1="#0969da", c2="#bc4c00", c3="#1a7f37", grid="#d0d7de")


def style(fig, ax, th):
    fig.patch.set_facecolor(th["bg"]); ax.set_facecolor(th["bg"])
    ax.tick_params(colors=th["fg"])
    for s in ax.spines.values():
        s.set_color(th["fg"])
    ax.xaxis.label.set_color(th["fg"]); ax.yaxis.label.set_color(th["fg"]); ax.title.set_color(th["fg"])


def save(fig, name, dark, th):
    fig.savefig(os.path.join(HERE, f"{name}_{'dark' if dark else 'light'}.svg"), facecolor=th["bg"],
                metadata={"Date": None})
    plt.close(fig)


src = open(os.path.join(ROOT, "lean", "Kissing8", "TwoForty.lean"), encoding="utf-8").read()
PTS = np.array([[int(v) for v in m] for m in re.findall(r"!\[(-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), "
                                                        r"(-?\d+), (-?\d+)\]", src.split("def rows0")[1])], float)
assert PTS.shape == (240, 8) and np.allclose((PTS ** 2).sum(1), 4)

dl = open(os.path.join(ROOT, "lean", "Kissing8", "Delsarte.lean"), encoding="utf-8").read()
ALPHA = [Fr(a) / Fr(b) for a, b in re.findall(r"\| \d+ => (\d+) / (\d+)", dl.split("def alpha")[1].split("theorem")[0])]
assert len(ALPHA) == 7 and ALPHA[0] == Fr(3, 320)


def fL(t):
    return (t + 1) * (t + 0.5) ** 2 * t ** 2 * (t - 0.5)


def fig_angles(dark):
    th = theme(dark)
    G = PTS @ PTS.T / 4
    iu = np.triu_indices(240, 1)
    cnt = Counter(np.round(np.degrees(np.arccos(np.clip(G[iu], -1, 1)))).astype(int))
    fig, ax = plt.subplots(figsize=(6.4, 3.4)); style(fig, ax, th)
    xs = sorted(cnt)
    ax.bar([f"{x}°" for x in xs], [cnt[x] for x in xs], color=th["c1"])
    for i, x in enumerate(xs):
        ax.text(i, cnt[x], str(cnt[x]), ha="center", va="bottom", color=th["fg"], fontsize=9)
    ax.set_xlabel("angle between two centres")
    ax.set_ylabel("number of pairs (of 28680)")
    ax.set_title("The 240 balls of the lower bound: every angle is at least 60° (lean/Kissing8/TwoForty.lean)",
                 fontsize=9)
    fig.tight_layout(); save(fig, "angles", dark, th)


def fig_polynomial(dark):
    th = theme(dark)
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(9.6, 3.8), gridspec_kw={"width_ratios": [3, 2]})
    style(fig, ax, th); style(fig, bx, th)
    t = np.linspace(-1, 1, 801)
    ax.axvspan(-1, 0.5, color=th["grid"], alpha=0.5, lw=0, label="$[-1, 1/2]$: inner products of distinct points")
    ax.axhline(0, color=th["fg"], lw=0.8)
    ax.plot(t, fL(t), color=th["c2"], lw=2, label="$f(t) = (t+1)(t+1/2)^2\\,t^2\\,(t-1/2)$")
    ax.plot([1], [fL(1)], "o", color=th["c2"])
    ax.annotate("$f(1) = 9/4$", (1, fL(1)), textcoords="offset points", xytext=(-60, -4), color=th["fg"], fontsize=9)
    ax.set_xlabel("$t$"); ax.set_ylim(-0.25, 2.5)
    leg = ax.legend(frameon=False, fontsize=8, loc="upper left")
    for x in leg.get_texts():
        x.set_color(th["fg"])
    ax.set_title("$f \\leq 0$ on $[-1, 1/2]$", fontsize=10)
    ins = ax.inset_axes([0.33, 0.38, 0.4, 0.3])
    style(fig, ins, th)
    u = np.linspace(-1, 0.5, 400)
    ins.axhline(0, color=th["fg"], lw=0.6)
    ins.plot(u, fL(u), color=th["c2"], lw=1.5)
    ins.set_xlim(-1, 0.5); ins.tick_params(labelsize=7)
    ins.set_title("on $[-1, 1/2]$, magnified", fontsize=7, color=th["fg"])
    # coefficients in the normalised Gegenbauer polynomials G_k (G_k(1) = 1): f_k = alpha_k * Zg 8 k 1 1 1
    z = [Fr(1), Fr(6)]
    for j in range(1, 6):
        z.append((2 * j + 6) * z[j] - j * (j + 5) * z[j - 1])
    f = [float(a * zz) for a, zz in zip(ALPHA, z)]
    bx.bar(range(7), f, color=th["c1"])
    bx.set_xticks(range(7)); bx.set_xlabel("$k$")
    bx.set_ylabel("coefficient of $G_k$ ($G_k(1) = 1$)")
    bx.set_title("$f = \\sum_k f_k G_k$, all $f_k > 0$;  $f(1)/f_0 = 240$", fontsize=10)
    fig.tight_layout(); save(fig, "polynomial", dark, th)


def fig_degree(dark):
    th = theme(dark)
    pts = [(int(d), float(b)) for d, b in re.findall(r"n = 8, degree (\d+): LP bound ([0-9.]+)",
                                                       open(os.path.join(ROOT, "numerics", "kissing8", "lp_probe.log")).read())]
    infeas = [int(d) for d in re.findall(r"n = 8, degree (\d+): LP bound The problem is infeasible",
                                          open(os.path.join(ROOT, "numerics", "kissing8", "lp_probe.log")).read())]
    fig, ax = plt.subplots(figsize=(6.0, 3.4)); style(fig, ax, th)
    ax.plot([d for d, _ in pts], [b for _, b in pts], "o-", color=th["c1"], label="two-point bound (floating point)")
    ax.plot(infeas, [340] * len(infeas), "x", color=th["fg"], ms=8, mew=2, ls="none", label="no feasible polynomial")
    ax.axhline(240, color=th["c3"], lw=1, ls=":")
    ax.text(2.1, 243, "240", color=th["c3"], fontsize=9)
    ax.set_xlabel("degree of the polynomial"); ax.set_ylabel("upper bound for the kissing number")
    ax.set_ylim(230, 350); ax.set_xticks(range(2, 9))
    leg = ax.legend(frameon=False, fontsize=8, loc="upper right")
    for x in leg.get_texts():
        x.set_color(th["fg"])
    ax.set_title("Two-point bound in dimension 8 by degree (numerics/kissing8/lp_probe.log)", fontsize=9)
    fig.tight_layout(); save(fig, "degree", dark, th)


for dark in (False, True):
    fig_angles(dark)
    fig_polynomial(dark)
    fig_degree(dark)
