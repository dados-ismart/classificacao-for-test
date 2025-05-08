import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
from time import sleep
import pytz

def ler_sheets(pagina):
    conn = st.connection("gsheets", type=GSheetsConnection)
    for i in range(0, 10):
        try:
            df = conn.read(worksheet=pagina, ttl=1)
            return df
        except:
            sleep(3)
            pass
    st.error('Erro ao conectar com o sheets')
    if st.button('Tentar novamente'):
        st.rerun()
    st.stop()
