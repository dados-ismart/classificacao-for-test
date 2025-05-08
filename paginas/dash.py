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
bd_segmentado = bd
col1, col2, col3, col4 = st.columns(4)
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
df_completo = df_completo[['RA', 'nome','data_submit','Orientadora', 'Segmento', 'Escola', 'Cidade','resposta_argumentacao','resposta_rotina_estudos',
                           'resposta_faltas','resposta_atividades_extracurriculares','resposta_respeita_escola',
                           'resposta_atividades_obrigatorias_ismart','resposta_colaboracao',
                           'resposta_atividades_nao_obrigatorias_ismart','resposta_networking','resposta_proatividade',
                           'resposta_questoes_psiquicas','resposta_questoes_familiares','resposta_questoes_saude',
                           'resposta_ideacao_suicida','resposta_adaptacao_projeto','resposta_seguranca_profissional',
                           'resposta_curso_apoiado','resposta_nota_condizente','classificacao_automatica','motivo_classificao_automatica',
                           'confirmacao_classificacao_orientadora','nova_classificacao_orientadora','novo_motivo_classificacao_orientadora',
                           'nova_justificativa_classificacao_orientadora','reversao','descricao_caso','plano_intervencao','tier',
                           'confirmacao_classificacao_coordenacao','justificativa_classificacao_coord','classificacao_final',
                           'motivo_final','confirmacao_classificacao_final','media_calibrada','Nota Matemática', 'Nota Português', 
                           'Nota História', 'Nota Geografia', 'Nota Inglês', 'Nota Francês/Alemão e Outros', 'Nota Espanhol', 'Nota Química', 
                           'Nota Física', 'Nota Biologia', 'Nota ENEM', 'Nota PU']]

