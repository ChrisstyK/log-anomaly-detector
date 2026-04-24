import streamlit as st
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
import time

from gpt_explainer import generate_ai_explanation
from email_sender import send_email_alert

st.set_page_config(layout="wide")
st.title("SIEM Inteligent (ML + AI + Email)")

refresh_interval = st.slider("Refresh (sec)", 1, 10, 3)
placeholder = st.empty()

action_map = {0: "login", 1: "download", 2: "visit"}
status_map = {0: "success", 1: "failed"}

# 🔥 prevenire spam email
sent_ips = set()


def generate_alert(row):
    ai_text = generate_ai_explanation(row)

    return f"""
ALERTĂ SECURITATE

IP: {row['ip']}
Acțiune: {action_map.get(row['action'])}
Status: {status_map.get(row['status'])}

Scor risc: {round(row['risk_score'], 2)}

Analiză AI:
{ai_text}
"""


def save_alert(text):
    with open("alerts.log", "a", encoding="utf-8") as f:
        f.write(text + "\n-----------------\n")


while True:
    try:
        df = pd.read_csv("logs.csv")

        df["status"] = df["status"].map({"success": 0, "failed": 1})
        df["action"] = df["action"].map({
            "login": 0,
            "download": 1,
            "visit": 2
        })

        df["timestamp"] = pd.to_datetime(df["timestamp"])

        # =========================
        # FEATURES
        # =========================
        df["ip_count"] = df.groupby("ip")["ip"].transform("count")
        df["ip_failed"] = df.groupby("ip")["status"].transform("sum")
        df["action_variety"] = df.groupby("ip")["action"].transform("nunique")
        df["fail_rate"] = df["ip_failed"] / df["ip_count"]

        ml_data = df[[
            "action", "status",
            "ip_count", "ip_failed",
            "action_variety", "fail_rate"
        ]]

        # =========================
        # ML
        # =========================
        iso = IsolationForest(contamination=0.2)
        df["iso"] = iso.fit_predict(ml_data)
        df["iso"] = df["iso"].map({1: 0, -1: 1})

        n = min(5, len(df) - 1)
        if n >= 2:
            lof = LocalOutlierFactor(n_neighbors=n)
            df["lof"] = lof.fit_predict(ml_data)
            df["lof"] = [0 if x == 1 else 1 for x in df["lof"]]
        else:
            df["lof"] = 0

        df["final_alert"] = df[["iso", "lof"]].max(axis=1)

        # =========================
        # RISK
        # =========================
        df["risk_score"] = (
            df["fail_rate"] * 50 +
            df["ip_count"] * 1.5 +
            df["action_variety"] * 10 +
            df["final_alert"] * 30
        )

        with placeholder.container():

            st.subheader("Anomalii detectate")

            anomalies = df[df["final_alert"] == 1]

            st.write(anomalies[[
                "ip", "action", "status", "risk_score"
            ]])

            # 🔥 IMPORTANT: max 1-2 alerte GPT
            for _, row in anomalies.head(2).iterrows():

                if row["ip"] in sent_ips:
                    continue

                alert = generate_alert(row)

                st.warning(alert)
                save_alert(alert)

                # 📧 TRIMITERE EMAIL
                send_email_alert(
                    subject="🚨 Alertă securitate detectată",
                    body=alert
                )

                sent_ips.add(row["ip"])

    except Exception as e:
        st.error(e)

    time.sleep(refresh_interval)