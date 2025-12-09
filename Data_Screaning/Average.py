import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Use consistent forward slashes
data1 = pd.read_csv("Data\Graphite_Data_06.11.2025\G_Data01_00.csv", encoding='latin1')
data2 = pd.read_csv("Data\Graphite_Data_06.11.2025\G_Data02_01.csv", encoding='latin1')
data3 = pd.read_csv("Data\Graphite_Data_06.11.2025\G_Data03_02.csv", encoding='latin1')
data5 = pd.read_csv("Data\Graphite_Data_06.11.2025\G_Data05_04.csv", encoding='latin1')
data6 = pd.read_csv("Data\Graphite_Data_06.11.2025\G_Data06_05.csv", encoding='latin1')
data7 = pd.read_csv("Data\Graphite_Data_06.11.2025\G_Data07_06.csv", encoding='latin1')
data10 = pd.read_csv("Data\Graphite_Data_06.11.2025\G_Data10_09.csv", encoding='latin1')
data12 = pd.read_csv("Data\Graphite_Data_06.11.2025\G_Data12_11.csv", encoding='latin1')

# data1 = pd.read_csv("Data\Copper_Data_06.11.2025\C_Data01_00.csv", encoding='latin1')
# data3 = pd.read_csv("Data\Copper_Data_06.11.2025\C_Data03_02.csv", encoding='latin1')
# data4 = pd.read_csv("Data\Copper_Data_06.11.2025\C_Data04_03.csv", encoding='latin1')
# data5 = pd.read_csv("Data\Copper_Data_06.11.2025\C_Data05_04.csv", encoding='latin1')
# data6 = pd.read_csv("Data\Copper_Data_06.11.2025\C_Data06_05.csv", encoding='latin1')
# data8 = pd.read_csv("Data\Copper_Data_06.11.2025\C_Data08_07.csv", encoding='latin1')
# data9 = pd.read_csv("Data\Copper_Data_06.11.2025\C_Data09_08.csv", encoding='latin1')
# data10 = pd.read_csv("Data\Copper_Data_06.11.2025\C_Data10_09.csv", encoding='latin1')

# GRAPHITE DATA
datasets = [
    data1['ADC_Value'], 
    data2['ADC_Value'], 
    data3['ADC_Value'], 
    data5['ADC_Value'], 
    data6['ADC_Value'], 
    data7['ADC_Value'], 
    data10['ADC_Value'], 
    data12['ADC_Value']
]

#COPPER DATA
# datasets = [
#     data1['ADC_Value'], 
#     data3['ADC_Value'], 
#     data4['ADC_Value'],
#     data5['ADC_Value'], 
#     data6['ADC_Value'], 
#     data8['ADC_Value'],
#     data9['ADC_Value'], 
#     data10['ADC_Value']
# ]

labels = ["G0","G1","G2","G4","G5","G6","G9","G10"]
# labels = ["C0","C2","C3","C4","C5","C7","C8","C9"]

# Compute averages
avg_values = [np.mean(d) for d in datasets]

print("Average ADC Values:", avg_values)

# Plot Bar Graph
plt.figure(figsize=(10,6))
plt.bar(labels, avg_values)


plt.xlabel("Dataset")
plt.ylabel("Average ADC Value")
plt.title("Average ADC Value for Each Graphite Sample")
plt.grid(axis='y', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()
