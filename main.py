# Um software python de terminal que busca ser uma pequena
# versão funcional do ifood

import os
import time

# Variaveis de escopo global
limparTela = "clear"
#identificar sistema operacional
if os.name == "nt":
    limparTela = "cls"
else:
    limparTela = "clear"

# Lista de dicionários
usuarios = [
    {
        "nome":"tia",
        "usuario":"tia",
        "senha":"tia"
    },
    {
        "nome":"lau",
        "usuario":"lau",
        "senha":"lau" 
    }
]
alimentos = [
    {
        "nome":"pizza",
        "preco": 30,
        "categoria":"italiana"
    },
    {
        "nome":"maca",
        "preco": 5,
        "categoria":"argentina"
    },
    {
        "nome":"acaraje",
        "preco": 15,
        "categoria":"bahiana"
    },
] 

pedidos = [] # [{'usuario': 'lau', 'itens': [{'nome': 'pizza', 'preco': 30, 'categoria': 'italiana'}], 'total': 30, 'avaliacao': ''}]
alimentosBuscados = [] # [{'usuario': 'lau', 'alimentos': ['pizza', 'maça']}]

def telaInicio():
    print(" ________________________________________ ")
    print("|                                        |")
    print("|       SEJA BEM VINDO AO FEIFOOD        |")
    print("|________________________________________|\n")
    print("1) Login")
    print("2) Cadastrar-se")
    
def telamenuHome(usr):
    print(" ________________________________________ ")
    print("|                                        |")
    print("|                FEI-FOOD                |")
    print("|________________________________________|\n")
    print("    BEM VINDO(A)",usr["usuario"],"\n")
    print("1) Buscar por alimento")
    print("2) Listar informações de alimentos buscados")
    print("3) Cadastrar pedido")
    print("4) Avaliar pedido")
    print("5) Logout")


                
def verificarSeAlimentoExisteNoBanco(nomeAlimento):
    encontrado = False
    for alimento in alimentos:
        if alimento["nome"] == nomeAlimento:
            encontrado = True
    
    return encontrado

def visualizarPedido():
    print(" ________________________________________")
    print("|                                        ")
    print("|                PEDIDO                  ")
    print("|==== ALIMENTOS =========================")
    print("|                                        ")

    print(pedidos[-1])
    pedido = pedidos[-1]
    total = pedido["total"]
    for item in pedido["itens"]:
        print(f"|{item["nome"]} ------- R$ {item["preco"]}")

    print("|                                        ")
    print("|==== TOTAL =============================")
    print("|                                        ")
    print(f"|   {total}                              ")
    print("|________________________________________\n")    
    input("Pressione QUALQUER tecla para voltar a tela home\n")



def avaliarPedido(usr):
    os.system(limparTela)
    print("--------------- Avaliar Pedido -----------------")
    print("Nome : ",usr["nome"])
    # print("Total de avaliações: ",len(pedido["avaliacao"]))
    for pedido in pedidos:
        # print(pedido) -> print pedidos de todos os usuarios
        if pedido["usuario"] == usr["usuario"]: # usuario que tem o acesso
            print(pedido["itens"])
            
    input()



# função recursiva para finalizar o pedido
def finalizarPedido():
    decisao = input("Deseja Adicionar outro alimento? sim(1) ou finalizar pedido?(2) \n")
    if decisao == "1":
        pedidoFinalizado = False
    elif decisao == "2":
        pedidoFinalizado = True
    else:
        print("Opção inválida, tente novamente...")
        finalizarPedido()
    return pedidoFinalizado

def adicionarItensAoPedido(itens,nomeAlimento):
    itens.append(nomeAlimento)
    print("Itens no pedido até o momento: ")
    print(itens)
    print(nomeAlimento," adicionado(a) ao seu pedido.")


def cadastrarPedido(usr):
    os.system(limparTela)
    pedidoFinalizado = False
    itens = []

    print(" ________________________________________ ")
    print("|                                        |")
    print("|                PEDIDO                  |")
    print("|________________________________________|\n")

    while pedidoFinalizado == False:
        
        nomeAlimento = input("Informe o nome do alimento a ser adicionado no pedido:\n")
        alimentoExiste = verificarSeAlimentoExisteNoBanco(nomeAlimento)
        if alimentoExiste == True:# o alimento existe
            adicionarItensAoPedido(itens, nomeAlimento)
            finalizado = finalizarPedido()
            if finalizado == True:
                pedidoFinalizado = True
                itensPedido = []
                totalPedido = 0

                for alimento in alimentos:
                    for itemUsr in itens:
                        if alimento["nome"] == itemUsr:
                            itensPedido.append(alimento["nome"])
                            totalPedido += alimento["preco"]
                print("Itens do pedido: ",itensPedido)
                id = len(pedidos) + 1 # para não começar em zero, adicionei 1

                novoPedido = {
                    "id": id,
                    "usuario": usr["usuario"],
                    "itens": itensPedido,
                    "total": totalPedido,
                    "avaliacao": ""
                }

                pedidos.append(novoPedido)
                
                os.system(limparTela)
                print("Fazendo o pedido...")
                time.sleep(1)
                print("pedido realizado com sucesso")
                #visualizarPedido()
                input("Pressione QUALQUER tecla para voltar a tela home\n")
            else:
                print("Alimento não encontrado no banco de dados, tente novamente...")



