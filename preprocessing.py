import pandas as pd

df = pd.read_csv("data/raw/bfro_reports_geocoded.csv")

irrelevant_columns = [
    "cloud_cover",
    "dew_point",
    "geohash",
    "humidity",
    "moon_phase",
    "precip_intensity",
    "precip_probability",
    "precip_type",
    "pressure",
    "temperature_high",
    "temperature_low",
    "uv_index",
    "wind_bearing",
    "wind_speed",
]

for col in irrelevant_columns:
    df.pop(col)


# adding more columns
df2 = pd.read_json("data/raw/bfro_reports.json")
df.join(df2["time_and_conditions"])

noOfColumns = len(df.columns)

df.to_csv("data/bfro_reports_geocoded.csv")
