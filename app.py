import streamlit as st

st.set_page_config(
    page_title="CNES Predictor",
    layout="centered"
)

import json
import requests
import pandas as pd
from datetime import datetime


# ======================
# Config Azure ML
# ======================
AZUREML_ENDPOINT = "https://cnes-aml-phvxh.eastus.inference.ml.azure.com/score"
AZUREML_API_KEY = ""  # depois mova para secrets

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {AZUREML_API_KEY}",
}

# ======================
# Load snapshot
# ======================
@st.cache_data
def load_snapshot():
    df = pd.read_csv("features_snapshot.csv", parse_dates=["date"])
    return df

df_snapshot = load_snapshot()

# ======================
# Streamlit UI
# ======================

st.title("📊 CNES – Previsão de Profissionais de Saúde")
st.markdown(
    "Selecione o **município** e a **especialidade**. "
    "As demais variáveis são estimadas automaticamente a partir do histórico."
)

# ======================
# Inputs simples
# ======================
municipios = sorted(df_snapshot["NO_MUNICIPIO"].unique())
municipio = st.selectbox("Município", municipios)

especialidades = sorted(
    df_snapshot[df_snapshot["NO_MUNICIPIO"] == municipio]["DS_ATIVIDADE_PROFISSIONAL"].unique()
)
especialidade = st.selectbox("Especialidade", especialidades)

# ======================
# Botão
# ======================
if st.button("🔮 Prever"):
    # Filtra histórico
    df_filtered = df_snapshot[
        (df_snapshot["NO_MUNICIPIO"] == municipio) &
        (df_snapshot["DS_ATIVIDADE_PROFISSIONAL"] == especialidade)
    ]

    if df_filtered.empty:
        st.error("❌ Não há dados históricos para essa combinação.")
        st.stop()

    # Usa o registro mais recente
    row = df_filtered.sort_values("date").iloc[-1]

    payload = {
        "inputs": [
            {
                "NO_MUNICIPIO": row["NO_MUNICIPIO"],
                "DS_ATIVIDADE_PROFISSIONAL": row["DS_ATIVIDADE_PROFISSIONAL"],
                "POPULACAO_MENSAL": float(row["POPULACAO_MENSAL"]),
                "GROWTH_PCT": float(row["GROWTH_PCT"]),
                "lag1": float(row["lag1"]),
                "rolling3": float(row["rolling3"]),
                "time_index": int(row["time_index"]),
            }
        ]
    }

    with st.spinner("Consultando modelo..."):
        response = requests.post(
            AZUREML_ENDPOINT,
            headers=headers,
            data=json.dumps(payload),
            timeout=30,
        )

    if response.status_code == 200:
        result = response.json()
        prediction = result["predictions"][0]

        st.success("✅ Previsão realizada com sucesso!")
        st.metric(
            label="Profissionais por 1000 habitantes (previsto)",
            value=round(prediction, 3),
        )

        # Info contextual (excelente para TCC)
        st.caption(
            f"Base histórica usada: {row['date'].strftime('%Y-%m')} · "
            f"Valor observado: {round(row['PROFISSIONAIS_POR_1000'], 3)}"
        )

    else:
        st.error("❌ Erro ao chamar o endpoint")
        st.code(response.text)
