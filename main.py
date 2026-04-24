import streamlit as st
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
import time

st.title("SIEM Inteligent - Monitorizare in timp real")

refresh_interval = st.slider("Interval refresh (secunde)", 1, 10, 3)

placeholder = st.empty()

while True:
    try:
        df = pd.read_csv("logs.csv")

        # =========================
        # PREPROCESARE
        # =========================
        df["status"] = df["status"].map({"success": 0, "failed": 1})
        df["action"] = df["action"].map({
            "login": 0,
            "download": 1,
            "visit": 2
        })

        df["timestamp"] = pd.to_datetime(df["timestamp"])

        # =========================
        # FEATURE ENGINEERING
        # =========================
        df["ip_count"] = df.groupby("ip")["ip"].transform("count")
        df["ip_failed"] = df.groupby("ip")["status"].transform("sum")

        # =========================
        # ML
        # =========================
        ml_data = df[["action", "status", "ip_count", "ip_failed"]]

        iso_model = IsolationForest(contamination=0.2, random_state=42)
        df["iso"] = iso_model.fit_predict(ml_data)
        df["iso"] = df["iso"].map({1: 0, -1: 1})

        lof_model = LocalOutlierFactor(n_neighbors=5, contamination=0.2)
        lof_preds = lof_model.fit_predict(ml_data)
        df["lof"] = [0 if x == 1 else 1 for x in lof_preds]

        # =========================
        # RULES
        # =========================
        brute_force = df[df["ip_failed"] > 5]

        # trafic mare (posibil DoS)
        high_traffic = df[df["ip_count"] > 15]

        # =========================
        # UI
        # =========================
        with placeholder.container():

            st.subheader("Date curente")
            st.write(df.tail(10))

            st.subheader("Detectie Brute Force")
            st.write(brute_force[["ip", "ip_failed"]].drop_duplicates())

            if not brute_force.empty:
                st.error("ATAC BRUTE FORCE DETECTAT")

            st.subheader("Trafic suspect (volum mare)")
            st.write(high_traffic[["ip", "ip_count"]].drop_duplicates())

            if not high_traffic.empty:
                st.warning("Trafic anormal detectat")

            st.subheader("Anomalii ML (Isolation Forest)")
            st.write(df[df["iso"] == 1][["ip", "action", "status"]])

            st.subheader("Anomalii ML (LOF)")
            st.write(df[df["lof"] == 1][["ip", "action", "status"]])

    except Exception as e:
        st.error(f"Eroare: {e}")

    time.sleep(refresh_interval)