import streamlit as st
import pandas as pd
import pytz
from paginas.funcoes import ler_sheets, ler_sheets_cache


df = ler_sheets('registro')
df['RA'] = df['RA'].astype(int)
bd = df_login = ler_sheets_cache('bd')
bd['RA'] = bd['RA'].astype(int)
bd = bd.merge(df[['RA', 'confirmacao_classificacao_orientadora','conclusao_classificacao_final']], how='left', on='RA')

lista_orientadoras = bd['Orientadora'].unique().tolist()

#visualização
st.title('Controle por Orientadora')
for i in lista_orientadoras:
    st.subheader(f'{i}')
    alunos_orientadora_total = bd.query(f"Orientadora == '{i}'")
    alunos_orientadora_total_registrados = alunos_orientadora_total.query("confirmacao_classificacao_orientadora == 'Não' or confirmacao_classificacao_orientadora == 'Sim'")
    try:
        st.progress(alunos_orientadora_total_registrados.shape[0]/alunos_orientadora_total.shape[0], f'Você registrou: **{alunos_orientadora_total_registrados.shape[0]}/{alunos_orientadora_total.shape[0]}**')
    except ZeroDivisionError:
        st.error('Zero Resultados')
for i in range(0 , 3):
    st.title(f'teste: {i}')