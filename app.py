import streamlit as st
import pandas as pd
import openpyxl as xl
#------------------------------------------------------------------------------
# Configuração da páginas
st.set_page_config(layout='wide',page_icon='🦷',page_title="Agenda",initial_sidebar_state='collapsed',menu_items=None)
st.title('📘 🦷 Agenda - Consultório Dr. Fulano',anchor=False)
st.markdown('--------')

#------------------------------------------------------------------------------
# Dados

tabela1 = pd.DataFrame({"Data":["today"],"Paciente":['Paciente 1','Paciente 2','Paciente 3']})
tabela = pd.read_excel('Agenda.xlsx')
df = pd.DataFrame(tabela)
df.sort_values("Data")
df['Data'] = df['Data'].dt.date
pd.to_datetime(df['Data'],format="DD/MM/YYYY")
df['Hora'] = df['Hora'].astype(str)
pacientes = pd.read_excel("Pacientes.xlsx")
dfpaciente = pd.DataFrame(pacientes)
#------------------------------------------------------------------------------
# Layout
col1, col2 = st.columns(2)

#------------------------------------------------------------------------------
# Barra Lateral
st.sidebar.image('paciente.png',width=200,caption="",use_column_width=True)
st.sidebar.markdown('---')
st.sidebar.title("Cadastrar Paciente",anchor=False)

nome = st.sidebar.text_input("Nome","")
telefone = st.sidebar.text_input("Telefone")

#------------------------------------------------------------------------------
# Barra lateral
with col1:
    st.subheader('Agendar',anchor=False)
    entrada_data = st.date_input("Data", 'today', format="DD/MM/YYYY")
    entrada_paciente = st.selectbox("Paciente",dfpaciente['Pacientes'].unique()) 
    entrada_procedimento = st.selectbox("Procedimento",df['Procedimento'].unique())
    entrada_hora = st.time_input("Horário")
with col2:
    st.subheader('Agenda do dia',anchor=False)
    dff= df.query("Data == @entrada_data")
    st.table(dff)
    
#------------------------------------------------------------------------------
# Adicionar na agenda
with col1:
    if st.button("Agendar"):
    # Abra o arquivo do Excel
        planilha = xl.load_workbook("Agenda.xlsx")
        planilha = planilha.active

        nova_linha = [entrada_data, entrada_paciente,entrada_procedimento, entrada_hora]

        planilha.append(nova_linha)

        planilha.parent.save("Agenda.xlsx")
        
        st.success("Agendamento salvo!")

#------------------------------------------------------------------------------
if st.sidebar.button("Salvar"):
    # Abra o arquivo do Excel
    planilha = xl.load_workbook("Pacientes.xlsx")
    planilha = planilha.active

    nova_linha = [nome,telefone]

    planilha.append(nova_linha)

    planilha.parent.save("Pacientes.xlsx")
    
    st.sidebar.success("Cadastro salvo!")
#------------------------------------------------------------------------------

st.markdown('--------')

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

#------------------------------------------------------------------------------

