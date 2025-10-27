import pandas as pd
import matplotlib.pyplot as plt

csv_path = "data/raw/ownership-institutional-valueTotals-n.2013-2025 (2).csv"
df = pd.read_csv(csv_path)

df["period"] = pd.to_datetime(df["period"], format="%Y%m%d", errors="coerce")
inst_per_quarter = df.groupby("period")["valueTotal"].sum().reset_index()

# here I just scale the values between 0 and 1 since I don’t have total market cap
inst_per_quarter["inst_share"] = inst_per_quarter["valueTotal"] / inst_per_quarter["valueTotal"].max()

# retail share is just whatever is left over
inst_per_quarter["retail_share"] = 1 - inst_per_quarter["inst_share"]

# plot
plt.figure(figsize=(10,6))
plt.plot(inst_per_quarter["period"], inst_per_quarter["inst_share"], label="Institutional Share", color="blue")
plt.plot(inst_per_quarter["period"], inst_per_quarter["retail_share"], label="Retail Share", color="red", linestyle="--")
plt.title("Replication of Figure 4")
plt.xlabel("Year")
plt.ylabel("Share (normalized)")
plt.legend()
plt.grid(True)
plt.show()
