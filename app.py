import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

url = "https://docs.google.com/spreadsheets/d/1wTaDcX3AnIeOLOgMFO4RxiGaT43oSfJOgfpgfGcWrZI/edit?gid=0#gid=0"

#ler planilha
conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read(spreadsheet=url, worksheet="sheet1", usecols=list(range(2)), ttl=1)
df = df.dropna(how='all')

st.dataframe(df)

with st.form(key='formulario'):
    id = st.number_input(label='ID',step=1)
    nome = st.text_input('Nome')

    submit_button = st.form_submit_button(label='Registrar')

    if submit_button:
        if not id or not nome:
            st.warning('Preencha o formuário')
            st.stop()
        else:
            df_insert = pd.DataFrame(
                [
                    {
                        'ID': id,
                        'nome': nome
                    }
                ]
            )
        updared_df = pd.concat([df, df_insert], ignore_index=True)
        
        conn.update(worksheet="sheet1", data=updared_df)

        st.success('Registrado com sucesso!')