#visualização
st.title('Visualização dos Dados')
st.dataframe(df, column_config={
                "justificativa_classificacao_coord": st.column_config.TextColumn(
                    "Justificativa da Coordenadora",
                    required=False
                ),
                "RA": st.column_config.TextColumn(
                    "RA",
                    required=False
                ),
                "nome": st.column_config.TextColumn(
                    "Nome",
                    required=False
                ),
                "Orientadora": st.column_config.TextColumn(
                    "Orientadora",
                    required=False
                ),
                "classificacao_final": st.column_config.SelectboxColumn(
                    "Classificação Final",
                    required=False
                ),
                "motivo_final": st.column_config.TextColumn(
                    "Motivo Classificação Final",
                    required=False
                ),
                "classificacao_automatica": st.column_config.TextColumn(
                    "Classificação Automatica",
                    required=False
                ),
                "motivo_classificao_automatica": st.column_config.TextColumn(
                    "Motivo Classificação Automatica",
                    required=False
                ),
                "confirmacao_classificacao_orientadora": st.column_config.TextColumn(
                    "Orientadora Confirmou a classificação Automatica?",
                    required=False
                ),
                "nova_classificacao_orientadora": st.column_config.TextColumn(
                    "Classificação da Orientadora",
                    required=False
                ),
                "novo_motivo_classificacao_orientadora": st.column_config.TextColumn(
                    "Motivo da Orientadora",
                    required=False
                ),
                "nova_justificativa_classificacao_orientadora": st.column_config.TextColumn(
                    "Justificativa da Orientadora",
                    required=False
                ),
                "reversao": st.column_config.TextColumn(
                    "Reversão",
                    required=False
                ),
                "descricao_caso": st.column_config.TextColumn(
                    "Descrição do Caso",
                    required=False
                ),
                "plano_intervencao": st.column_config.TextColumn(
                    "Plano de Intervenção",
                    required=False
                ),
                "tier": st.column_config.TextColumn(
                    "Tier",
                    required=False
                ),
                "resposta_argumentacao": st.column_config.TextColumn(
                    "Resposta - Nivel de Argumentação/Interações",
                    required=False
                ),
                "resposta_rotina_estudos": st.column_config.TextColumn(
                    "Resposta - Rotina de Estudos Adequada?",
                    required=False
                ),
                "resposta_atividades_extracurriculares": st.column_config.TextColumn(
                    "Resposta - Atividades Extracurriculares",
                    required=False
                ),
                "resposta_faltas": st.column_config.TextColumn(
                    "Resposta - Número de Faltas comprometentes?",
                    required=False
                ),
                "resposta_respeita_escola": st.column_config.TextColumn(
                    "Resposta - Respeita Normas Escolares?",
                    required=False
                ),
                "resposta_atividades_obrigatorias_ismart": st.column_config.TextColumn(
                    "Resposta - Participa das Atividades Obrigatórias?",
                    required=False
                ),
                "resposta_colaboracao": st.column_config.TextColumn(
                    "Resposta - É Colaborativo Com Amigos?",
                    required=False
                ),
                "resposta_atividades_nao_obrigatorias_ismart": st.column_config.TextColumn(
                    "Resposta - Participa das Atividades Não Obrigatórias?",
                    required=False
                ),
                "resposta_networking": st.column_config.TextColumn(
                    "Resposta - Cultiva Parcerias?",
                    required=False
                ),
                "resposta_proatividade": st.column_config.TextColumn(
                    "Resposta - É Proativo?",
                    required=False
                ),
                "resposta_questoes_psiquicas": st.column_config.TextColumn(
                    "Resposta - Apresenta Questões Psíquicas de impacto?",
                    required=False
                ),
                "resposta_questoes_familiares": st.column_config.TextColumn(
                    "Resposta - Apresenta Questões Familiares de impacto?",
                    required=False
                ),
                "resposta_questoes_saude": st.column_config.TextColumn(
                    "Resposta - Apresenta Questões Saúde de impacto?",
                    required=False
                ),
                "resposta_ideacao_suicida": st.column_config.TextColumn(
                    "Resposta - Apresenta Ideação Suicida?",
                    required=False
                ),
                "resposta_adaptacao_projeto": st.column_config.TextColumn(
                    "Resposta - Se Adaptou ao Projeto?",
                    required=False
                ),
                "resposta_seguranca_profissional": st.column_config.TextColumn(
                    "Resposta - Tem Segurança Proficional?",
                    required=False
                ),
                "resposta_curso_apoiado": st.column_config.TextColumn(
                    "Resposta - Deseja Curso Apoiado?",
                    required=False
                ),
                "resposta_nota_condizente": st.column_config.TextColumn(
                    "Resposta - Nota Condizente Com o Curso Desejado?",
                    required=False
                ),
                "Segmento": st.column_config.TextColumn(
                    "Segmento",
                    required=False
                ),
                "confirmacao_classificacao_coordenacao": st.column_config.TextColumn(
                    "Coordenação Confirmou Classificação da Orientadora?",
                    required=False
                ),
                "confirmacao_classificacao_final": st.column_config.TextColumn(
                    "Classificação Final do Mês Concluida?",
                    required=False
                ),
                "Nota Matemática": st.column_config.NumberColumn(
                    "Nota Matemática",
                    required=False
                ),
                "Nota Português": st.column_config.NumberColumn(
                    "Nota Português",
                    required=False
                ),
                "Nota História": st.column_config.NumberColumn(
                    "Nota História",
                    required=False
                ),
                "Nota Geografia": st.column_config.NumberColumn(
                    "Nota Geografia",
                    required=False
                ),
                "Nota Inglês": st.column_config.NumberColumn(
                    "Nota Inglês",
                    required=False
                ),
                "Nota Francês/Alemão e Outros": st.column_config.NumberColumn(
                    "Nota Francês/Alemão e Outros",
                    required=False
                ),
                "Nota Espanhol": st.column_config.NumberColumn(
                    "Nota Espanhol",
                    required=False
                ),
                "Nota Química": st.column_config.NumberColumn(
                    "Nota Química",                        required=False
                ),        
                "Nota Física": st.column_config.NumberColumn(
                    "Nota Física",
                    required=False
                ),
                "Nota Biologia": st.column_config.NumberColumn(
                    "Nota Biologia",
                    required=False
                ),
                "Nota ENEM": st.column_config.NumberColumn(
                    "Nota ENEM",
                    required=False
                ),
                "Nota PU": st.column_config.NumberColumn(
                    "Nota PU",
                    required=False
                ),                          
                "media_calibrada": st.column_config.NumberColumn(
                    "Média Calibrada",
                    required=False
                ),                          
            })
