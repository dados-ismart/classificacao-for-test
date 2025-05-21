import streamlit as st
import pandas as pd
import pytz
from paginas.funcoes import ler_sheets, ler_sheets_cache

# importar dados
df = ler_sheets('registro')
df['RA'] = df['RA'].astype(int)
bd = df_login = ler_sheets_cache('bd')
bd['RA'] = bd['RA'].astype(int)
bd = bd.merge(df[['RA', 'confirmacao_classificacao_orientadora','conclusao_classificacao_final']], how='left', on='RA')

#tratar dados
orientadoras_por_cidade = bd.groupby('Cidade')['Orientadora'].unique().to_dict()

#visualização
with st.expander("Controle por Orientadora"):
    for cidade, orientadoras in orientadoras_por_cidade.items():
        st.divider()
        st.header(f'{cidade}')
        for orientadora in orientadoras:
            st.subheader(f'{orientadora}')
            alunos_orientadora_total = bd.query(f"Orientadora == '{orientadora}'")
            alunos_orientadora_total_registrados = alunos_orientadora_total.query("confirmacao_classificacao_orientadora == 'Não' or confirmacao_classificacao_orientadora == 'Sim'")
            try:
                st.progress(alunos_orientadora_total_registrados.shape[0]/alunos_orientadora_total.shape[0], f'Você registrou: **{alunos_orientadora_total_registrados.shape[0]}/{alunos_orientadora_total.shape[0]}**')
            except ZeroDivisionError:
                st.error('Zero Resultados')
