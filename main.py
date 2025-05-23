import streamlit as st
from paginas.funcoes import ler_sheets_cache


def check_password():
    def password_entered():
        if (
            st.session_state["username"] in st.secrets["passwords"]
            and st.session_state["password"] == st.secrets["passwords"][st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            st.session_state["authenticated_username"] = st.session_state["username"]
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Usuário", key="username")
        st.text_input("Senha", type="password", key="password", on_change=password_entered)
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Usuário", key="username")
        st.text_input("Senha", type="password", key="password", on_change=password_entered)
        st.error("😕 Usuário desconhecido ou senha incorreta.")
        return False
    else:
        return True


def login_page():
    st.title("Login")
    if check_password():
        st.success(f"Bem-vindo, {st.session_state['authenticated_username']}!")
        st.rerun()  # Força a atualização para mostrar as páginas após login

def logout():
    st.session_state["password_correct"] = False
    st.session_state["authenticated_username"] = None
    st.rerun()

logout_page = st.Page(logout, title="Sair")

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

st.set_page_config(layout="wide")

# --- NAVIGATION SETUP [WITH SECTIONS]---
if st.session_state.get("password_correct"):
    df_login = ler_sheets_cache('login')
    if df_login.query(f'login == "{st.session_state["authenticated_username"]}"')["cargo"].iloc[0] == "coordenação":
        pg = st.navigation({
            "Paginas": [pagina_inicial_coordenadora, dash, dash_status_preenchimento],
        })    
    else:
        pg = st.navigation({
            "Paginas": [pagina_inicial_orientadora, dash, dash_status_preenchimento],
        })  
else:
    pg = st.navigation([st.Page(login_page, title="Login")])
# --- RUN NAVIGATION ---
pg.run()
