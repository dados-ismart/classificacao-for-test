import streamlit as st
from paginas.funcoes import ler_sheets_cache, check_microsoft_login
import time
from PIL import Image

logo = Image.open('imagens/logo_ismart.png')

st.set_page_config(page_title='Ismart - Dashboard EB',
                   page_icon=logo,
                   layout="wide",
                   initial_sidebar_state="collapsed")

st.logo(logo, icon_image=logo)

def logout():
    """Realiza logout da conta Microsoft e limpa a sessão."""
    if st.user.is_logged_in:
        st.logout()
    
    # Limpa variáveis da sessão
    keys_to_remove = ["auth_success_shown", "autenticado"]
    for key in keys_to_remove:
        if key in st.session_state:
            del st.session_state[key]
    
    st.toast("🔒 Você foi desconectado com sucesso!", icon="🔒")
    time.sleep(0.5)

# --- PAGE SETUP ---
pagina_inicial_coordenadora = st.Page(
    "paginas/coordenadoras.py",
    title= "Classificação",
    icon= "⚖️",
    default=True,
)

pagina_inicial_orientadora = st.Page(
    "paginas/orientadoras.py",
    title= "Classificação",
    icon= "⚖️",
    default=True,
)

dash = st.Page(
    "paginas/dash.py",
    title= "Visualização",
    icon= "📊"
)

dash_status_preenchimento = st.Page(
    "paginas/dash_status_preenchimento.py",
    title= "Status de Preenchimento",
    icon= "🕔"
)
        
# --- NAVIGATION SETUP [WITH SECTIONS]---
if check_microsoft_login() is not None:
    if "auth_success_shown" not in st.session_state:
        st.toast("Autenticação realizada com sucesso!", icon="✅")
        st.session_state.auth_success_shown = True 
    df_login = ler_sheets_cache('login')
    if df_login.query(f'email == "{check_microsoft_login()}"')["cargo"].iloc[0] == "coordenação":
        pg = st.navigation({
            "Páginas": [pagina_inicial_coordenadora, dash, dash_status_preenchimento],
        })    
    else:
        pg = st.navigation({
            "Páginas": [pagina_inicial_orientadora, dash, dash_status_preenchimento],
        })  
else:
    st.stop()
# --- RUN NAVIGATION ---
pg.run()
