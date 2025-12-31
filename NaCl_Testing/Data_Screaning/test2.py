import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# -------- USER SETTINGS --------
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
# base_path = "Data\Copper_Data_06.11.2025"  
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

TAKE_IDX_FROM_END = 1000   # take y[-TAKE_IDX_FROM_END], or y[-1] if too short
poly_degrees = [1, 2]      # fits to show (1 = linear, 2 = quadratic)
# --------------------------------

def extract_numeric_index(fname):
    m = re.search(r'_(\d{2})\.csv$', fname)
    if m:
        return int(m.group(1))
    m2 = re.search(r'(\d+)', fname)
    return int(m2.group(1)) if m2 else None

x_list = []
y_list = []
labels = []

for fname in files:
    full = os.path.join(base_path, fname)
    if not os.path.exists(full):
        print("Missing:", full)
        continue
    df = pd.read_csv(full, encoding='latin1')
    if 'ADC_Value' not in df.columns:
        print("No ADC_Value in", fname)
        continue
    arr = df['ADC_Value'].astype(float).values
    if len(arr) < TAKE_IDX_FROM_END:
        val = float(arr[-1])
        print(f"{fname}: less than {TAKE_IDX_FROM_END} samples, using last value {val:.3f}")
    else:
        val = float(arr[-TAKE_IDX_FROM_END])
        print(f"{fname}: using value at -{TAKE_IDX_FROM_END} -> {val:.3f}")
    idx = extract_numeric_index(fname)
    x_list.append(idx if idx is not None else len(x_list))
    y_list.append(val)
    labels.append(os.path.splitext(os.path.basename(fname))[0])

# require at least 2 points
if len(x_list) < 2:
    raise SystemExit("Not enough points to fit a curve.")

# convert and sort by x
x = np.array(x_list, dtype=float)
y = np.array(y_list, dtype=float)
order = np.argsort(x)
x = x[order]
y = y[order]
labels = [labels[i] for i in order]

# make smooth x for plotting fits
x_smooth = np.linspace(x.min(), x.max(), 400)

plt.figure(figsize=(9,6))
plt.scatter(x, y, s=80, zorder=5, label="Measured (single-point)")
plt.xlabel("Sample index (parsed from filename)")
plt.ylabel(f"ADC (value at -{TAKE_IDX_FROM_END})")
plt.title("Measured points + best-fit curves")
plt.grid(True, linestyle='--', alpha=0.4)

# Fit polynomials and plot
for deg in poly_degrees:
    coeffs = np.polyfit(x, y, deg=deg)           # highest -> lowest
    p = np.poly1d(coeffs)
    y_fit_smooth = p(x_smooth)
    y_fit_on_x = p(x)
    # R^2
    ss_res = np.sum((y - y_fit_on_x)**2)
    ss_tot = np.sum((y - np.mean(y))**2)
    r2 = 1 - ss_res/ss_tot if ss_tot != 0 else float('nan')

    # plotting
    label = f"{deg}-deg fit (R²={r2:.4f})"
    plt.plot(x_smooth, y_fit_smooth, linewidth=2, label=label)

    # show equation text (compact)
    coeffs_str = ", ".join([f"{c:.4g}" for c in coeffs])
    plt.text(0.02, 0.95 - 0.06*(deg-1), f"deg{deg} coeffs: [{coeffs_str}]", transform=plt.gca().transAxes,
             fontsize=9, va='top')

# annotate each point with short filename
for xi, yi, lab in zip(x, y, labels):
    plt.text(xi, yi, "  " + lab, va='center', fontsize=8)

plt.legend()
plt.tight_layout()
plt.show()

# Print numeric summary
print("\nPoints used (x, y):")
for xi, yi, lab in zip(x, y, labels):
    print(f"  {lab}: x={xi}, y={yi:.4f}")
print("\nFits summary:")
for deg in poly_degrees:
    coeffs = np.polyfit(x, y, deg=deg)
    p = np.poly1d(coeffs)
    y_pred = p(x)
    ss_res = np.sum((y - y_pred)**2)
    ss_tot = np.sum((y - np.mean(y))**2)
    r2 = 1 - ss_res/ss_tot if ss_tot != 0 else float('nan')
    print(f" Degree {deg}: coeffs (high->low) = {coeffs}, R² = {r2:.6f}")
