import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ===================================================================================================== DATA FILES

# ----------------------------------------- Graphite data 
# TYP = 'Graphite'
# base_path = "NaCl_Testing\Data\Graphite_Data" 
# files = [
#     "G_Data01_00.csv",
#     "G_Data02_01.csv",
#     "G_Data03_02.csv",
#     "G_Data04_03.csv",
#     "G_Data05_04.csv",
#     "G_Data06_05.csv",
#     "G_Data07_06.csv",

#     "G_Data09_08.csv",
#     "G_Data10_09.csv",
#     "G_Data11_10.csv",
#     "G_Data12_11.csv",
#     "G_Data13_00.csv",
#     "G_Data14_01.csv",
#     "G_Data15_02.csv",
 
#     "G_Data17_04.csv",

#     "G_Data19_06.csv",
#     "G_Data20_07.csv",
#     "G_Data21_08.csv",
#     "G_Data22_09.csv",


# ]

# # ----------------------------------------- Copper data 
# TYP = 'Copper'
# base_path = "NaCl_Testing\Data\Copper_Data"  
# files = [
#     "C_Data01_00.csv",

#     "C_Data03_02.csv",
#     "C_Data04_03.csv",
#     "C_Data05_04.csv",
#     "C_Data06_05.csv",
#     "C_Data07_06.csv",
#     "C_Data08_07.csv",
#     "C_Data09_08.csv",
#     "C_Data10_09.csv",

#     "C_Data12_11.csv",
#     "C_Data13_00.csv",
#     "C_Data14_01.csv",
#     "C_Data15_02.csv",
#     "C_Data16_03.csv",
#     "C_Data17_04.csv",


#     "C_Data20_07.csv",
#     "C_Data21_08.csv",
#     "C_Data22_09.csv",
#     "C_Data23_10.csv",
#     "C_Data24_11.csv"
# ]

# ----------------------------------------- Graphite INK data 
# TYP = 'Graphite INK'
# base_path = "NaCl_Testing\Data\Graphite_INK_Data" 
# files = [
#     "GI_Data01_00.csv",
#     "GI_Data02_01.csv",
#     "GI_Data03_02.csv",
#     "GI_Data04_03.csv",
   

#     "GI_Data07_06.csv",
#     "GI_Data08_07.csv",
#     "GI_Data09_08.csv",
#     "GI_Data10_09.csv",
#     "GI_Data11_10.csv",
#     "GI_Data12_11.csv"
# ]

# ----------------------------------------- Solid Graphite data 
TYP = 'Solid Graphite'
base_path = "NaCl_Testing\Data\Solid_Graphite_Data" 
files = [
    "SG_Data01_00.csv",
    "SG_Data02_01.csv",
    "SG_Data03_02.csv",
    "SG_Data04_03.csv",
    "SG_Data05_04.csv",
    "SG_Data06_05.csv",
    "SG_Data07_06.csv",

    "SG_Data09_08.csv",
    "SG_Data10_09.csv",
    "SG_Data11_10.csv",
    "SG_Data12_11.csv"
]

MA_WINDOW = 1000     # Moving-average window size 
ENCODING = 'latin1' 
METRIC = 'mean'      # Metric for X–Y plot: 'mean' | 'median' | 'max' | 'min' | 'range'

# ==================================================================================================== HELPER FUNCTIONS (Moving Avg)

def moving_average(arr, window):

    if window <= 1:
        return arr.copy()
    kernel = np.ones(window) / window
    return np.convolve(arr, kernel, mode='same')

def extract_label_and_index(fname):

    m = re.search(r'_(\d{2})\.csv$', fname)
    if m:
        return f"{int(m.group(1))}", int(m.group(1))   # GNN label and index
    m2 = re.search(r'(\d+)', fname)
    if m2:
        return os.path.splitext(os.path.basename(fname))[0], int(m2.group(1))
    return os.path.splitext(os.path.basename(fname))[0], None

# ===================================================================================================== DATA PROCESSING (Moving Avg)

labels, indices, mins, maxs, summary = [], [], [], [], []

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
    # ------------------------------------------------------------------ check for column    
    if 'ADC_Value' not in df.columns:
        print(f"Skipping {fname}: no 'ADC_Value' column.")
        continue

    y_raw = pd.to_numeric(df['ADC_Value'], errors='coerce').dropna().values
    if y_raw.size == 0:
        print(f"Skipping {fname}: empty ADC data.")
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

    print(f"{fname} -> {lab} (idx={idx}) : min={cur_min:.3f}, max={cur_max:.3f}, mean={cur_mean:.3f}")


summary_df = pd.DataFrame(summary)
if summary_df['parsed_index'].notnull().any():
    summary_df.sort_values(by='parsed_index', inplace=True, na_position='last')
else:
    summary_df.sort_values(by='label', inplace=True)

labels_sorted = summary_df['label'].tolist()
mins_sorted = summary_df['min_smoothed'].tolist()
maxs_sorted = summary_df['max_smoothed'].tolist()

# ===================================================================================================== BAR CHART + TREND LINES + LINEAR FIT + R² ANALYSIS

