import serial
import csv
import time


PORT = "COM3"   
BAUD = 9600          
#CSV_FILENAME = "Data\Copper_Data\C_Data13_00.csv"

#CSV_FILENAME = "Data\Graphite_Data\G_Data13_00.csv"

#CSV_FILENAME = "Data\Graphite_INK_Data\GI_Data01_00.csv"
CSV_FILENAME = "Data\Graphite_INK_Data\DRY_RUN.csv"

#CSV_FILENAME = "Data\Solid_Graphite_Data\SG_Data01_00.csv"
#CSV_FILENAME = "Data\Solid_Graphite_Data\DRY_RUN.csv"

num_samples = 1000


ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)  

print("Logging data...")


with open(CSV_FILENAME, mode="w", newline="") as file:
    writer = csv.writer(file)
    

    # Header
    writer.writerow(["ADC_Value", "mV_Value"])

    count = 0

    while count < num_samples:
        try:
            line = ser.readline().decode().strip()

            if line:
                # Expected format: "12345, 456.78"
                data = line.split(",")

                if len(data) == 2:
                    adc = data[0].strip()
                    mv = data[1].strip()

                    writer.writerow([adc, mv])
                    count += 1

                    print(f"[{count}] Saved: ADC={adc}, mV={mv}")

        except Exception as e:
            print("Error:", e)
            continue

ser.close()
print(f"\nCompleted! {num_samples} samples saved to {CSV_FILENAME}")
