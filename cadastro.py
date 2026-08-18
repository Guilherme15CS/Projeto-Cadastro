# Fazer Basico da Inferface feito
# Adicionar Opções do cadastro feito
# Fazer ligação com o Banco de Dados feito
    #Conectar com o banco de Dados feito
    #Conseguir Interagir com o Banco de Dados feito
# Integrar com o Excel

# Voltar na parte de adicionar cadastro para resolver formatação de dados(CPF, Data de Nascimento)

#Importando as bibliotecas necessarias
import streamlit as st
import pymysql
import pandas as pd
from sqlalchemy import create_engine
import datetime


def pagina_inicial():
    st.session_state.proxima_aba = "Visualizar"  # faz a "solicitação de troca de pagina"
    st.rerun() # Roda o codigo denovo para fazer a ação acima


def conectar():
    return pymysql.connect(
        host=st.secrets["mysql"]["host"],
        port=st.secrets["mysql"]["port"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"],
        ssl={"ca": "ca.pem"}
    )


# Configurações iniciais da pagina 
st.set_page_config(page_title="Sistema de Cadastro", page_icon="🗂️" , layout="wide")

# Obriga o site a começar com a tela de visualizar a tabela
if "opcoes" not in st.session_state:
    st.session_state.opcoes = "Visualizar"

# Faz voltar para a tela que for selecionada na parte do codigo onde a variavel session_state.proxima_abo for chamada
if "proxima_aba" in st.session_state:
    st.session_state.opcoes = st.session_state.proxima_aba
    del st.session_state.proxima_aba

data_minima = datetime.date(1900, 1, 1)
#data_maxima = datetime.date.today().year

# A engine é uma ligação direta do Python com o MySQl sem que acontece nehum erro de "entendimento" entre eles 
engine = create_engine(
    f'mysql+pymysql://{st.secrets["mysql"]["user"]}:{st.secrets["mysql"]["password"]}'
    f'@{st.secrets["mysql"]["host"]}:{st.secrets["mysql"]["port"]}/{st.secrets["mysql"]["database"]}'
    f'?ssl_ca=ca.pem')


# Conexão com o Banco de Dados com tratamento de erro caso ele não esteja funcionando
try:
    conexao = conectar()
    conexao.close()
except Exception as e:
    #print("Banco não Conectado")
    st.title("O Banco de Dados não está funcionando")
    st.error(f"Erro detalhado {e}")
    exit()


#Adiciona Um Titulo na pagina inicial
st.header("Sistema de Cadastro", divider="gray", text_alignment="center")



#Cria uma barra lateral com as opções de controle do cadastro
st.sidebar.title("Menu", text_alignment='left')
opcoes = st.sidebar.radio(
    "O que deseja fazer?",
    ["Visualizar", "Adicionar", "Remover", "Atualizar"],
    key="opcoes" )

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=
#OPÇÃO VISUALIZAR
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


#Caso a opção "Visualizar" for selecionada irá acontecer isso
if opcoes == "Visualizar":
    #st.title("Você apertou em Visualizar", text_alignment= "center")
    # Abrindo o Banco de Dados 
    conexao = conectar()

    # Fazendo uma variavel com o camndo de selecionar todos os dados com o auxilio de intepretação da engine
    comando = pd.read_sql("SELECT * FROM informações ORDER BY Id", engine)

    # Comando para aparecer no site como uma tabela (tipo Excel)
    st.table(comando)

    conexao.close()

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=
#OPÇÃO ADICIONAR
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Caso a opção "Adicionar" for selecionada irá acontecer isso
elif opcoes == "Adicionar":

    # Abrindo o Banco de Dados
    conexao = conectar()
    cursor = conexao.cursor()
    
    #st.title("Você apertou em Adicionar", text_alignment= "center")
    #Text input Cpf, Nome, Cidade
    #Selectbox para Situação, Estado Civil 
    #TESTAR Data input Para Nascimento
    #Radio para Time, Sexo
    #Se sim para time aparce campo para escrever, senao não aparece nada
    #Se empregado Aparecer campo de Emprego
    #Se estudante aparecer outro Selectbox Para Escola ou Faculdade

    # Cria duas coluna onde vai separar tudo por elas na esquerda e diteita
    col1, col2 = st.columns(2, gap="medium")

    # Criação de uma variável para cada campo para adicionar na ligação com o BD e salvar no site

    # Uso da coluna 1 com os seguintes dados CPF, NOME, SEXO, DATA DE NASCIEMNTO
    with col1:
        add_CPF = st.text_input("CPF (apenas números)")

        # Fazendo a Formatação do CPF para facilitar o cadastro

        cpf_formatado = f"{add_CPF[:3]}.{add_CPF[3:6]}.{add_CPF[6:9]}-{add_CPF[9:]}"

        add_CPF = cpf_formatado

        add_Nome =st.text_input("Nome")


        sexo = st.radio("Sexo",
                ["Masculino", "Feminino"])
        if sexo == "Masculino":
            add_Sexo = "M"
        elif sexo == "Feminino":
            add_Sexo = "F"

        
        add_Data = st.date_input("Data de Nascimento", value=None, min_value=data_minima, max_value="today", format="DD/MM/YYYY")


    # Uso da coluna 2 com os seguintes dados SITUAÇÃO CIVIL, ESTADO CIVIL, CIDADE, TIME
    with col2:
        add_Situ = Situ = st.selectbox("Situação Civil", options=["Empregado(a)", "Desempregado(a)", "Estudante", "Aposentado(a)"])


        if Situ == "Estudante":
            Estudante_Situ = st.radio("Estudante",
            ["Escola", "Faculdade"]) 
            add_Situ = f"{Situ}/{Estudante_Situ}" 
           
        elif Situ == "Empregado(a)":
            Empregado_Situ = st.text_input("Digite seu cargo")
            add_Situ = f"{Situ}/{Empregado_Situ}"

        

        add_Esta = st.selectbox("Estado Civil", options=["Solteiro(a)", "Casado(a)", "Divorciado(a)", "Viúvo(a)", "Namoradno"])


        add_Cida = st.text_input("Cidade onde mora")


        Torce = st.radio("Torce para algum time?",
                ["Sim", "Não"])
        if Torce == "Sim":
            add_Time = st.text_input("Qual time você torce")
        elif Torce == "Não":
            add_Time = "Não torce para nenhum time"


    # Comando de adição de dados dentro do BD 
    adicionr = f"INSERT INTO informações (CPF, Nome, Sexo, Data_de_Nascimento, Situação_Civil, Estado_Civil, Cidade_que_Mora, Time_que_Torce) VALUES ('{add_CPF}', '{add_Nome}', '{add_Sexo}', '{add_Data}', '{add_Situ}', '{add_Esta}', '{add_Cida}', '{add_Time}')"

    #Botão que adiciona todos os dados no BD com os comando de integração e fechamento do mesmo
    if st.button("Adicionar"):
        cursor.execute(adicionr)
        conexao.commit()
                    
        conexao.close()
        cursor.close()
        pagina_inicial()

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=
#OPÇÃO REMOVER
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Caso a opção "Remover" for selecionada irá acontecer isso
elif opcoes == "Remover":
    #st.title("Você apertou em Remover", text_alignment= "center")
    # Abrindo o Banco de Dados 
    conexao = conectar()
    cursor = conexao.cursor()
    
    st.header("Remover Cadastro")

    # Fazendo uma variavel com o comando de selecionar alguns dados com o auxilio da engine
    comando = pd.read_sql("SELECT Id, CPF, Nome FROM informações ORDER BY Id", engine)

    st.table(comando)

    #Selecionando o Id da pessoa que ira ser removida
    id_remover = st.selectbox("Selecione o Id para remover", comando["Id"]) #Comando["Id"] Vai na tabela e seleciona apenas a coluna ID

    #Localica (.loc) na coluna Id onde for igual ao Id seleciona o Nome na linha
    nome_remover = comando.loc[comando["Id"] == id_remover, "Nome"].values[0] 

    #Localica (.loc) na coluna Id onde for igual ao Id seleciona o CPF na linha
    cpf_remover = comando.loc[comando["Id"] == id_remover, "CPF"].values[0] 

    #Aviso Falando o nome e CPF da pessoa que ira remover
    st.warning(f"Removendo: **{nome_remover}** do CPF **{cpf_remover}**")

    #Comando para remover o cadastro com o id selecionado
    remover = f"DELETE FROM informações WHERE Id = {id_remover}"

    #Botão que remove o usuario selecionado
    if st.button("Remover"):
        cursor.execute(remover)
        conexao.commit()
                            
        conexao.close()
        cursor.close()

        pagina_inicial()



#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=
#OPÇÃO ATUALIZAR
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Caso a opção "Atualizar" for selecionada irá acontecer isso
elif opcoes == "Atualizar":
    #st.title("Você apertou em Atualizar", text_alignment= "center")
    # Abrindo o Banco de Dados 
    conexao = conectar()
    cursor = conexao.cursor()


    st.header("Atualizção de Cadastro")

    # Fazendo uma variavel com o comando de selecionar alguns dados com o auxilio da engine
    comando = pd.read_sql("SELECT Id, CPF, Nome FROM informações ORDER BY Id", engine)

    tabela = pd.read_sql("SELECT * FROM informações", engine)

    st.table(comando)

    #Selecionando a pessoa pelo id para alterção
    id_altera = st.selectbox("Selecione o Id para atualizar", tabela["Id"])

    #Localica (.loc) na coluna Id onde for igual ao Id seleciona o CPF na linha
    cpf_altera = tabela.loc[tabela["Id"] == id_altera, "CPF"].values[0] 

    #Localica (.loc) na coluna Id onde for igual ao Id seleciona o Nome na linha
    nome_altera = tabela.loc[tabela["Id"] == id_altera, "Nome"].values[0] 

    #Localica (.loc) na coluna Id onde for igual ao Id seleciona o Sexo na linha
    sexo_altera = tabela.loc[tabela["Id"] == id_altera, "Sexo"].values[0] 

    #Localica (.loc) na coluna Id onde for igual ao Id seleciona a Data de Nascimento na linha
    data_altera = tabela.loc[tabela["Id"] == id_altera, "Data_de_Nascimento"].values[0] 

    #Localica (.loc) na coluna Id onde for igual ao Id seleciona a Situação Civil na linha
    situacao_altera = tabela.loc[tabela["Id"] == id_altera, "Situação_Civil"].values[0] 

    #Localica (.loc) na coluna Id onde for igual ao Id seleciona o Estado Civil na linha
    estado_altera = tabela.loc[tabela["Id"] == id_altera, "Estado_Civil"].values[0]

    #Localica (.loc) na coluna Id onde for igual ao Id seleciona a Cidade na linha
    cidade_altera = tabela.loc[tabela["Id"] == id_altera, "Cidade_que_Mora"].values[0]  

    #Localica (.loc) na coluna Id onde for igual ao Id seleciona o Time na linha
    time_altera = tabela.loc[tabela["Id"] == id_altera, "Time_que_Torce"].values[0] 

    st.warning(f"Alterando valores do usuario: {nome_altera} do CPF {cpf_altera}")


    #Cria uma variavel que apenas lê o nome nas colunas 
    colunas = pd.read_sql("SELECT Nome, Sexo, Data_de_Nascimento, Situação_Civil, Estado_Civil, Cidade_que_Mora, Time_que_Torce FROM informações", engine)
    #Campo para Selecionar a coluna que deseja alterar
    campo_altera = st.selectbox("Selecione o campo para alterar", colunas.columns)

    #Alteração no campo nome
    if campo_altera == "Nome":

        #Mostra o dado atual
        st.info(f'o campo "Nome" atualmente está como: {nome_altera}')

        #Digitação do novo dado
        novo_nome = st.text_input("Digite o nome")

        #Comando para alterar o campo
        alteracao = f"UPDATE informações SET Nome = '{novo_nome}' WHERE Id = {id_altera}"

        #Botão que atualiza o campo
        if st.button("Atualizar"):
            cursor.execute(alteracao)
            conexao.commit()
            
            conexao.close()
            cursor.close()

            pagina_inicial()

    #Alteração no campo Sexo
    elif campo_altera == "Sexo":

        #Mostra o dado atual
        st.info(f'O campo "Sexo" atualmente está como: {sexo_altera}')
        
        #Seleciona o novo dado do campo
        sexo = st.radio("Sexo",
                        ["Masculino", "Feminino"])
        if sexo == "Masculino":
            novo_sexo = "M"
        elif sexo == "Feminino":
            novo_sexo = "F"


        #Comando para alterar o campo
        alteracao = f"UPDATE informações SET Sexo = '{novo_sexo}' WHERE Id = {id_altera}"

        #Botão que atualiza o campo
        if st.button("Atualizar"):
            cursor.execute(alteracao)
            conexao.commit()
                        
            conexao.close()
            cursor.close()

            pagina_inicial()
        
        
    #Alteração no campo data    
    elif campo_altera == "Data_de_Nascimento":

        #Mostra o dado atual
        st.info(f'o campo "Data de Nascimento" atualmente está como: {data_altera}')

        #Seleciona o novo dado do campo
        nova_data = st.date_input("Data de Nascimento", value=None, min_value=data_minima, format="DD/MM/YYYY")
        
        #Comando para alterar o campo
        alteracao = f"UPDATE informações SET Data_de_Nascimento = '{nova_data}' WHERE Id = {id_altera}"
        
        #Botão que atualiza o campo
        if st.button("Atualizar"):
            cursor.execute(alteracao)
            conexao.commit()
                    
            conexao.close()
            cursor.close()

            pagina_inicial()

    #Alteração no campo Situação Civil
    elif campo_altera == "Situação_Civil":

        #Mostra o dado atual
        st.info(f'O campo "Situação Civil atualmente está como: {situacao_altera}"')

        #Selecionando o novo dado do campo
        nova_situ = Situ = st.selectbox("Situação Civil", options=["Empregado(a)", "Desempregado(a)", "Estudante", "Aposentado(a)"])
        if Situ == "Estudante":
            nova_estu = st.radio('Estudante',
                     ["Escola", "Faculdade"])
            nova_situ = f"{Situ}/{nova_estu}"
        elif Situ == "Empregado(a)":
            nova_empre = st.text_input("Digite seu cargo")
            nova_situ = f"{Situ}/{nova_empre}"

        #Comando para alterar o campo
        alteracao = f"UPDATE informações SET Situação_Civil = '{nova_situ}' WHERE Id = {id_altera}"
                
        #Botão que atualiza o campo
        if st.button("Atualizar"):
            cursor.execute(alteracao)
            conexao.commit()
                            
            conexao.close()
            cursor.close()

            pagina_inicial()

    #Alteração no campo Estado Civil
    elif campo_altera == "Estado_Civil":

        #Mostra o dado atual
        st.info(f'O campo "Estado Civil" atualmente está como: {estado_altera}')

        #Selecionadno o novo dado do campo
        novo_estado = st.selectbox("Estado Civil", options=["Solteiro(a)", "Casado(a)", "Divorciado(a)", "Viúvo(a)", "Namoradno"])

        #Comando para alterar o campo
        alteracao = f"UPDATE informações SET Estado_Civil = '{novo_estado}' WHERE Id = {id_altera}"
                        
        #Botão que atualiza o campo
        if st.button("Atualizar"):
            cursor.execute(alteracao)
            conexao.commit()
                                    
            conexao.close()
            cursor.close()

            pagina_inicial()

    #Alteração no campo Cidade que Mora
    elif campo_altera == "Cidade_que_Mora":   

        #Mostra o dado atual
        st.info(f'O campo "Cidade que Mora" atualmente está como: {cidade_altera}')

        #Selecionado o novo dado do campo
        nova_cidade = st.text_input("Cidade onde mora")

        #Comando para alterar o campo
        alteracao = f"UPDATE informações SET Cidade_que_Mora = '{nova_cidade}' WHERE Id = {id_altera}"
                                
        #Botão que atualiza o campo
        if st.button("Atualizar"):
            cursor.execute(alteracao)
            conexao.commit()
                                            
            conexao.close()
            cursor.close()

            pagina_inicial()


    #Alteração no campo Time que Torce
    elif campo_altera == "Time_que_Torce":

        #Mostra o dado atual
        st.info(f'O campo "Time que Torce" atualmente está como: {time_altera}')

        #Selecionando o novo dado do campo
        novo_Torce = st.radio("Torce para algum time?",
                ["Sim", "Não"])
        if novo_Torce == "Sim":
            novo_time = st.text_input("Qual time você torce")
        elif novo_Torce == "Não":
            novo_time = "Não torce para nenhum time"

        #Comando para alterar o campo
        alteracao = f"UPDATE informações SET Time_que_Torce = '{novo_time}' WHERE Id = {id_altera}"
                                        
        #Botão que atualiza o campo
        if st.button("Atualizar"):
            cursor.execute(alteracao)
            conexao.commit()
                                                    
            conexao.close()
            cursor.close()

            pagina_inicial()
