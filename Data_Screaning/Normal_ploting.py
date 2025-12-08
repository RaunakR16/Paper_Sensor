import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Use consistent forward slashes
# data1 = pd.read_csv("Data\Graphite_Data_06.11.2025\G_Data01_00.csv", encoding='latin1')
# data2 = pd.read_csv("Data\Graphite_Data_06.11.2025\G_Data02_01.csv", encoding='latin1')
# data3 = pd.read_csv("Data\Graphite_Data_06.11.2025\G_Data03_02.csv", encoding='latin1')
# data4 = pd.read_csv("Data\Graphite_Data_06.11.2025\G_Data04_03.csv", encoding='latin1')
# data5 = pd.read_csv("Data\Graphite_Data_06.11.2025\G_Data05_04.csv", encoding='latin1')
# data6 = pd.read_csv("Data\Graphite_Data_06.11.2025\G_Data06_05.csv", encoding='latin1')
# data7 = pd.read_csv("Data\Graphite_Data_06.11.2025\G_Data07_06.csv", encoding='latin1')
# data8 = pd.read_csv("Data\Graphite_Data_06.11.2025\G_Data08_07.csv", encoding='latin1')
# data9 = pd.read_csv("Data\Graphite_Data_06.11.2025\G_Data09_08.csv", encoding='latin1')
# data10 = pd.read_csv("Data\Graphite_Data_06.11.2025\G_Data10_09.csv", encoding='latin1')
# data11 = pd.read_csv("Data\Graphite_Data_06.11.2025\G_Data11_10.csv", encoding='latin1')
# data12 = pd.read_csv("Data\Graphite_Data_06.11.2025\G_Data12_11.csv", encoding='latin1')

data1 = pd.read_csv("Data\Copper_Data_06.11.2025\C_Data01_00.csv", encoding='latin1')
data2 = pd.read_csv("Data\Copper_Data_06.11.2025\C_Data02_01.csv", encoding='latin1')
data3 = pd.read_csv("Data\Copper_Data_06.11.2025\C_Data03_02.csv", encoding='latin1')
data4 = pd.read_csv("Data\Copper_Data_06.11.2025\C_Data04_03.csv", encoding='latin1')
data5 = pd.read_csv("Data\Copper_Data_06.11.2025\C_Data05_04.csv", encoding='latin1')
data6 = pd.read_csv("Data\Copper_Data_06.11.2025\C_Data06_05.csv", encoding='latin1')
data7 = pd.read_csv("Data\Copper_Data_06.11.2025\C_Data07_06.csv", encoding='latin1')
data8 = pd.read_csv("Data\Copper_Data_06.11.2025\C_Data08_07.csv", encoding='latin1')
data9 = pd.read_csv("Data\Copper_Data_06.11.2025\C_Data09_08.csv", encoding='latin1')
data10 = pd.read_csv("Data\Copper_Data_06.11.2025\C_Data10_09.csv", encoding='latin1')
data11 = pd.read_csv("Data\Copper_Data_06.11.2025\C_Data11_10.csv", encoding='latin1')
data12 = pd.read_csv("Data\Copper_Data_06.11.2025\C_Data12_11.csv", encoding='latin1')


print(data1.head())

y1 = data1['ADC_Value'].values
y2 = data2['ADC_Value'].values
y3 = data3['ADC_Value'].values
y4 = data4['ADC_Value'].values
y5 = data5['ADC_Value'].values
y6 = data6['ADC_Value'].values
y7 = data7['ADC_Value'].values
y8 = data8['ADC_Value'].values
y9 = data9['ADC_Value'].values
y10 = data10['ADC_Value'].values
y11 = data11['ADC_Value'].values
y12 = data12['ADC_Value'].values

# Plotting
plt.figure(figsize=(10, 6))
plt.plot( y1, label='G0', color='blue', linestyle='-', markersize=4)
# plt.plot( y2, label='G1', color='red', linestyle='-', markersize=4)
plt.plot( y3, label='G2', color='green', linestyle='-', markersize=4)
plt.plot( y4, label='G3', color='orange', linestyle='-', markersize=4)
plt.plot( y5, label='G4', color='purple', linestyle='-', markersize=4)
plt.plot( y6, label='G5', color='brown', linestyle='-', markersize=4)
# plt.plot( y7, label='G6', color='pink', linestyle='-', markersize=4)
plt.plot( y8, label='G7', color='gray', linestyle='-', markersize=4)
plt.plot( y9, label='G8', color='olive', linestyle='-', markersize=4)
plt.plot( y10, label='G9', color='cyan', linestyle='-', markersize=4)
# plt.plot( y11, label='G10', color='magenta', linestyle='-', markersize=4)
# plt.plot( y12, label='G11', color='lime', linestyle='-', markersize=4)

# Adding labels and title
plt.xlabel('Time (mS)')
plt.ylabel('ADC')
plt.title('Time Vs ADC')
plt.legend()
plt.grid(True)

# Show plot
plt.tight_layout()
plt.show()