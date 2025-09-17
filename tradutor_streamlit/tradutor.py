import streamlit as st
import pandas as pd

# --- LÓGICA ORIGINAL DO SEU SCRIPT (QUASE INALTERADA) ---

dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
horarios_gerais = [
    "07:00 - 08:00", "08:00 - 09:00", "09:00 - 10:00", "10:00 - 11:00", "11:00 - 12:00",
    "13:00 - 14:00", "14:00 - 15:00", "15:00 - 16:00", "16:00 - 17:00", "17:00 - 18:00",
    "18:00 - 19:00", "19:00 - 20:00", "20:00 - 21:00", "21:00 - 22:00", "22:00 - 23:00"
]

# A grade agora será gerenciada pelo Streamlit para persistir entre as interações
# Não precisamos mais da inicialização global aqui.

def adicionar_na_grade(grade, turno, dia, tempo, nome):
    offset = 0
    if turno == 'T':
        offset = 5
    elif turno == 'N':
        offset = 10

    tempo_real = offset + tempo
    if 0 <= dia < 5 and 0 <= tempo_real < 15:
        grade[dia][tempo_real] = nome
    return grade

def processar_codigo(grade, codigo, nome):
    if len(codigo) < 3:
        return grade

    i = 0
    while i < len(codigo) and codigo[i] in '23456': # Corrigido para aceitar os dias da semana
        i += 1

    dias = codigo[:i]
    turno = codigo[i].upper() # Garante que o turno seja maiúsculo
    tempos = codigo[i+1:]

    for d in dias:
        dia_num = int(d)
        if 2 <= dia_num <= 6:
            dia_index = dia_num - 2
        else:
            continue

        for t in tempos:
            if t.isdigit():
                tempo_index = int(t) - 1
                if 0 <= tempo_index < 5:
                    grade = adicionar_na_grade(grade, turno, dia_index, tempo_index, nome)
    return grade

# --- INTERFACE WEB COM STREAMLIT ---

st.set_page_config(layout="wide") # Deixa a página mais larga
st.title("📅Meu horário")


# Inicializa o estado da sessão para guardar a lista de matérias
if 'materias' not in st.session_state:
    st.session_state.materias = []

# Formulário para adicionar novas matérias
st.header("Adicionar Nova Matéria")
with st.form("nova_materia_form", clear_on_submit=True):
    nome_materia = st.text_input("Nome da Matéria (Ex: Cálculo I)")
    codigo_horario = st.text_input("Código de Horário (Ex: 35T12)")
    
    submitted = st.form_submit_button("Adicionar Matéria")
    if submitted and nome_materia and codigo_horario:
        st.session_state.materias.append({"nome": nome_materia, "codigo": codigo_horario})
        st.success(f"Matéria '{nome_materia}' adicionada!")

# Botão para limpar a grade
if st.button("Limpar Grade"):
    st.session_state.materias = []
    st.experimental_rerun()

# Lógica para processar e exibir a grade
if st.session_state.materias:
    st.header("Sua Grade de Horários")

    # Inicializa uma grade vazia a cada atualização
    grade_atual = [[None for _ in range(15)] for _ in range(5)]

    # Processa todas as matérias adicionadas
    for materia in st.session_state.materias:
        grade_atual = processar_codigo(grade_atual, materia["codigo"], materia["nome"])

    # Converte a lista de listas em um DataFrame do Pandas para exibição
    # A transposição (.T) é necessária para que os dias fiquem nas colunas e os horários nas linhas
    df = pd.DataFrame(grade_atual).T 
    df.columns = dias_semana
    df.index = horarios_gerais

    # Substitui os valores None por uma string vazia para uma melhor visualização
    df.fillna("-", inplace=True)
    
    # Exibe o DataFrame como uma tabela na página
    st.dataframe(df, height=562, use_container_width=True)
    
    # Mostra a lista de matérias cadastradas
    st.subheader("Matérias Cadastradas")
    for materia in st.session_state.materias:
        st.write(f"- **{materia['nome']}**: `{materia['codigo']}`")

else:

    st.info("Adicione uma matéria para começar a montar sua grade.")
