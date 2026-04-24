import pandas as pd
from sklearn.metrics import classification_report
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor

df = pd.read_csv("logs.csv")

df["status"] = df["status"].map({"success": 0, "failed": 1})
df["action"] = df["action"].map({
    "login": 0,
    "download": 1,
    "visit": 2
})

df["ip_count"] = df.groupby("ip")["ip"].transform("count")
df["ip_failed"] = df.groupby("ip")["status"].transform("sum")
df["action_variety"] = df.groupby("ip")["action"].transform("nunique")
df["fail_rate"] = df["ip_failed"] / df["ip_count"]

ml_data = df[[
    "action",
    "status",
    "ip_count",
    "ip_failed",
    "action_variety",
    "fail_rate"
]]

iso = IsolationForest(contamination=0.2, random_state=42)
df["iso"] = iso.fit_predict(ml_data)
df["iso"] = df["iso"].map({1: 0, -1: 1})

n_neighbors = min(5, len(ml_data) - 1)

if n_neighbors >= 2:
    lof = LocalOutlierFactor(n_neighbors=n_neighbors, contamination=0.2)
    lof_preds = lof.fit_predict(ml_data)
    df["lof"] = [0 if x == 1 else 1 for x in lof_preds]
else:
    df["lof"] = 0

# GROUND TRUTH
df["label"] = 0
df.loc[df["ip"] == "185.220.101.1", "label"] = 1

print("\n=== Isolation Forest ===")
print(classification_report(df["label"], df["iso"]))

print("\n=== LOF ===")
print(classification_report(df["label"], df["lof"]))