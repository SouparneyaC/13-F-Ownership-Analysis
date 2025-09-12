import pandas as pd
import numpy as np

# Toy dataset: 2 firms × 3 managers
data = [
    ("2020Q1", "FirmA", "M1", 50, 100),
    ("2020Q1", "FirmA", "M2", 30, 100),
    ("2020Q1", "FirmA", "M3", 20, 100),
    ("2020Q1", "FirmB", "M1", 10, 200),
    ("2020Q1", "FirmB", "M2", 50, 200),
    ("2020Q1", "FirmB", "M3", 140, 200),
]

df = pd.DataFrame(data, columns=["period", "firm", "manager", "value_held", "market_cap"])
df["beta"] = df["value_held"] / df["market_cap"]

# κ function with α parameter
def compute_kappa(group, alpha=1):
    betas = group["beta"].to_numpy()
    gammas = betas**alpha   # apply control assumption
    num = np.sum([gammas[i]*gammas[j] for i in range(len(gammas)) for j in range(len(gammas)) if i != j])
    den = np.sum(gammas**2)
    return num / den if den > 0 else np.nan

# compute κ under different α assumptions
results = []
for alpha in [0.5, 1, 2]:
    kappa_df = df.groupby(["period", "firm"], group_keys=False).apply(compute_kappa, alpha=alpha).reset_index(name="kappa")
    kappa_df["alpha"] = alpha
    results.append(kappa_df)

final = pd.concat(results)

print("Toy κ results under different control assumptions:")
print(final)
