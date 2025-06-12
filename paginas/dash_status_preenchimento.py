import streamlit as st
import pandas as pd
import pytz
from paginas.funcoes import ler_sheets, ler_sheets_cache, registrar, esvazia_aba, enviar_email
from time import sleep

# importar dados
df = ler_sheets('registro')
bd = ler_sheets_cache('bd')
df_login = ler_sheets_cache('login')
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
st.divider()
@st.dialog("Insira a senha e confirme para reiniciar a classificação")
def input_popup():
    with st.form(key='confirmacao_classificacao_mes'):
        senha = st.text_input("Senha")
        submit_button = st.form_submit_button(label='Confirmar')
    if submit_button:
        st.session_state.senha = senha
        st.rerun()
        
if st.button("Finalizar Classificação do Mês"):
    input_popup()

if 'registro_finalizado' not in st.session_state:
    st.session_state.registro_finalizado = False

if 'limpeza_finalizada' not in st.session_state:
    st.session_state.limpeza_finalizada = False

if 'senha' in st.session_state:
    if st.session_state.senha == 'User#1340':
        st.session_state.registro_finalizado = True
        st.session_state.limpeza_finalizada = True

if st.session_state.registro_finalizado:
    st.session_state.registro_finalizado = False
    del st.session_state["senha"]
    bd = ler_sheets_cache('bd')
    df = ler_sheets('registro')
    df_insert = df.merge(bd[['RA', 'Cidade','Escola','Nota Matemática'
                                    ,'Nota Português','Nota História','Nota Geografia'
                                    ,'Nota Inglês','Nota Francês/Alemão e Outros'
                                    ,'Nota Espanhol','Nota Química','Nota Física'
                                    ,'Nota Biologia','Nota ENEM','Nota PU'
                                    ,'media_calibrada','Orientadora','Ano','Segmento']]
                                    , how='left', on='RA')
    registrar(df_insert, 'historico', 'RA', False)

if st.session_state.limpeza_finalizada:
    st.session_state.limpeza_finalizada = False

    esvazia_aba('registro')

    st.toast("Classificação do Mês Concluída!", icon="✅")
    sleep(2)
    st.rerun()
        
# ENVIO E E-MAIL
@st.dialog("Insira a senha e confirme para enviar")
def input_popup_email():
    with st.form(key='confirmacao_classificacao_mes'):
        senha = st.text_input("Senha")
        submit_button = st.form_submit_button(label='Confirmar')
    if submit_button:
        st.session_state.senha_email = senha
        st.rerun()
        
if st.button("Enviar E-mail de lembrete"):
    input_popup_email()

if 'enviar_email' not in st.session_state:
    st.session_state.enviar_email = False

if 'senha' in st.session_state:
    if st.session_state.senha_email == 'User#1340':
        st.session_state.enviar_email = True

if st.session_state.enviar_email:
    st.session_state.enviar_email = False
    del st.session_state["senha"]

    try:
        # 1. Contar o total de alunos por orientadora
        total_por_orientadora = bd.groupby('Orientadora').size().rename('Total')

        # 2. Filtrar apenas os alunos já registrados e contar por orientadora
        registrados_df = bd.query("confirmacao_classificacao_orientadora == 'Sim' or confirmacao_classificacao_orientadora == 'Não'")
        registrados_por_orientadora = registrados_df.groupby('Orientadora').size().rename('Registrados')

        # 3. Combinar os totais e os registrados em um único DataFrame
        # O .fillna(0) é crucial para orientadoras que não registraram ninguém
        progresso_df = pd.concat([total_por_orientadora, registrados_por_orientadora], axis=1).fillna(0)
        progresso_df['Registrados'] = progresso_df['Registrados'].astype(int)
        # 4. Filtrar apenas as orientadoras onde o registrado é menor que o total
        incompletas_df = progresso_df[progresso_df['Registrados'] < progresso_df['Total']]

        if incompletas_df.empty:
            st.success("🎉 Todas as orientadoras completaram o registro de seus alunos!")
        else:
            incompletas_df = incompletas_df.merge(df_login[['Orientadora', 'email']], how='left', on='Orientadora')
            email_list = incompletas_df['email'].to_list()
            
            assunto = 'Preenchimento da classificação'
            mensagem = '''
            Olá, tudo bem?

            Este é um lembrete de que a tarefa de classificação dos alunos referente a este mês ainda consta como pendente em nosso sistema.

            Sua avaliação é fundamental para mantermos os registros atualizados. Para concluir, por favor, acesse o sistema através do link abaixo:

            Links separados por praça:

            •	🟣 BH: Classificação Praça BH - https://classificacao-ismart-bh.streamlit.app/
            •	🔵 RJ: Classificação Praça RJ - https://classificacao-ismart-rj.streamlit.app/
            •	🟡 SJC: Classificação Praça SJC - https://classificacao-ismart-sjc.streamlit.app/
            •	🟢 SP: Classificação Praça SP - https://classificacao-ismart-sp.streamlit.app/
            
            Só lembrando as categorias de avaliação (baseadas apenas nas notas):

            ❌ Crítico Escolar - 1 nota com diferença menor que 1 ponto da média ou mais de 2 notas abaixo da média
            ⚠️ Atenção Escolar - até 2 notas abaixo da média
            ➖ Mediano Escolar - nenhuma nota abaixo da média
            🔶 Pré-Destaque Escolar - mais de 2 notas com diferença maior que 2 pontos da média e pelo menos 1 com diferença maior que 1 ponto da média
            ⭐ Destaque Escolar - 5 notas com diferença maior que 2 pontos da média


            Agradecemos sua atenção e colaboração.

            Atenciosamente,

            Equipe de Dados

            ---
            Este é um e-mail automático. Por favor, não responda diretamente.
            '''
            enviar_email(email_list, assunto, mensagem)
    except Exception as e:
        st.error(f"Ocorreu um erro ao processar os dados: {e}")