def listarAlimentos():
    pass



def buscarAlimento(nomeUsuario,nomeAlimento):
    alimentoBuscado = []
    alimentoExistenteNoBanco = False
    os.system(limparTela)
    print("__________________________________________")
    print("|                                        |")
    print("|             BUSCAR ALIMENTO            |")
    print("|________________________________________|")
    
    for alimento in alimentos:
        if alimento["nome"] in nomeAlimento:
            alimentoExistenteNoBanco = True

    if alimentoExistenteNoBanco == True:
        for alimento in alimentos:
            if alimento["nome"] == nomeAlimento:
                alimentoBuscado.append(alimento["nome"])
                print("|                                        |")
                print("|     Nome : ",alimento["nome"])
                print("|     Categoria : ", alimento["categoria"])
                print("|     Preço : ",alimento["preco"])
        print("|________________________________________|\n")

    if alimentoExistenteNoBanco == False:
        print("Alimento não encontrado no banco de dados...")
            
    alimentosBuscados = {
        "usuario": nomeUsuario,
        "alimentos": alimentoBuscado
    }
    input("Pressione QUALQUER tecla para voltar a tela home\n")


def telaHome(usr): # dicionario do usuario que acessou
    acesso = True
    while acesso == True:

        os.system(limparTela)
        telamenuHome(usr)
        opcao = input("\nO que deseja fazer?\n")

        if opcao == "1":
            nomeAlimento = input("Informe o nome do alimento que deseja buscar: \n")
            buscarAlimento(usr["usuario"],nomeAlimento)
        
        elif opcao == "2":
            listarAlimentos()
            
        elif opcao == "3":
            cadastrarPedido(usr)            

        elif opcao == "4":
            avaliarPedido(usr)
        elif opcao == "5":
            input("Pressione QUALQUER tecla para voltar a tela de login\n")
            print("Voltando para a tela de login...")
            time.sleep(1)
            break
        else:
            print("Informe uma opção válida!")
            time.sleep(1)


def loginUsuario(usuario, senha):
    encontrado = False
    for usr in usuarios:
        if usuario == usr["usuario"] and senha == usr["senha"]:
            print("Acessando...")
            time.sleep(1)
            telaHome(usr) # tela HOME
            encontrado = True

    if encontrado == False:
        print("Credenciais incorretas! ")
        time.sleep(1)
        input("Pressione QUALQUER tecla para voltar a tela inicial\n")
         

#uma função recursiva para validar o cadastro do usuario
def validarCadastro(usuario):
    existe = False
    for usr in usuarios:
        if usuario == usr["usuario"]:
            existe = True
    
    if existe == True:
        print("Já existe alguém cadastrado com esse nome de usuário, tente outro...")
        usuario = input("Informe um novo nome de usuário: ")
        validarCadastro(usuario)

    return existe #false


def CadastrarUsuario(nome, usuario, senha):

    cadastrado = validarCadastro(usuario)
    if cadastrado == False:
        print("Cadastrando usuario...")
        time.sleep(1)

    user = {
        "nome": nome,
        "usuario": usuario,
        "senha": senha
    }

    usuarios.append(user)
    # verificar se ocorreu tudo bem ao gravar no arquivo
    
    return "Usuario cadastrado com sucesso" 


# loop principal
def main():

    while True: 
        opcao = 0
        os.system(limparTela)
        telaInicio()

        opcao = input("Escolha uma opção para continuar: ")
    
        if opcao == "1":
            print("\n----------- LOGIN ----------\n")
            usuario = input("Informe seu usuario: ")
            senha = input("Informe sua senha: ")
            loginUsuario(usuario, senha)

        elif opcao == "2":
            print("\n----------- CADASTRAR-SE ----------\n")
            nome = input("Informe um nome: ")
            usuario = input("Informe um nome de usuario: ")
            senha = input("Informe uma senha: ")
            mensagem = CadastrarUsuario(nome, usuario, senha)
            print(mensagem)
            input("\nPressione QUALQUER tecla para continuar\n")

        else:
            print("Informe uma opção válida! ")
            input("\nPressione QUALQUER tecla para continuar\n")

main()