import os 
import sqlite3
from sqlite3 import Error
from datetime import datetime

# conexao
vConexao = sqlite3.connect("simplesAgenda.db")
cursor = vConexao.cursor()

# query
def query(conexao, sql):
    try:
        cursor = conexao.cursor()
        cursor.execute(sql)
        conexao.commit()
    except Error as erro:
        print(erro)
    finally:
        print("Operação realizada com sucesso!")
# consulta com retorno em array
def consultar(conexao, sql):
    cursor = conexao.cursor()
    cursor.execute(sql)    
    resultado = cursor.fetchall()
    return resultado
# função para inserir contato
def menuInserir(con):
    os.system("cls")
    menuPrincipal(1)
    print("----------------| Adicionar novo contato |-------------------")
    vID = input("Digite o novo ID: ")
    vNome = input("Digite o nome e sobrenome: ")
    vTelefone = input("Número com DDD: ")
    opcao = "0"
    while opcao < "1" or opcao > "6":
        print("--------------------| Tipo de contato |-----------------")
        print("[1]: Cônjugue \t [2]: Namorado(a)")
        print("[3]: Amigo(a) \t [4]: Família")
        print("[5]: Trabalho \t [6]: Conhecido(a)")
        opcao = input("Digite uma opção: ")
        if(opcao == "1"):
            vTipo_de_contato = "Cônjugue"
        elif(opcao == "2"):
            vTipo_de_contato = "Namorado(a)"
        elif(opcao == "3"):
            vTipo_de_contato = "Amigo(a)"
        elif(opcao == "4"):
            vTipo_de_contato = "Família"
        elif(opcao == "5"):
            vTipo_de_contato = "Trabalho"
        elif(opcao == "6"):
            vTipo_de_contato = "Conhecido(a)"
        else:
            print("Opção inválida")
            os.system("pause")
    vsql = "INSERT INTO agenda (ID, nome, telefone, tipo_de_contato) VALUES ("+vID+", '"+vNome+"', '"+vTelefone+"', '"+vTipo_de_contato+"');"
    query(con, vsql)
    os.system("pause")
    menuPrincipal(0)
# função para editar contato
def menuEditar(con):
    os.system("cls")
    menuPrincipal(2)
    print("--------------| Atualizar contato existente |----------------")
    print("\t\t\t\t[V]: Voltar ao início")
    vID = "0"
    while (vID < "1" or vID > str(contaContatos(vConexao))):
        vID = input("\nInforme o ID do contato: ")
        if(vID == "V"): 
            break
        elif(int(vID) > contaContatos(vConexao) or vID < "1"):
            print("Insira um ID válido!")
            os.system("pause")
        else:
            registro = consultar(con, "SELECT * FROM agenda WHERE ID = " + vID)
            registroNome = registro[0][1]
            registroTelefone = registro[0][2]
            registroTipo = registro[0][3]
            os.system("cls")
            print("--------------| Nova entrada de dados do contato |-------------")
            vNome = input("Digite o nome: ")
            vTelefone = input("Digite o telefone: ")
            opcao = "0"
            while opcao < "1" or opcao > "6":
                print("-------| Tipo de contato |-------")
                print("[1]: Cônjugue \t [2]: Namorado(a)")
                print("[3]: Amigo(a) \t [4]: Família")
                print("[5]: Trabalho \t [6]: Conhecido(a)")
                opcao = input("Digite uma opção: ")
                if(opcao == "1"):
                    vTipo_de_contato = "Cônjugue"
                elif(opcao == "2"):
                    vTipo_de_contato = "Namorado(a)"
                elif(opcao == "3"):
                    vTipo_de_contato = "Amigo(a)"
                elif(opcao == "4"):
                    vTipo_de_contato = "Família"
                elif(opcao == "5"):
                    vTipo_de_contato = "Trabalho"
                elif(opcao == "6"):
                    vTipo_de_contato = "Conhecido(a)"
                else:
                    print("Opção inválida")
                    os.system("pause")
            if(len(vNome) == 0):
                vNome = registroNome
            if(len(vTelefone) == 0):
                vTelefone = registroTelefone
            if(len(vTipo_de_contato) == 0):
                vTipo_de_contato = registroTipo
            vsql = "UPDATE agenda SET nome = '"+ vNome + "', telefone = '"+ vTelefone +"', tipo_de_contato = '"+ vTipo_de_contato +"' WHERE ID = " + vID
            query(con, vsql)
            os.system("pause")
