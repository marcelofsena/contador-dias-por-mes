import streamlit as st
import pandas as pd

# Tradução de nomes de meses
MESES_PT = {
    "January": "Janeiro", "February": "Fevereiro", "March": "Março",
    "April": "Abril", "May": "Maio", "June": "Junho",
    "July": "Julho", "August": "Agosto", "September": "Setembro",
    "October": "Outubro", "November": "Novembro", "December": "Dezembro"
}


from datetime import datetime, timedelta
from collections import defaultdict

st.set_page_config(page_title="Contador de Dias por Mês", layout="centered")

st.title("📅 Contador de Dias por Mês")

st.markdown("Adicione intervalos de datas e veja a quantidade de dias separados por mês.")
st.markdown("**Formato de data: dd/mm/aaaa**")

# Função auxiliar
def calcular_dias_por_mes(periodos):
    dias_por_mes = defaultdict(int)

    for inicio, fim in periodos:
        data_atual = inicio
        while data_atual <= fim:
            mes_en = data_atual.strftime("%B")
            mes_pt = MESES_PT.get(mes_en, mes_en)
            chave = f"{mes_pt}/{data_atual.year}"

            dias_por_mes[chave] += 1
            data_atual += timedelta(days=1)

    return dias_por_mes

# Entrada de períodos
num_periodos = st.number_input("Quantos períodos deseja inserir?", min_value=1, max_value=10, value=1, step=1)

periodos = []
for i in range(num_periodos):
    col1, col2 = st.columns(2)
    with col1:
        inicio = st.date_input(f"📆 Data inicial do período {i+1}", format="DD/MM/YYYY", key=f"inicio_{i}")
    with col2:
        fim = st.date_input(f"📆 Data final do período {i+1}", format="DD/MM/YYYY", key=f"fim_{i}")

    if inicio > fim:
        st.warning(f"A data inicial não pode ser depois da final no período {i+1}")
    else:
        periodos.append((inicio, fim))

# Botão para calcular dias por mês
if st.button("📊 Calcular dias por mês"):
    dias = calcular_dias_por_mes(periodos)
    st.session_state['dias'] = dict(dias)
    st.session_state['calculo_feito'] = True

# Exibe os resultados se o cálculo foi feito
if st.session_state.get('calculo_feito', False):
    st.subheader("📋 Resultado com ajustes por mês:")

        # Campo para valor base
    valor_base = st.number_input("💰 Informe o valor base", min_value=0.0, format="%.2f")

    tabela_resultado = []
    total_original = 0
    total_ajustado = 0
    total_calculo_final = 0

    MES_PARA_NUM = {
    "Janeiro": 1, "Fevereiro": 2, "Março": 3,
    "Abril": 4, "Maio": 5, "Junho": 6,
    "Julho": 7, "Agosto": 8, "Setembro": 9,
    "Outubro": 10, "Novembro": 11, "Dezembro": 12
    }
    for mes, qtd in sorted(
    st.session_state['dias'].items(),
    key=lambda x: (int(x[0].split("/")[1]), MES_PARA_NUM[x[0].split("/")[0]])
    ):
        subtrair = st.number_input(f"Subtrair de {mes}", min_value=0, max_value=qtd, value=0, key=f"sub_{mes}")
        ajustado = qtd - subtrair
        total_original += qtd
        total_ajustado += ajustado

        valor_20 = (valor_base * 0.20)/30
        resultado_final = valor_20 * ajustado
        total_calculo_final += resultado_final

        tabela_resultado.append({
            "Mês/Ano": mes,
            "Total de Dias": qtd,
            "Subtração": subtrair,
            "Resultado Ajustado": ajustado,
            "💸 Resultado (20% x dias)": round(resultado_final, 2)
        })

    if tabela_resultado:
        df_resultado = pd.DataFrame(tabela_resultado)
        st.dataframe(df_resultado, use_container_width=True)

        st.markdown(f"🧮 **Total de dias originais:** {total_original}")
        st.markdown(f"🧮 **Total após subtrações:** {total_ajustado}")
        st.markdown(f"💵 **Valor 20% do base:** R$ {valor_base * 0.20:.2f}")
        st.markdown(f"💰 **Total geral (20% x dias ajustados):** R$ {total_calculo_final:.2f}")

