import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# -------- USER SETTINGS --------
#----------------------------------------------------------------------- Graphite data
# base_path = "Data/Graphite_Data_06.11.2025"  # adjust if needed
# files = [
#     "G_Data01_00.csv",
#     "G_Data02_01.csv",
#     "G_Data03_02.csv",
#     "G_Data05_04.csv",
#     "G_Data06_05.csv",
#     "G_Data07_06.csv",
#     "G_Data10_09.csv",
#     "G_Data12_11.csv"
# ]

#----------------------------------------------------------------------- Copper data
base_path = "Data\Copper_Data_06.11.2025"  
files = [
    "C_Data01_00.csv",
    "C_Data03_02.csv",
    "C_Data04_03.csv",
    "C_Data05_04.csv",
    "C_Data06_05.csv",
    "C_Data08_07.csv",
    "C_Data09_08.csv",
    "C_Data10_09.csv",
]


MA_WINDOW = 1000   # moving-average window (odd recommended). Use 1 for no smoothing.
ENCODING = 'latin1'
METRIC = 'mean'    # 'mean' | 'median' | 'max' | 'min' | 'range' - used for x vs y y-value

# ---------------------------------------------------

def moving_average(arr, window):
    if window <= 1:
        return arr.copy()
    kernel = np.ones(window) / window
    # 'same' keeps same length and gives a centered MA
    return np.convolve(arr, kernel, mode='same')

def extract_label_and_index(fname):
    # try pattern ..._NN.csv (NN two digits)
    m = re.search(r'_(\d{2})\.csv$', fname)
    if m:
        return f"G{int(m.group(1))}", int(m.group(1))
    # fallback: try any number in filename
    m2 = re.search(r'(\d+)', fname)
    if m2:
        return os.path.splitext(os.path.basename(fname))[0], int(m2.group(1))
    return os.path.splitext(os.path.basename(fname))[0], None

# containers
labels = []
indices = []
mins = []
maxs = []
summary = []

# Process files
for fname in files:
    path = os.path.join(base_path, fname)
    if not os.path.exists(path):
        print(f"Skipping missing file: {path}")
        continue

    try:
        df = pd.read_csv(path, encoding=ENCODING)
    except Exception as e:
        print(f"Error reading {path}: {e}")
        continue

    if 'ADC_Value' not in df.columns:
        print(f"Skipping {fname}: no 'ADC_Value' column. Columns: {df.columns.tolist()}")
        continue

    # Convert to float, drop NaNs
    y_raw = pd.to_numeric(df['ADC_Value'], errors='coerce').dropna().values
    if y_raw.size == 0:
        print(f"Skipping {fname}: 'ADC_Value' column empty after coercion.")
        continue

    y_smooth = moving_average(y_raw, MA_WINDOW)

    label, idx = extract_label_and_index(fname)
    lab = label if label is not None else os.path.splitext(fname)[0]

    cur_min = float(np.min(y_smooth))
    cur_max = float(np.max(y_smooth))
    cur_mean = float(np.mean(y_smooth))
    cur_std = float(np.std(y_smooth))
    cur_median = float(np.median(y_smooth))
    cur_range = cur_max - cur_min

    labels.append(lab)
    indices.append(idx)
    mins.append(cur_min)
    maxs.append(cur_max)

    summary.append({
        'filename': fname,
        'label': lab,
        'parsed_index': idx,
        'min_smoothed': cur_min,
        'max_smoothed': cur_max,
        'mean_smoothed': cur_mean,
        'std_smoothed': cur_std,
        'median_smoothed': cur_median,
        'range_smoothed': cur_range,
        'n_samples': len(y_smooth)
    })

    print(f"{fname} -> {lab} (idx={idx}) : min={cur_min:.3f}, max={cur_max:.3f}, mean={cur_mean:.3f}, samples={len(y_smooth)}")

if len(summary) == 0:
    raise SystemExit("No valid files processed. Check base_path and filenames.")

