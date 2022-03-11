import pandas as pd
import xlrd

file = '/Users/alainzypinoglou/Desktop/pretbrsm.xlsx'
df = pd.ExcelFile(file)
print(df.sheet_names)
df1 = df.parse('TOTO')
print(type(df1))
