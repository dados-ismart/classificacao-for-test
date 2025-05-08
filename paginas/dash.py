import streamlit as st
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
from time import sleep
import pytz
from paginas.funcoes import ler_sheets

fuso_horario = pytz.timezone('America/Sao_Paulo')
conn = st.connection("gsheets", type=GSheetsConnection)

df = ler_sheets('registro')
df['RA'] = df['RA'].astype(int)
bd = ler_sheets('bd')
bd['RA'] = bd['RA'].astype(int)

#filtros
bd_segmentado = bd.query("apoio_registro_final != 'Sim'")
bd_segmentado = bd_segmentado.query("apoio_registro == 'Sim' or apoio_registro == 'Não'")
# filtros bd
col1, col2, col3, col4 = st.columns(4)
# Aplique os filtros
valores_segmento = col1.multiselect("Filtro de Segmento", bd_segmentado['Segmento'].unique())
if valores_segmento:
    bd_segmentado = bd_segmentado.query(f"Segmento in {valores_segmento}")
valores_escola = col2.multiselect("Filtro de Escola", bd_segmentado['Escola'].unique())
if valores_escola:
    bd_segmentado = bd_segmentado.query(f"Escola in {valores_escola}")
valores_ano = col3.multiselect("Filtro de Ano", bd_segmentado['Ano'].unique())
if valores_ano:
    bd_segmentado = bd_segmentado.query(f"Ano in {valores_ano}")
selecao_orientadora = col4.multiselect("Filtro Orientadora", bd_segmentado['Orientadora'].unique())
if selecao_orientadora:
    bd_segmentado = bd_segmentado.query(f"Orientadora in {selecao_orientadora}")
st.divider()

df = df.query('confirmacao_classificacao_coordenacao != "Sim" and confirmacao_classificacao_coordenacao != "Não" and confirmacao_classificacao_orientadora == "Sim" or confirmacao_classificacao_orientadora == "Não"')
df = df[df['RA'].isin(bd_segmentado['RA'])]

df_completo = df.merge(bd[['RA', 'Orientadora', 'Segmento', 'Escola', 'Cidade', 'media_calibrada','Nota Matemática', 'Nota Português', 'Nota História', 'Nota Geografia', 
                'Nota Inglês', 'Nota Francês/Alemão e Outros', 'Nota Espanhol', 'Nota Química', 
                'Nota Física', 'Nota Biologia', 'Nota ENEM', 'Nota PU']]
                , how='left', on='RA')
df_completo.sort_values(by=['Orientadora', 'Segmento', 'nome'])


#visualização
st.title('Visualização dos Dados')
st.dataframe(df_completo)
