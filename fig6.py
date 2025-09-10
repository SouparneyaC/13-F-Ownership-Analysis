import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- Load and clean data ---
csv_path = "data/raw/ownership-institutional-valueTotals-n.2013-2025 (2).csv"
df = pd.read_csv(csv_path)

df["period"] = pd.to_datetime(df["period"], format="%Y%m%d", errors="coerce")
df["name"] = df["name"].astype(str).str.upper()

# --- Total AUM per quarter ---
total_q = df.groupby("period", as_index=False)["valueTotal"].sum().rename(columns={"valueTotal":"total_value"})

# --- 1. HHI (Herfindahl across manager AUM) ---
def hhi_for_group(g):
    total = g["valueTotal"].sum()
    if total <= 0: 
        return 0.0
    shares = g["valueTotal"] / total
    return float((shares**2).sum())

hhi = df.groupby("period").apply(hhi_for_group).reset_index(name="HHI")

# --- 2. Gini coefficient ---
def gini(array):
    array = np.sort(array)
    n = len(array)
    if n == 0: return 0
    return (2*np.sum((np.arange(1,n+1))*array)/(n*np.sum(array))) - (n+1)/n

gini_vals = df.groupby("period")["valueTotal"].apply(gini).reset_index(name="Gini")

# --- 3. Top N managers’ share (5 and 10) ---
topN_results = []
for period, group in df.groupby("period"):
    total_val = group["valueTotal"].sum()
    for N in [5, 10]:
        top_val = group.nlargest(N, "valueTotal")["valueTotal"].sum()
        share = top_val / total_val if total_val > 0 else 0
        topN_results.append({"period": period, "N": N, "share": share})

topN_df = pd.DataFrame(topN_results)

# --- 4. Big Three AUM share ---
pattern = r"BLACKROCK|VANGUARD|STATE\s*STREET"
big3_df = df[df["name"].str.contains(pattern, na=False)]
big3_q = big3_df.groupby("period")["valueTotal"].sum().reset_index().rename(columns={"valueTotal":"big3_value"})
big3_q = big3_q.merge(total_q, on="period", how="left")
big3_q["Big3_share"] = big3_q["big3_value"] / big3_q["total_value"]

# --- Merge everything into one DataFrame ---
merged = total_q[["period"]].merge(hhi, on="period").merge(gini_vals, on="period").merge(big3_q[["period","Big3_share"]], on="period")

for N in [5, 10]:
    sub = topN_df[topN_df["N"]==N][["period","share"]].rename(columns={"share":f"Top{N}_share"})
    merged = merged.merge(sub, on="period", how="left")

# --- Plotting (two panels, like paper Fig 6) ---
fig, axes = plt.subplots(2, 1, figsize=(12,10), sharex=True)

# Top panel: HHI only
axes[0].plot(merged["period"], merged["HHI"]*10000, label="HHI (×10,000)", color="red")
axes[0].set_title("Institutional Concentration (HHI only)")
axes[0].set_ylabel("HHI (×10,000)")
axes[0].legend(loc="upper left")
axes[0].grid(True)

# Bottom panel: the other metrics
axes[1].plot(merged["period"], merged["Top5_share"]*100, label="Top 5 Share (%)", color="blue")
axes[1].plot(merged["period"], merged["Top10_share"]*100, label="Top 10 Share (%)", color="green")
axes[1].plot(merged["period"], merged["Big3_share"]*100, label="Big Three Share (%)", color="purple")
axes[1].plot(merged["period"], merged["Gini"]*100, label="Gini (×100)", color="orange")
axes[1].set_title("Top Shares and Gini")
axes[1].set_xlabel("Year")
axes[1].set_ylabel("Share (%)")
axes[1].legend(loc="upper left")
axes[1].grid(True)
axes[1].set_ylim(0, 100)   

plt.tight_layout()
plt.show()
