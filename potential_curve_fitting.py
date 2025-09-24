# Recompute and print all coefficients, then build a ready-to-paste GROMACS [ dihedrals ] table (function type 1).
import numpy as np
from math import atan2, sqrt, pi, degrees

# Reload and fit quickly (reuse simpler code from earlier cell assumptions)
# (We depend on variables from earlier execution; if missing, re-derive.)

# Load data
filepath = 'dihedral-angle.txt'
angles_deg = []
energies_raw = []
with open(filepath, 'r') as f:
    for line in f:
        if not line.strip():
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        angles_deg.append(float(parts[0]))
        energies_raw.append(float(parts[1]))

phi = np.deg2rad(np.asarray(angles_deg, float))
E = np.asarray(energies_raw, float) * 4.18

sigma = E * 0.01 + 0.1
w = 1.0 / (sigma**2)
Wsqrt = np.sqrt(w)

def r2_score(y, yhat):
    ss_res = np.sum((y - yhat)**2)
    ss_tot = np.sum((y - np.mean(y))**2)
    return 1.0 - ss_res/ss_tot if ss_tot > 0 else 0.0

def bic_score(y, yhat, k):
    n = y.size
    rss = np.sum((y - yhat)**2)
    return n * np.log(rss / n) + k * np.log(n)

def fourier_design(phi, m):
    cols = [np.ones_like(phi)]
    for n in range(1, m+1):
        cols.append(np.cos(n*phi))
        cols.append(np.sin(n*phi))
    return np.column_stack(cols)

# Fit Fourier 0..6 by BIC
best = None
best_m = 0
for m in range(0, 7):
    X = fourier_design(phi, m)
    Xw = Wsqrt[:, None] * X
    yw = Wsqrt * E
    beta, *_ = np.linalg.lstsq(Xw, yw, rcond=None)
    Ehat = X @ beta
    r2 = r2_score(E, Ehat)
    bic = bic_score(E, Ehat, k=len(beta))
    if best is None or bic < best['bic']:
        best = {'beta': beta, 'r2': r2, 'bic': bic}
        best_m = m

beta = best['beta']
r2 = best['r2']
m = best_m

# Collect coefficients a0, {a_n, b_n}
a0 = beta[0]
a = {}
b = {}
k = {}
delta_rad = {}
delta_deg = {}
for n in range(1, m+1):
    a[n] = beta[2*n-1]
    b[n] = beta[2*n]
    A = sqrt(a[n]**2 + b[n]**2)
    d = atan2(b[n], a[n])
    k[n] = A
    delta_rad[n] = d
    delta_deg[n] = degrees(d)

# Display all coefficients
print("Chosen model: Fourier(m=%d)" % m)
print("R^2 =", r2)
print("Raw cosine/sine coefficients:")
print("  a0 =", a0)
for n in range(1, m+1):
    print(f"  a_{n} = {a[n]}")
    print(f"  b_{n} = {b[n]}")

print("\nAmplitude/phase form (for GROMACS funct=1):")
for n in range(1, m+1):
    print(f"  n={n:>1d} : k_n = {k[n]}   delta_n = {delta_deg[n]} deg")

# Build ready-to-paste [ dihedrals ] lines (function type 1).
# GROMACS form: i  j  k  l  funct  phi0(deg)  k (kJ/mol)  multiplicity
# Multiple lines per multiplicity n=1..m.
# We'll leave atom indices as placeholders: I J K L
lines = ["[ dihedrals ]",
         ";  i    j    k    l    funct    phi0(deg)         k(kJ/mol)    mult"]
for n in range(1, m+1):
    phi0 = delta_deg[n]
    kk = k[n]
    lines.append(f"I    J    K    L      1      {phi0:10.6f}    {kk:14.8f}    {n}")

table_text = "\n".join(lines)

# Also provide an optional [ dihedraltypes ] version
types_lines = ["[ dihedraltypes ]",
               ";  i    j    k    l    funct    phi0(deg)         k(kJ/mol)    mult"]
for n in range(1, m+1):
    types_lines.append(f"X    X    X    X      1      {delta_deg[n]:10.6f}    {k[n]:14.8f}    {n}")
types_text = "\n".join(types_lines)

# Save both snippets
with open("gromacs_dihedrals_table.txt", "w") as f:
    f.write(table_text + "\n\n" + types_text + "\n")

