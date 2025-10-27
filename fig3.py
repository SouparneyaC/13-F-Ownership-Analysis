import pandas as pd
import matplotlib.pyplot as plt

csv_path = "data/raw/ownership-institutional-valueTotals-n.2013-2025 (2).csv"
df = pd.read_csv(csv_path)

# converted the period column into datetime
df["period"] = pd.to_datetime(df["period"], format="%Y%m%d", errors="coerce")

managers_per_quarter = df.groupby("period")["cik"].nunique().reset_index()
managers_per_quarter.rename(columns={"cik": "num_managers"}, inplace=True)

# check
print(managers_per_quarter.head())

#Plot
plt.figure(figsize=(10,6))
plt.plot(managers_per_quarter["period"], managers_per_quarter["num_managers"], color="green")
plt.title("Replication of Figure 3: Number of 13(f) Managers")
plt.xlabel("Year")
plt.ylabel("Number of Managers")
plt.grid(True)
plt.show()
