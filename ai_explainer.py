import random

def generate_explanation(row):
    explanations = []

    if row["fail_rate"] > 0.6:
        explanations.append("număr mare de autentificări eșuate")

    if row["ip_count"] > 20:
        explanations.append("trafic intens de la același IP")

    if row["action_variety"] > 2:
        explanations.append("diversitate neobișnuită de acțiuni")

    if row["iso"] == 1:
        explanations.append("anomalie detectată de modelul Isolation Forest")

    if row["lof"] == 1:
        explanations.append("anomalie detectată de modelul LOF")

    if not explanations:
        explanations.append("abatere minoră de la comportamentul normal")

    return explanations


def generate_description(row):
    explanations = generate_explanation(row)

    intro = random.choice([
        "Activitatea analizată indică un comportament suspect.",
        "S-a identificat un tipar anormal în trafic.",
        "Analiza sistemului sugerează o posibilă activitate malițioasă."
    ])

    return intro + " Cauze: " + ", ".join(explanations) + "."


def generate_recommendation(row):

    if row["fail_rate"] > 0.6:
        return "Blocarea temporară a IP-ului și investigarea autentificărilor."

    elif row["ip_count"] > 20:
        return "Aplicarea rate limiting sau blocarea IP-ului."

    elif row["action_variety"] > 2:
        return "Monitorizarea comportamentului și analiză manuală."

    elif row["iso"] == 1 or row["lof"] == 1:
        return "Verificare suplimentară a activității detectate de ML."

    return "Nu sunt necesare acțiuni."