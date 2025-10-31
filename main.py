# Um software python de terminal que busca ser uma pequena
# versão funcional do ifood, nele devo fazer pedidos de comida
# implementando as seguntes funcionalidades:

import os
import time

# Variaveis de escopo global
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
        "nome":"maça",
        "preco": 5,
        "categoria":"argentina"
    },
    {
        "nome":"acarajé",
        "preco": 15,
        "categoria":"bahiana"
    },
] 

pedidos = [] # [{'usuario': 'lau', 'itens': [{'nome': 'pizza', 'preco': 30, 'categoria': 'italiana'}], 'total': 30, 'avaliacao': ''}]

def telaInicio():
    print(" ________________________________________ ")
    print("|                                        |")
    print("|       SEJA BEM VINDO AO FEIFOOD        |")
    print("|________________________________________|\n")
    print("1) Login")
    print("2) Cadastrar-se")
    
def telaMenuHome():
    print("1) Buscar por alimento")
    print("2) Listar informações de alimentos buscados")
    print("3) Cadastrar pedido")
    print("4) Avaliar pedido")
    print("5) Logout")

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

def cadastrarPedido(usr,itens):
    #itens = ["pizza", "pizza", "maça", "acarajé"] - 4 itens
    itensPedido = []
    totalPedido = 0

    for alimento in alimentos:
        for item_escolhido_usr in itens:
            if alimento["nome"] == item_escolhido_usr:
                itensPedido.append(alimento)
                totalPedido += alimento["preco"]

    novoPedido = {
        "usuario": usr["usuario"],
        "itens": itensPedido,
        "total": totalPedido,
        "avaliacao": ""
    }

    pedidos.append(novoPedido)
    # print(pedidos)



                
def verificarSeAlimentoExiste(nomeAlimento):
    encontrado = False
    for alimento in alimentos:
        if alimento["nome"] == nomeAlimento:
            encontrado = True
    
    return encontrado

def visualizarPedido():
    #{'usuario': 'lau', 'itens': [{'nome': 'pizza', 'preco': 30, 'categoria': 'italiana'}], 'total': 30, 'avaliacao': ''}
    print(" ________________________________________")
    print("|                                        ")
    print("|                PEDIDO                  ")
    print("|==== ALIMENTOS =========================")
    print("|                                        ")

    pedido = pedidos[-1] 
    
    total = pedido["total"]

    for item in pedido["itens"]:
        print("|",item['nome']," ------- R$ ",item['preco'])

    print("|                                        ")
    print("|==== TOTAL =============================")
    print("|                                        ")
    print("|   ",total,"                            ")
    print("|________________________________________\n")    



def buscarAlimento(nomeAlimento):
    alimentosBuscados = []
    os.system(limparTela)
    print("__________________________________________")
    print("|                                        |")
    print("|             BUSCAR ALIMENTO            |")
    print("|________________________________________|")
    
    
    for alimento in alimentos:
        if alimento["nome"] == nomeAlimento:
            alimentosBuscados.append(alimento["nome"])
            print("|                                        |")
            print("|     Nome : ",alimento["nome"])
            print("|     Categoria : ", alimento["categoria"])
            print("|     Preço : ",alimento["preco"])
    print("|________________________________________|\n")
    input("Pressione QUALQUER tecla para voltar a tela home\n")

def listarAlimentos():
    pass

def telaHome(usr): # dicionario do usuario que acessou
    #{"nome": "lau", "usuario": "lau", "senha": "123"} 
    acesso = True
    while acesso == True:
        os.system(limparTela)
        print(" ________________________________________ ")
        print("|                                        |")
        print("|                FEI-FOOD                |")
        print("|________________________________________|\n")
        print("    BEM VINDO(A)",usr["usuario"],"\n")

        telaMenuHome()
        opcao = input("\nO que deseja fazer?\n")
        if opcao == "1":
            nomeAlimento = input("Informe o nome do alimento que deseja buscar: \n")
            buscarAlimento(nomeAlimento)
        
        elif opcao == "2":
            listarAlimentos()
            
        elif opcao == "3":
            os.system(limparTela)
            pedidoFinalizado = False
            itens = []

            print(" ________________________________________ ")
            print("|                                        |")
            print("|                PEDIDO                  |")
            print("|________________________________________|\n")

            while pedidoFinalizado == False:

                nomeAlimento = input("Informe o nome do alimento:\n")
                verificacao = verificarSeAlimentoExiste(nomeAlimento)
                #print(verificacao)
                if verificacao == True:# o alimento existe
                    itens.append(nomeAlimento)
                    print(nomeAlimento," adicionado(a) ao seu pedido")
                    decisao = input("Deseja Adicionar outro alimento? sim(s) qualquer tecla para não: \n")
                    if decisao == "s":
                        pedidoFinalizado = False
                    if decisao != "s":
                        os.system(limparTela)
                        cadastrarPedido(usr,itens)
                        print("Fazendo o pedido...")
                        time.sleep(1)
                        print("pedido realizado com sucesso")
                        decisao2 = input("gostaria de ver o seu pedido? sim(s) ou qualquer tecla para não: \n")
                        if decisao2 == "s":
                            visualizarPedido()
                            pedidoFinalizado = True
                            input()
                        elif decisao2 != "s":
                            print("Certo")
                            pedidoFinalizado = True
                            input()
                else:
                    print("Esse alimento não foi encontrado, tente outro...")

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
    # print(usuarios)
    for usr in usuarios:
        # print(usr)
        if usuario == usr["usuario"] and senha == usr["senha"]: # Verificar nos arquivos de texto, se usuario[x] existe e se a senha[x] esta correta
            # print("encontrado")
            print("Acessando...")
            time.sleep(1)
            telaHome(usr)
            encontrado = True

    if encontrado == False:
        print("Credenciais incorretas! ")
        time.sleep(1)
        input("Pressione QUALQUER tecla para voltar a tela inicial\n")
               
        

         

def CadastrarUsuario(nome, usuario, senha):
    usuario = {
        "nome": nome,
        "usuario": usuario,
        "senha": senha
    }
    usuarios.append(usuario)
    # for usr in usuarios:
    #     print(usr["nome"])
    #     print(usr["usuario"])
    #     print(usr["senha"])
    
    return "Usuario cadastrado com sucesso" # verificar se ocorreu tudo bem ao gravar no arquivo
    

# loop principal
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