import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_ai_explanation(row):

    prompt = f"""
Ești analist SOC.

Analizează acest eveniment:

IP: {row['ip']}
fail_rate: {row['fail_rate']}
ip_count: {row['ip_count']}
action_variety: {row['action_variety']}
IsolationForest: {row['iso']}
LOF: {row['lof']}

Răspunde STRUCTURAT:

Tip anomalie:
Explicație:
Risc:
Recomandare:
"""

    try:
        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {"role": "system", "content": "Ești expert în securitate cibernetică."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Eroare AI: {e}"