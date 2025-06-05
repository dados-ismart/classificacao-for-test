import streamlit as st
import pandas as pd
import pytz
from paginas.funcoes import ler_sheets, ler_sheets_cache, registrar, esvazia_aba

# importar dados
df = ler_sheets('registro')
df['RA'] = df['RA'].astype(int)
bd = ler_sheets_cache('bd')
bd['RA'] = bd['RA'].astype(int)
bd = bd.merge(df[['RA', 'confirmacao_classificacao_orientadora','conclusao_classificacao_final']], how='left', on='RA')


st.title('Geral')
st.header('Alunos Registrados por Orientadoras')
qtd_alunos = bd.shape[0]
qtd_alunos_registrados = bd.query("confirmacao_classificacao_orientadora == 'Não' or confirmacao_classificacao_orientadora == 'Sim'").shape[0]
try:
    st.progress(qtd_alunos_registrados/qtd_alunos, f'Status de Preenchimento das Orientadoras de ***Todas as Praças***: **{qtd_alunos_registrados}/{qtd_alunos}**')
except ZeroDivisionError:
    st.error('Zero Resultados')
st.divider()

st.header('Alunos Confirmados por Coordenadoras')
qtd_alunos = bd.shape[0]
qtd_alunos_registrados = bd.query("conclusao_classificacao_final == 'Sim'").shape[0]
try:
    st.progress(qtd_alunos_registrados/qtd_alunos, f'Status de Preenchimento das Coordenadoras de ***Todas as Praças***: **{qtd_alunos_registrados}/{qtd_alunos}**')
except ZeroDivisionError:
    st.error('Zero Resultados')

cidades = bd['Cidade'].dropna().unique().tolist()
st.title('Geral por Praça')
with st.expander("Orientadoras"):
    for cidade in cidades:
        total_alunos = bd.query(f"Cidade == '{cidade}'")
        qtd_alunos_registrados = total_alunos.query("confirmacao_classificacao_orientadora == 'Não' or confirmacao_classificacao_orientadora == 'Sim'").shape[0]
        try:
            st.progress(qtd_alunos_registrados/total_alunos.shape[0], f'Status de Preenchimento das Orientadoras de ***{cidade}***: **{qtd_alunos_registrados}/{total_alunos.shape[0]}**')
        except ZeroDivisionError:
            st.error('Zero Resultados')
        st.divider()

with st.expander("Coordenadoras"):   
    for cidade in cidades:
        total_alunos = bd.query(f"Cidade == '{cidade}'")
        qtd_alunos_registrados = total_alunos.query("conclusao_classificacao_final == 'Sim'").shape[0]
        try:
            st.progress(qtd_alunos_registrados/total_alunos.shape[0], f'Status de Preenchimento das Orientadoras de ***{cidade}***: **{qtd_alunos_registrados}/{total_alunos.shape[0]}**')
        except ZeroDivisionError:
            st.error('Zero Resultados')
        st.divider()

st.title('Micro')
with st.expander("Orientadoras"):
    orientadoras_por_cidade = bd.groupby('Cidade')['Orientadora'].unique().to_dict()
    for cidade, orientadoras in orientadoras_por_cidade.items():
        st.divider()
        st.header(f'{cidade}')
        for orientadora in orientadoras:
            st.subheader(f'{orientadora}')
            alunos_orientadora_total = bd.query(f"Orientadora == '{orientadora}'")
            alunos_orientadora_total_registrados = alunos_orientadora_total.query("confirmacao_classificacao_orientadora == 'Não' or confirmacao_classificacao_orientadora == 'Sim'")
            try:
                st.progress(alunos_orientadora_total_registrados.shape[0]/alunos_orientadora_total.shape[0], f'Registrou: **{alunos_orientadora_total_registrados.shape[0]}/{alunos_orientadora_total.shape[0]}**')
            except ZeroDivisionError:
                st.error('Zero Resultados')


# Automatização da atualização de histórico
if 'registro_finalizado' not in st.session_state:
    st.session_state.registro_finalizado = False

if 'limpeza_finalizada' not in st.session_state:
    st.session_state.limpeza_finalizada = False

def finalizar():
    st.session_state.registro_finalizado = True
    st.session_state.limpeza_finalizada = True

st.button('Finalizar Classificação do Mês', on_click=finalizar)

if st.session_state.registro_finalizado:
    st.session_state.registro_finalizado = False
    bd = ler_sheets_cache('bd')
    df = ler_sheets('registro')
    df_modelo_historico = df.merge(bd[['RA', 'Cidade','Escola','Nota Matemática'
                                    ,'Nota Português','Nota História','Nota Geografia'
                                    ,'Nota Inglês','Nota Francês/Alemão e Outros'
                                    ,'Nota Espanhol','Nota Química','Nota Física'
                                    ,'Nota Biologia','Nota ENEM','Nota PU'
                                    ,'media_calibrada','Orientadora','Ano','Segmento']]
                                    , how='left', on='RA')
    registrar(df_modelo_historico, 'historico', 'RA', False)

if st.session_state.limpeza_finalizada:
    st.session_state.limpeza_finalizada = False

    esvazia_aba('registro')

    st.toast("Classificação do Mês Concluída!", icon="✅")
