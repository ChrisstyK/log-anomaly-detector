import math

def analyze_event(row):

    fail_score = row["fail_rate"]
    traffic_score = row["ip_count"]
    variety_score = row["action_variety"]
    ml_score = row["iso"] + row["lof"]

    if fail_score > 0.6 and row["ip_failed"] > 5:
        attack_type = "Brute Force Attack"
        severity = "HIGH"
        description = "Multiple autentificări eșuate într-un timp scurt."

    elif traffic_score > 20:
        attack_type = "Traffic Flood / DoS"
        severity = "HIGH"
        description = "Volum neobișnuit de trafic."

    elif fail_score > 0.3:
        attack_type = "Slow Attack"
        severity = "MEDIUM"
        description = "Atac lent pentru a evita detecția."

    elif variety_score > 2:
        attack_type = "Behavior Anomaly"
        severity = "MEDIUM"
        description = "Comportament diferit de normal."

    elif ml_score > 0:
        attack_type = "Unknown ML Anomaly"
        severity = "LOW"
        description = "Deviere detectată de ML."

    else:
        attack_type = "Normal"
        severity = "INFO"
        description = "Activitate normală."

    confidence = min(round(
        fail_score * 50 +
        traffic_score * 1.5 +
        variety_score * 10 +
        ml_score * 20, 2), 100)

    if severity == "HIGH":
        recommendation = "Blocare IP imediat."
    elif severity == "MEDIUM":
        recommendation = "Monitorizare."
    elif severity == "LOW":
        recommendation = "Verificare manuală."
    else:
        recommendation = "OK."

    return {
        "type": attack_type,
        "severity": severity,
        "confidence": confidence,
        "description": description,
        "recommendation": recommendation
    }