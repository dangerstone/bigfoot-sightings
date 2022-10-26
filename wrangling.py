import pandas as pd
import missingno as msno
import numpy as np

df = pd.read_csv("data/bfro_reports_geocoded.csv")

# Actual data wrangling
noOfColumns = len(df.columns)
noOfRows = len(df.index)

print(noOfColumns)
print(noOfRows)

# df.info()
msno.heatmap(df)
