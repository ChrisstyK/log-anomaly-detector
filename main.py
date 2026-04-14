import pandas as pd
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt

# =========================
# 1. CITIRE DATE
# =========================
df = pd.read_csv("logs.csv")

print("=== DATE INITIALE ===")
print(df)


# =========================
# 2. PREPROCESARE + FEATURE ENGINEERING
# =========================

# encoding
df["status"] = df["status"].map({"success": 0, "failed": 1})
df["action"] = df["action"].map({"login": 0, "download": 1})

# timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"])

# feature: număr evenimente per IP
df["ip_count"] = df.groupby("ip")["ip"].transform("count")

# feature: număr failed per IP
df["ip_failed"] = df.groupby("ip")["status"].transform("sum")

print("\n=== FEATURE ENGINEERING ===")
print(df[["ip", "action", "status", "ip_count", "ip_failed"]])


# =========================
# 3. MODEL ML
# =========================

# alegem doar coloane numerice pentru ML
ml_data = df[["action", "status", "ip_count", "ip_failed"]]

model = IsolationForest(contamination=0.2, random_state=42)

df["anomaly"] = model.fit_predict(ml_data)

# transformare
df["anomaly"] = df["anomaly"].map({1: 0, -1: 1})

print("\n=== REZULTAT ML ===")
print(df[["ip", "action", "status", "ip_count", "ip_failed", "anomaly"]])


# =========================
# 4. DETECTIE BRUTE FORCE (RULE-BASED)
# =========================

# prag: mai mult de 5 login failed
brute_force = df[df["ip_failed"] > 5]

print("\n=== DETECTIE BRUTE FORCE ===")
print(brute_force[["ip", "ip_failed"]].drop_duplicates())


# =========================
# 5. ANOMALII ML
# =========================

anomalies = df[df["anomaly"] == 1]

print("\n=== ANOMALII ML ===")
print(anomalies[["ip", "action", "status"]])


# =========================
# 6. GRAFIC
# =========================

plt.figure()

normal = df[df["anomaly"] == 0]
plt.scatter(normal.index, normal["status"], label="Normal")

plt.scatter(anomalies.index, anomalies["status"], label="Anomalie")

plt.title("Detectie Anomalii + Atacuri")
plt.xlabel("Index")
plt.ylabel("Status (0=OK, 1=Failed)")
plt.legend()

plt.show()