# Put into DataFrame and sort by parsed index when available
summary_df = pd.DataFrame(summary)
if summary_df['parsed_index'].notnull().any():
    summary_df.sort_values(by='parsed_index', inplace=True, na_position='last')
else:
    summary_df.sort_values(by='label', inplace=True)

labels_sorted = summary_df['label'].tolist()
mins_sorted = summary_df['min_smoothed'].tolist()
maxs_sorted = summary_df['max_smoothed'].tolist()

# ---------- Plot grouped bar chart ----------
x = np.arange(len(labels_sorted))
width = 0.35

plt.figure(figsize=(11,6))
plt.bar(x - width/2, mins_sorted, width, label='Min (smoothed)')
plt.bar(x + width/2, maxs_sorted, width, label='Max (smoothed)')

plt.xticks(x, labels_sorted, rotation=45)
plt.xlabel("Sample")
plt.ylabel("ADC (smoothed)")
plt.title(f"Min & Max of Smoothed ADC per Sample (MA window={MA_WINDOW})")
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

# Print summary table
print("\nSummary table (sorted):")
print(summary_df[['filename','label','parsed_index','min_smoothed','max_smoothed','mean_smoothed','std_smoothed','n_samples']].to_string(index=False))

# ---------- X vs Y plot for all concentrations ----------
# Choose the y-metric based on METRIC variable
if METRIC == 'mean':
    y_vals = summary_df['mean_smoothed'].astype(float).values
elif METRIC == 'median':
    y_vals = summary_df['median_smoothed'].astype(float).values
elif METRIC == 'max':
    y_vals = summary_df['max_smoothed'].astype(float).values
elif METRIC == 'min':
    y_vals = summary_df['min_smoothed'].astype(float).values
elif METRIC == 'range':
    y_vals = summary_df['range_smoothed'].astype(float).values
else:
    raise ValueError("Unsupported METRIC. Choose from 'mean','median','max','min','range'.")

# Use std for errorbars where applicable
y_err = summary_df['std_smoothed'].astype(float).values if 'std_smoothed' in summary_df.columns else None

# Prepare x-values: prefer parsed_index if present for at least one row; else use ordinal indices
if summary_df['parsed_index'].notnull().any():
    # If some parsed_index are NaN, fallback to ordinal positions for those entries:
    parsed = summary_df['parsed_index']
    x_vals = parsed.copy()
    # fill NaN with position index (this keeps unique x values)
    x_vals = x_vals.fillna(pd.Series(np.arange(len(parsed)), index=parsed.index))
    x_vals = x_vals.astype(float).values
    x_label = "Parsed index (concentration)"
else:
    x_vals = np.arange(len(summary_df)).astype(float)
    x_label = "Sample (ordinal)"

plt.figure(figsize=(9,6))
# scatter + errorbars (stddev) if available
if y_err is not None:
    plt.errorbar(x_vals, y_vals, yerr=y_err, fmt='o', capsize=4, label=f'{METRIC.capitalize()} ± 1σ (smoothed)')
else:
    plt.plot(x_vals, y_vals, 'o-', label=f'{METRIC.capitalize()} (smoothed)')

# show min/max as faint vertical lines (for context)
mins = summary_df['min_smoothed'].astype(float).values
maxs = summary_df['max_smoothed'].astype(float).values
for xv, mn, mx in zip(x_vals, mins, maxs):
    plt.vlines(xv, mn, mx, linestyles='dashed', alpha=0.35)

# annotate each point with label
for xv, yv, lab in zip(x_vals, y_vals, summary_df['label'].tolist()):
    plt.annotate(lab, (xv, yv), textcoords="offset points", xytext=(4,4), ha='left', fontsize=8)

plt.xlabel(x_label)
plt.ylabel(f"{METRIC.capitalize()} ADC (smoothed)")
plt.title(f"Concentration (x) vs {METRIC.capitalize()} ADC (y)  — MA window = {MA_WINDOW}")
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.show()