# função para remover contato
def menuRemover():
    os.system("cls")
    menuPrincipal(3)
    print("----------------| Remover um contato |-------------------")
    print("\t\t\t\t[V]: Voltar ao início")
    vID = "0"
    while (vID < "1"):
        vID = input("\nDigite o ID do registro a ser deletado: ")
        if(vID == "V"): 
            break
        else:
            os.system("cls")
            data_e_hora_atuais = datetime.now()
            data_e_hora_em_texto = data_e_hora_atuais.strftime("%d/%m/%Y - %H:%M")
            print("#########| Agenda de Contatos | "+ data_e_hora_em_texto +" |########")
            barraNotificação(4)
            registro = consultar(vConexao, "SELECT * FROM agenda WHERE ID = " + vID)
            print("-----| Dados do contato registrado |-----")
            print("\nID |   Nome   |      Telefone      | Tipo de contato")
            print("------------------------------------------------------------")
            for r in registro:
                print("\n{0: <5}{1: <12}{2: <23}{3: <0}".format(r[0], r[1], r[2], r[3]))
            opcao = "0"
            while opcao != "S" and opcao != "N":
                print("\nDeseja realmente remover este contato? ")
                print("[S]: Sim \t [N]: Não")
                opcao = input("Selecione uma opção > ")
                if(opcao == "S"):
                    vsql = "DELETE FROM agenda WHERE ID = " + vID
                    query(vConexao, vsql)
                    os.system("pause")
                elif(opcao == "N"):
                    break
                else:
                    print("Digite uma opção válida!")
            
# função para retornar quantidade de contatos adicionados
def contaContatos(con):
    vsql = "SELECT * FROM agenda"
    registro = consultar(con, vsql)
    vCont = 0
    for r in registro:
        r[0] #vai contar cada linha
        vCont +=1
    return vCont
# função para mostrar na tela os contatos cadastrados
def apresentaAgenda(con):
    vsql = "SELECT * FROM agenda"
    registro = consultar(con, vsql)
    vLimite = 10
    vCont = 0
    for r in registro:
        if(vCont < vLimite):
            print("{0: <6}{1: <10}{2: <25}{3: <10}".format(r[0], r[1], r[2], r[3]))
            vCont +=1
        if(vCont >= vLimite):
            vCont = 0
            os.system("pause")
            os.system("cls")
    print("\n\t\t----Fim da lista----\n")

#Funcao para visualizão do menu principal
def menuPrincipal(a):
    os.system("cls")
    data_e_hora_atuais = datetime.now()
    data_e_hora_em_texto = data_e_hora_atuais.strftime("%d/%m/%Y - %H:%M")
    print("#########| Agenda de Contatos | "+ data_e_hora_em_texto +" |########")
    barraNotificação(a)
    print("----------| Há um total de "+str(contaContatos(vConexao))+" contatos registrados |---------")
    print("\nID |   Nome   |      Telefone      | Tipo de contato")
    print("------------------------------------------------------------")
    print()
    apresentaAgenda(vConexao)
# função para notificar o usuário 
def barraNotificação(a):
    if a == 0:
        mensagem = "Seja bem vindo(a)! (:D) Fique à vontade."
    elif a == 1:
        mensagem = "Fique atento aos dados! Cuidado para não errar."
    elif a == 2:
        mensagem = "Verifique o ID do contato que quer atualizar!"
    elif a == 3:
        mensagem = "Verifique o ID do contato que quer deletar!"
    elif a == 4:
        mensagem = "Atenção! Contato removido não pode ser recuperado."
    print("#####| Notificação: ", mensagem)
#função para apresentar opções
def apresentaOpcao():
    opcao = 0
    while opcao != "S":
        menuPrincipal(0)
        print("[I]: Inserir Contato \t [E]: Editar Contato")
        print("[R]: Remover Contato \t [S]: Sair")
        opcao = input("Digite uma opção: ")
        if opcao == "I":
            menuInserir(vConexao)
        elif opcao == "E":
            menuEditar(vConexao)
        elif opcao == "R":
            menuRemover()
        elif opcao == "S":
            os.system("cls")
            vConexao.close()
            print("Encerrando Programa em: 3.. 2.. 1..")
            print("Programa encerrado!")
        else:
            os.system("cls")
            print("Opção inválida")
            os.system("pause")
# chamada da função
apresentaOpcao()


