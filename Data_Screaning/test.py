import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- USER SETTINGS ----------------
#----------------------------------------------------------------------- Graphite data
base_path = "Data/Graphite_Data_06.11.2025"  # adjust if needed
files = [
    "G_Data01_00.csv",
    "G_Data02_01.csv",
    "G_Data03_02.csv",
    "G_Data05_04.csv",
    "G_Data06_05.csv",
    "G_Data07_06.csv",
    "G_Data10_09.csv",
    "G_Data12_11.csv"
]

#----------------------------------------------------------------------- Copper data
# base_path = "Data\Copper_Data_06.11.2025"  # adjust if needed
# files = [
#     "C_Data01_00.csv",
#     "C_Data03_02.csv",
#     "C_Data04_03.csv",
#     "C_Data05_04.csv",
#     "C_Data06_05.csv",
#     "C_Data08_07.csv",
#     "C_Data09_08.csv",
#     "C_Data10_09.csv",
# ]


LAST_N = 1000                # use last N samples to compute the representative ADC per file
polyfit_degrees = [1, 2]     # degrees to try: 1=linear, 2=quadratic
# ------------------------------------------------

def extract_index(fname):
    """Extract numeric index from filename pattern ..._NN.csv"""
    m = re.search(r'_(\d{2})\.csv$', fname)
    if m:
        return int(m.group(1))
    # fallback: try to find any number group
    m2 = re.search(r'(\d+)', fname)
    return int(m2.group(1)) if m2 else None

x_vals = []
y_means = []
used_files = []

for fname in files:
    full = os.path.join(base_path, fname)
    if not os.path.exists(full):
        print(f"Skipping missing file: {full}")
        continue

    df = pd.read_csv(full, encoding='latin1')
    if 'ADC_Value' not in df.columns:
        print(f"Skipping {fname}: 'ADC_Value' column not found")
        continue

    y = df['ADC_Value'].astype(float).values
    n_take = min(LAST_N, len(y))
    last_seg = y[-n_take:]
    mean_val = float(np.mean(last_seg))

    idx = extract_index(fname)
    if idx is None:
        # if index extraction fails, use sequential order (append at end)
        idx = len(x_vals)

    x_vals.append(idx)
    y_means.append(mean_val)
    used_files.append(fname)
    print(f"Loaded {fname}: index={idx}, mean_last{n_take}={mean_val:.3f}")

if len(x_vals) < 2:
    raise SystemExit("Not enough data points to fit. Check files and LAST_N.")

# convert to numpy arrays and sort by x (important if filenames are out of order)
x = np.array(x_vals, dtype=float)
y = np.array(y_means, dtype=float)
order = np.argsort(x)
x = x[order]
y = y[order]
used_files = [used_files[i] for i in order]

# Plot scatter
plt.figure(figsize=(9,6))
plt.scatter(x, y, s=70, label='Measured (mean of last N)', zorder=5)
plt.xlabel("Sample index (parsed from filename)")
plt.ylabel(f"Mean ADC (last {LAST_N} samples)")
plt.title("Calibration points and best-fit curves")
plt.grid(True, linestyle='--', alpha=0.4)

# Fit and plot polynomials, compute R^2 and show equation
x_for_plot = np.linspace(x.min(), x.max(), 200)

for deg in polyfit_degrees:
    coeffs = np.polyfit(x, y, deg=deg)
    p = np.poly1d(coeffs)
    y_fit = p(x_for_plot)

    # compute R^2 on the original points
    y_pred = p(x)
    ss_res = np.sum((y - y_pred)**2)
    ss_tot = np.sum((y - np.mean(y))**2)
    r2 = 1 - ss_res/ss_tot if ss_tot != 0 else float('nan')

    # format equation
    if deg == 1:
        m, b = coeffs
        eq = f"y = {m:.3f}x + {b:.3f}"
    else:
        # show highest->lowest terms
        terms = []
        for i, c in enumerate(coeffs):
            power = deg - i
            terms.append(f"{c:.3e}x^{power}" if power>0 else f"{c:.3e}")
        eq = " + ".join(terms)

    plt.plot(x_for_plot, y_fit, label=f"{deg} deg fit (R²={r2:.4f})\n{eq}", linewidth=2)

# Annotate each data point with filename short label (optional)
for xi, yi, fn in zip(x, y, used_files):
    lbl = os.path.splitext(os.path.basename(fn))[0]
    plt.text(xi, yi, "  " + lbl, va='center', fontsize=8, alpha=0.9)

plt.legend(loc='best', fontsize=9)
plt.tight_layout()
plt.show()

# Print fit coefficients and R^2 values to console as well
print("\nFitting summary:")
for deg in polyfit_degrees:
    coeffs = np.polyfit(x, y, deg=deg)
    p = np.poly1d(coeffs)
    y_pred = p(x)
    ss_res = np.sum((y - y_pred)**2)
    ss_tot = np.sum((y - np.mean(y))**2)
    r2 = 1 - ss_res/ss_tot if ss_tot != 0 else float('nan')
    print(f"Degree {deg}: coeffs (highest->lowest) = {coeffs}, R² = {r2:.6f}")
