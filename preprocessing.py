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
df2 = pd.read_json("data/raw/bfro_reports.json", lines=True)
df = df.join(df2["TIME_AND_CONDITIONS"])
df = df.rename(columns={"TIME_AND_CONDITIONS": "time_and_conditions"})

# add ansi columns
df_ansi = pd.read_csv("data/misc/ansi.csv")

df["state_ansi_code"] = [
    str(df_ansi.loc[df_ansi["state"] == x, "state_ansi_code"].iat[0]).zfill(2)
    for x in df["state"]
]

# reorder columns
neworder = [
    "number",
    "date",
    "season",
    "classification",
    "state_ansi_code",
    "state",
    "county",
    "latitude",
    "longitude",
    "temperature_mid",
    "summary",
    "visibility",
    "title",
    "observed",
    "location_details",
    "time_and_conditions",
]  # print(df.columns)
df = df.reindex(columns=neworder)
df = df.rename(columns={"summary": "weather_summary"})

noOfColumns = len(df.columns)

df.to_csv("data/bfro_reports_geocoded.csv", index=False)
