
# CNES Serving

Este repositório é responsável pela **camada de Machine Learning e Serving**
do projeto CNES, consumindo dados analíticos da camada **Gold**
e disponibilizando resultados para **usuários de negócio** por meio de APIs e dashboards interativos.

---


### Visão Geral

- **Entrada**: Dados Gold do Azure Data Lake
- **Treinamento**: Azure Machine Learning
- **Serving**: Azure Container Instances
- **Visualização**: Streamlit
- **Usuário final**: Analistas, gestores e decisores

---

## 🤖 Machine Learning

Este repositório contempla:

- Treinamento de modelos preditivos
- Versionamento de artefatos (modelos, métricas, features)
- Avaliação offline
- Preparação para inferência

Os modelos podem ser utilizados para:
- Análise de distribuição de profissionais de saúde
- Suporte à tomada de decisão em políticas públicas
- Exploração territorial e demográfica

---

## 📊 Streamlit App

A aplicação Streamlit permite:

- Exploração interativa dos dados
- Visualização de métricas e distribuições
- Consumo direto por usuários não técnicos

### Execução local
```bash
streamlit run app/main.py
