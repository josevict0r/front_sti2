import streamlit as st
import requests

BASE_URL = "https://sti2-production.up.railway.app/"

with st.expander("Sobre o sistema", expanded=True):
    st.markdown('''
# Tutor Inteligente de Programação em Python

Este sistema tem como intenção guiar o usuário em uma jornada de aprendizado orientada a exercícios, capacitando-o usar lógica de programação fluentemente, manipular estruturas de dados, das mais simples às mais complexas, proporcionando ajuda específica para as dificuldades que apareçam pelo caminho.

* O Sistema ainda está em fase Beta, precisa de ajustes na submissão de respostas que não foram realizadas ainda por falta do recurso de tempo;

* Além dos ajustes indispensáveis para um fluxo ideal do sistema, há polimentos que podem melhorar o que já funciona como: expansão do banco de questôes, login de usuário, planejamento de uma trilha de aprendizado com escolha de temática pelo aluno, etc.

### Teste os módulos de Feedback, Ver resposta e Dicas! Todos integrados com a LLM do Google Gemini!                 
''')

st.title("Tutor Inteligente de Programação")

st.sidebar.header("Ações")

# Exibir pontuação
aluno_id = st.sidebar.number_input("ID do Aluno", min_value=1, step=1)

if st.sidebar.button("Ver Pontuação Total"):
    res = requests.get(f"{BASE_URL}/alunos/{aluno_id}/pontuacao_total")
    if res.status_code == 200:
        dados = res.json()
        st.success(f"Pontuação total: {dados['pontuacao_total']} pontos")
    else:
        st.error("Aluno não encontrado")

# Submeter código para avaliação

exercicio_id = st.number_input("Selecione o Exercício:", min_value=1, step=1)

res = requests.get(f"{BASE_URL}/exercicios/{exercicio_id}")
enun=res.json()
enunciado_id = st.markdown(f""" ### Exercício {exercicio_id}: {enun['enunciado']}

                            """
                           )

codigo = st.text_area("Cole seu código aqui:", height=200)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Ver Dicas do Exercício"):
        params = {
            "exercicio_id": exercicio_id,
            'codigo': "enumere dicas curtas para resolver esse exercício"
        }
        res = requests.post(f"{BASE_URL}/alunos/{aluno_id}/feedback", params=params)
        if res.status_code == 200:
            dicas = res.json()
            if dicas:
                st.markdown("### 📌 Dicas:")
                st.info(dicas["feedback"])                
        else:
            try:
                erro = res.json()["detail"]
                st.error(erro)
            except:
                st.error("Erro inesperado no servidor")

with col2:
    if st.button("Obter Feedback da IA"):
        params = {
            "exercicio_id": exercicio_id,
            "codigo": codigo
        }
        res = requests.post(f"{BASE_URL}/alunos/{aluno_id}/feedback", params=params)
        if res.status_code == 200:
            r = res.json()
            st.markdown("### 💡 Feedback:")
            st.info(r["feedback"])
        else:
            try:
                erro = res.json()["detail"]
                st.error(erro)
            except:
                st.error("Erro inesperado no servidor")
    if st.button("Desistir e Ver Resposta"):
        params = {
            "codigo": codigo
        }
        res = requests.post(
            f"{BASE_URL}/alunos/{aluno_id}/exercicios/{exercicio_id}/resolver",
            params=params
        )
        if res.status_code == 200:
            r = res.json()
            print(r)
            st.markdown("### ✅ Solução:")
            st.info(r["resolucao_llm"])
        else:
            try:
                erro = res.json()["detail"]
                st.error(erro)
            except:
                st.error("Erro inesperado no servidor")



with col3:
    if st.button("Enviar Resposta Final"):
        payload = {"aluno_id": aluno_id, "exercicio_id": exercicio_id, "codigo": codigo}
        res = requests.post(f"{BASE_URL}/tentativas/avaliar", json=payload)
        if res.status_code == 200:
            r = res.json()
            st.success(f"Passou nos testes? {'Sim' if r['passou_testes'] else 'Não'}")
            st.info(f"Pontos ganhos: {r['pontos_ganhos']}")
        else:
            try:
                erro = res.json()["detail"]
                st.error(erro)
            except:
                st.error("Erro inesperado no servidor")
st.write('Planejado e Realizado por: Gabriela Tenório, Laís Souza e José Victor.')

