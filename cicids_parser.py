import pandas as pd
import random
from datetime import datetime, timedelta

df = pd.read_csv("cicids.csv")

# 🔥 FIX IMPORTANT
df.columns = df.columns.str.strip()

logs = []

for i, row in df.head(2000).iterrows():

    timestamp = datetime.now() - timedelta(seconds=random.randint(0, 10000))
    ip = f"192.168.1.{random.randint(1, 255)}"

    # 🔥 acum merge sigur
    if row["Label"] == "BENIGN":
        status = "success"
        action = random.choice(["visit", "download"])
    else:
        status = "failed"
        action = "login"

    logs.append([timestamp, ip, action, status])

df_logs = pd.DataFrame(logs, columns=["timestamp", "ip", "action", "status"])
df_logs.to_csv("logs.csv", index=False)

print("Logs reale generate din CICIDS!")