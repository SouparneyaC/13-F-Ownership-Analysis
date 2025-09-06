import pandas as pd
import matplotlib.pyplot as plt

# load the dataset
csv_path = "data/raw/ownership-institutional-valueTotals-n.2013-2025 (2).csv"
df = pd.read_csv(csv_path)

# convert the period column into datetime
df["period"] = pd.to_datetime(df["period"], format="%Y%m%d", errors="coerce")

# count unique managers (by cik) for each quarter
managers_per_quarter = df.groupby("period")["cik"].nunique().reset_index()
managers_per_quarter.rename(columns={"cik": "num_managers"}, inplace=True)

# quick check
print(managers_per_quarter.head())

# plot the number of managers over time
plt.figure(figsize=(10,6))
plt.plot(managers_per_quarter["period"], managers_per_quarter["num_managers"], color="green")
plt.title("Replication of Figure 3: Number of 13(f) Managers")
plt.xlabel("Year")
plt.ylabel("Number of Managers")
plt.grid(True)
plt.show()
