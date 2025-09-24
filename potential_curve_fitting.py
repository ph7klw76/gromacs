# This script loads dihedral scan data, fits a weighted Fourier series selected by BIC,
# prints GROMACS-ready tables  saves them to a file,
# and PLOTS the raw data and fitted curve.
#
# Notes:
# - Input file expected: "dihedral-angle.txt" with two columns: angle_deg energy_eV (space-separated)
# - Energies are converted from eV to kJ/mol using 96.4853321233
# - Output file: gromacs_dihedrals_table.txt
#
# The plotting obeys the constraints:
#   * uses matplotlib (no seaborn)
#   * one chart only (no subplots)
#   * no explicit colors/styles are set

import os
import numpy as np
import matplotlib.pyplot as plt
from math import atan2, sqrt, pi, degrees

# ---------- Utilities ----------
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

# ---------- Load data ----------
candidate_paths = [
    "dihedral-angle.txt" ]

filepath = None
for p in candidate_paths:
    if os.path.exists(p):
        filepath = p
        break

if filepath is None:
    print("❌ Could not find 'dihedral-angle.txt'. Please upload it to this chat or place it at dihedral-angle.txt.")
else:
    angles_deg = []
    energies_raw = []
    with open(filepath, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            try:
                angles_deg.append(float(parts[0]))
                energies_raw.append(float(parts[1]))
            except ValueError:
                # Skip header or malformed lines gracefully
                continue

    angles_deg = np.asarray(angles_deg, float)
    phi = np.deg2rad(angles_deg)
    # Convert eV -> kJ/mol
    E = np.asarray(energies_raw, float) * 96.4853321233

    # Build weights (heuristic: 1/(0.01*E + 0.1)^2 with floor to avoid zero-weight)
    sigma = np.abs(E) * 0.01 + 0.1
    w = 1.0 / (sigma**2)
    Wsqrt = np.sqrt(w)

    # ---------- Fit Fourier 0..6 by BIC ----------
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
    r2 = float(best['r2'])
    m = int(best_m)

    # ---------- Collect coefficients a0, {a_n, b_n} and amplitude/phase ----------
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
        d = atan2(b[n], a[n])  # phase in radians
        k[n] = A
        delta_rad[n] = d
        delta_deg[n] = degrees(d)

    # ---------- Build GROMACS tables ----------
    lines = ["[ dihedrals ]",
             ";  i    j    k    l    funct    phi0(deg)         k(kJ/mol)    mult"]
    for n in range(1, m+1):
        phi0 = delta_deg[n]
        kk = k[n]
        lines.append(f"I    J    K    L      1      {phi0:10.6f}    {kk:14.8f}    {n}")
    table_text = "\n".join(lines)

    types_lines = ["[ dihedraltypes ]",
                   ";  i    j    k    l    funct    phi0(deg)         k(kJ/mol)    mult"]
    for n in range(1, m+1):
        types_lines.append(f"X    X    X    X      1      {delta_deg[n]:10.6f}    {k[n]:14.8f}    {n}")
    types_text = "\n".join(types_lines)

    out_path = "gromacs_dihedrals_table.txt"
    with open(out_path, "w") as f:
        f.write(table_text + "\n\n" + types_text + "\n")

    # ---------- Prepare plot (raw points + fitted curve) ----------
    # Smooth curve over 0..360 deg (or min..max if data narrower)
    lo = float(np.min(angles_deg)) if angles_deg.size else 0.0
    hi = float(np.max(angles_deg)) if angles_deg.size else 360.0
    if hi - lo < 359.0:  # ensure full period coverage for clarity
        lo, hi = -175, 150

    grid_deg = np.linspace(lo, hi, 721)
    grid_phi = np.deg2rad(grid_deg)
    Xgrid = fourier_design(grid_phi, m)
    Ehat_grid = Xgrid @ beta

    # Single figure, no explicit styles/colors
    plt.figure(figsize=(8,5))
    # Scatter raw data
    plt.scatter(angles_deg, E, s=18, label="Data (kJ/mol)")
    # Fitted curve
    plt.plot(grid_deg, Ehat_grid, label=f"Fourier(m={m}) fit • R²={r2:.4f}")
    plt.xlabel("Dihedral angle φ (deg)")
    plt.ylabel("Energy (kJ/mol)")
    plt.title("Dihedral Scan: Data & Weighted Fourier Fit")
    plt.legend()
    plt.tight_layout()
    plt.show()

    # ---------- Print summary to the notebook output ----------
    print(f"\nChosen model: Fourier(m={m})")
    print(f"R^2 = {r2}")
    print("\nRaw cosine/sine coefficients:")
    print(f"  a0 = {a0}")
    for n in range(1, m+1):
        print(f"  a_{n} = {a[n]}")
        print(f"  b_{n} = {b[n]}")

    print("\nAmplitude/phase form (for GROMACS funct=1):")
    for n in range(1, m+1):
        print(f"  n={n:>1d} : k_n = {k[n]}   delta_n = {delta_deg[n]} deg")

    print("\n[ dihedrals ] (paste into your topology; replace I J K L):\n")
    print(table_text)
    print("\n[ dihedraltypes ] (generic types version):\n")
    print(types_text)

    print(f"\n✅ Saved tables to: {out_path}\n")



