import pandas as pd
import pyxlsb

# Replace 'input.csv' with your CSV file name and 'output.xlsb' with the desired XLSB file name
csv_file = 'test.csv'
xlsb_file = 'output.xlsb'

# Read CSV file into a pandas DataFrame
df = pd.read_csv(csv_file)

# Write DataFrame to XLSB file
with pd.ExcelWriter(xlsb_file, engine='pyxlsb') as writer:
    df.to_excel(writer, index=False)

print(f'{csv_file} has been successfully converted to {xlsb_file}.')
