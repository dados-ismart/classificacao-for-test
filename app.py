import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
from time import sleep

#ler planilha
conn = st.connection("gsheets", type=GSheetsConnection)

def ler_sheets():
    df = conn.read(worksheet="Página1", ttl=1)
    return df

def classificar():
    return 'batata'

df = ler_sheets()
df

with st.form(key='formulario', clear_on_submit=True):
    
    col1, col2 = st.columns([2, 4])
    with col1:
        ra = st.number_input(label='RA',step=1)
    with col2:
        nome = st.text_input('Nome')

    submit_button = st.form_submit_button(label='Registrar')

    
    if submit_button:
        if not id or not nome:
            st.warning('Preencha o formuário')
            st.stop()
        else:
            for i in range(0, 3):
                try:
                    #inserir classificação
                    df = ler_sheets()
                    df_insert = pd.DataFrame([{'RA': ra, 'nome': nome, 'data_submit': datetime.now(), 'classificacao': classificar()}])
                    updared_df = pd.concat([df, df_insert], ignore_index=True)

                    conn.update(worksheet="Página1", data=updared_df)
                except:
                    st.error('erro ao registrar')
                    sleep(1)
                    continue

                #verificar
                sleep(3)
                df = ler_sheets()
                if not df.query(f'RA == {ra}').empty:
                    st.success('Registrado com sucesso!')
                    sleep(2)
                    break
                else:
                    st.error('erro ao registrar, aluno não encontrado na base')
                    sleep(1)
                    continue
        st.rerun()
        
      