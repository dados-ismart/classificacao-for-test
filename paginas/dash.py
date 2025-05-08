import streamlit as st
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
from time import sleep
import pytz
from app import ler_sheets

fuso_horario = pytz.timezone('America/Sao_Paulo')
conn = st.connection("gsheets", type=GSheetsConnection)

df = ler_sheets('registro')

st.success('dash')
st.dataframe(df)