x = np.arange(len(labels_sorted))
width = 0.35
degree = 1   # Linear model

plt.figure(figsize=(11,6))

a = x - width/2
b = x + width/2

# --------------------------------------------------------------------- Bars
plt.bar(a, mins_sorted, width, label='Min (smoothed)', alpha=0.7)
plt.bar(b, maxs_sorted, width, label='Max (smoothed)', alpha=0.7)

# ----------------------------------------------------------------------Joined bars
plt.plot(a, mins_sorted, '-', linewidth=1, label='Min trend')
plt.plot(b, maxs_sorted, '-', linewidth=1, label='Max trend')

# -------------------------------------------------------Linear fits
m_min, c_min = np.polyfit(a, mins_sorted, degree)
m_max, c_max = np.polyfit(b, maxs_sorted, degree)

y_min_fit = m_min * a + c_min
y_max_fit = m_max * b + c_max

def r_squared(y, y_fit):
    ss_res = np.sum((y - y_fit) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    return 1 - ss_res / ss_tot

r2_min = r_squared(np.array(mins_sorted), y_min_fit)
r2_max = r_squared(np.array(maxs_sorted), y_max_fit)

x_dense_min = np.linspace(a.min(), a.max(), 300)
x_dense_max = np.linspace(b.min(), b.max(), 300)

Y_dense_min = m_min * x_dense_min + c_min
Y_dense_max = m_max * x_dense_max + c_max

# ------------------------------------------------------------------------------------------------------------------- Plotting fits with equations and R²
plt.plot(x_dense_min, Y_dense_min, '--', linewidth=1, label=f"Min fit: y={m_min:.3f}x+{c_min:.3f}, R²={r2_min:.4f}", color='red')
plt.plot(x_dense_max, Y_dense_max, '--', linewidth=1, label=f"Max fit: y={m_max:.3f}x+{c_max:.3f}, R²={r2_max:.4f}", color='blue')

# -----------------------------------------------------------------------------------Avg fit line between min-max fits & R²
Avg = (Y_dense_min + Y_dense_max) / 2

# Linear fit for Avg curve
m_avg, c_avg = np.polyfit(x_dense_min, Avg, 1)
Y_avg_fit = m_avg * x_dense_min + c_avg

# R² for Avg curve
r2_avg = r_squared(Avg, Y_avg_fit)

# Plot Avg best-fit line (optional overlay, same line)
plt.plot(x_dense_min, Y_avg_fit, ':', linewidth=2, label=f"Avg fit eqn: y={m_avg:.3f}x+{c_avg:.3f}, R²={r2_avg:.4f}", color='darkgreen')


plt.xticks(x, labels_sorted, rotation=45)
plt.xlabel("Sample / Concentration (gm/20ml)")
plt.ylabel("ADC (smoothed)")
plt.title(f"Min–Max Analysis of Smoothed ADC Response for {TYP} Sensor with Linear Fit (MA Window = {MA_WINDOW})")
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()


print("\nLinear Fit Results:")
print(f"Min curve : y = {m_min:.6f}x + {c_min:.6f},  R² = {r2_min:.6f}")
print(f"Max curve : y = {m_max:.6f}x + {c_max:.6f},  R² = {r2_max:.6f}")
print(f"Avg curve : y = {m_avg:.6f}x + {c_avg:.6f},  R² = {r2_avg:.6f}")

# ==================================================================================================== X vs Y CHARACTERISTIC PLOT (SELECTED METRIC)

if METRIC == 'mean':
    y_vals = summary_df['mean_smoothed'].values
elif METRIC == 'median':
    y_vals = summary_df['median_smoothed'].values
elif METRIC == 'max':
    y_vals = summary_df['max_smoothed'].values
elif METRIC == 'min':
    y_vals = summary_df['min_smoothed'].values
elif METRIC == 'range':
    y_vals = summary_df['range_smoothed'].values
else:
    raise ValueError("Unsupported METRIC.")

y_err = summary_df['std_smoothed'].values

if summary_df['parsed_index'].notnull().any():
    x_vals = summary_df['parsed_index'].fillna(pd.Series(np.arange(len(summary_df)), index=summary_df.index)).values
    x_label = "Parsed index (concentration (gm/20ml))"
else:
    x_vals = np.arange(len(summary_df))
    x_label = "Sample (ordinal)"

plt.figure(figsize=(9,6))
plt.errorbar(x_vals, y_vals, yerr=y_err, fmt='o', capsize=4, label=f'{METRIC.capitalize()} ± 1σ')

for xv, mn, mx in zip(x_vals, summary_df['min_smoothed'], summary_df['max_smoothed']):
    plt.vlines(xv, mn, mx, linestyles='dashed', alpha=0.35)

for xv, yv, lab in zip(x_vals, y_vals, summary_df['label']):
    plt.annotate(lab, (xv, yv), xytext=(4,4), textcoords="offset points", fontsize=8)

plt.xlabel(x_label)
plt.ylabel(f"{METRIC.capitalize()} ADC (smoothed)")
plt.title(f"{TYP} Sensor Concentration vs {METRIC.capitalize()} ADC (MA window={MA_WINDOW})")
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.show()
