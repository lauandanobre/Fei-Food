# Um software python de terminal que tem como objetivo ser uma pequena versão funcional e não tão complexa do ifood

import os
import time
import json
from dados import *

usuariosArq = "usuarios.txt"
pedidosArq = "pedidos.json"

#limparTela = "clear"
if os.name == "nt":
    limparTela = "cls"
else:
    limparTela = "clear"

tempoLongo = 0.7
tempoCurto = 0.3

#================================== carregar
def carregarUsuarios():
    arquivo = open(usuariosArq, "a") # cria arquivo caso esse não exista
    arquivo.close()
    arquivo = open(usuariosArq,"r")
    for linha in arquivo.readlines():
        #print(linha)
        palavras = linha.strip()
        palavras = palavras.split(",")
        nome, usuario, senha = palavras
        #print(nome,usuario,senha)
        user = {
            "nome": nome,
            "usuario": usuario,
            "senha": senha
        }
        usuarios.append(user)
    #print(usuarios)
    arquivo.close()

def carregarPedidos():
    global pedidos
    if not os.path.exists(pedidosArq):
        arquivo = open(pedidosArq, "w")
        json.dump([], arquivo)
        arquivo.close()

    arquivo = open(pedidosArq, "r")
    pedidos = json.load(arquivo)
    arquivo.close()


def salvarPedidos():
    arquivo = open(pedidosArq, "w")
    json.dump(pedidos, arquivo, indent=4)
    arquivo.close()    

def adicionarPedido(ped):
    pedidos.append(ped)
    salvarPedidos()

#==================================== adicionar
def adicionarUsuario(usr):
    arquivo = open(usuariosArq, "a")
    arquivo.write(f"{usr['nome']},{usr['usuario']},{usr['senha']}\n")
    arquivo.close()


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
    print("3) Meus Pedidos")
    print("4) Avaliar pedido")
    print("5) Logout")

def menuHomePedidos(usr):
    print(" ________________________________________ ")
    print("|                                        |")
    print("|              MEUS PEDIDOS              |")
    print("|________________________________________|\n")
    print("Pedidos de",usr["usuario"],"\n")
    print("1) Visualizar pedidos")
    print("2) Cadastrar pedido")
    print("3) Editar pedido")
    print("4) Excluir pedido")
    print("5) Voltar")


def verificarSeAlimentoExisteNoBanco(nomeAlimento):
    encontrado = False
    for alimento in alimentos:
        if alimento["nome"] == nomeAlimento:
            encontrado = True

    return encontrado


def mostrarPedidos(usr):
    encontrado = False
    os.system(limparTela)
    print("Pedidos:\n")
    for pedido in pedidos:
        if pedido["usuario"] == usr["usuario"]:
            encontrado = True
            print("------------------------------------")
            print("ID: ", pedido["id"])
            print("Itens:")
            print(pedido["itens"])
            print("Total: R$", pedido["total"])
            print("Avaliação:", pedido.get("avaliacao", "Não avaliado"))
    
    if encontrado == True:
        cont = 0
        for pedido in pedidos:
            if pedido["usuario"] == usr["usuario"]:
                cont += 1
        
        print(f"\n{cont} pedido(s) encontrados")
    else:
        print("Você não fez nenhum pedido ainda...")



def verificarSePossuiPedidos(usr):
    for pedido in pedidos:
        if pedido["usuario"] == usr["usuario"]:
            return True
    return False
def editarPedido(usr):
    os.system(limparTela)
    encontrado = False
    if not verificarSePossuiPedidos(usr):
        return "Você não possui pedidos para editar."

    mostrarPedidos(usr)
    idPedido = input("Informe o ID do pedido que deseja editar: ")

    for pedido in pedidos:
        if pedido["id"] == int(idPedido) and pedido["usuario"] == usr["usuario"]:
            encontrado = True
            print("1) Adicionar item")
            print("2) Remover item")
            print("3) Voltar")
            decisao = input("Escolha a opção: ")

            if decisao == "1":
                novoItem = input("Informe o alimento a adicionar: ")
                if verificarSeAlimentoExisteNoBanco(novoItem):
                    pedido["itens"].append(novoItem)
                    for alimento in alimentos:
                        if alimento["nome"] == novoItem:
                            pedido["total"] += alimento["preco"]
                    salvarPedidos()
                    return "Item adicionado com sucesso!"
                else:
                    return "Alimento não encontrado no banco de dados."

            elif decisao == "2":
                removerItem = input("Informe o alimento a remover: ")
                if removerItem in pedido["itens"]:
                    pedido["itens"].remove(removerItem)
                    for alimento in alimentos:
                        if alimento["nome"] == removerItem:
                            pedido["total"] -= alimento["preco"]
                    salvarPedidos()
                    return "Item removido com sucesso!"
                else:
                    return "Esse alimento não está no pedido."
            break

    if not encontrado:
        return "Pedido não encontrado."

def excluirPedido(usr):
    os.system(limparTela)
    encontrado = False
    v = verificarSePossuiPedidos(usr)
    if v == False:
        return "Você não possui pedidos para excluir."
        
    if v == True:
        mostrarPedidos(usr)
        idPedido = input("Informe o ID do pedido que deseja excluir: ")
        for pedido in pedidos:
            if pedido["id"] == int(idPedido) and pedido["usuario"] == usr["usuario"]:
                time.sleep(tempoCurto)
                pedidos.remove(pedido)
                salvarPedidos()
                encontrado = True
                return "Pedido excluído com sucesso!"
                

    if encontrado == False:
        return "Pedido não encontrado."

def avaliarPedido(usr):
    os.system(limparTela)
    encontrado = False
    v = verificarSePossuiPedidos(usr)
    if v == False:
        return "Você não possui pedidos para avaliar."
    if v == True:
        mostrarPedidos(usr)
        idPedido = input("Informe o ID do pedido que deseja avaliar: ")
        for pedido in pedidos:
            if pedido["usuario"] == usr["usuario"] and str(pedido["id"]) == idPedido:
                while True:
                    avaliacao = int(input("Informe sua avaliação para o pedido (de 1 a 5 estrelas): \n"))
                    if 1 <= avaliacao and avaliacao <= 5:
                        pedido["avaliacao"] = avaliacao
                        salvarPedidos()  # Atualizar o arquivo JSON dos pedidos
                        encontrado = True
                        return "Avaliação registrada com sucesso!"
                    else:
                        print("Avaliação inválida! Informe um número entre 1 e 5.")
    if encontrado == False:
        return "Pedido não encontrado."
    

# função recursiva para finalizar o pedido
def finalizarPedido():
    pedidoFinalizado = False
    decisao = input("\nDeseja Adicionar outro alimento? sim(1) ou finalizar pedido?(2) \n")
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
    time.sleep(tempoCurto)
    print(nomeAlimento," adicionado(a) ao seu pedido.")

def gerarNovoId():
    if not pedidos: 
        return 1
    else:
        maior_id = 0
        for ped in pedidos:
            if ped["id"] > maior_id:
                maior_id = ped["id"]
        return maior_id + 1
    
def cadastrarPedido(usr):
    os.system(limparTela)
    pedidoFinalizado = False
    itens = []  # lista de nomes de alimentos

    print(" ________________________________________ ")
    print("|                                        |")
    print("|           CADASTRAR PEDIDO             |")
    print("|________________________________________|\n")

    while not pedidoFinalizado:
        nomeAlimento = input("Informe o nome do alimento a ser adicionado no pedido:\n")
        if verificarSeAlimentoExisteNoBanco(nomeAlimento):
            itens.append(nomeAlimento)
            print(f"{nomeAlimento} adicionado ao pedido.")

            # Pergunta se deseja finalizar o pedido
            decisao = input("\nDeseja adicionar outro alimento? sim(1) ou finalizar pedido?(2) \n")
            if decisao == "2":
                pedidoFinalizado = True

                # Calcula total do pedido
                totalPedido = 0
                for nome in itens:
                    for alimento in alimentos:
                        if alimento["nome"] == nome:
                            totalPedido += alimento["preco"]

                # Define ID do pedido
                
                idPedido = gerarNovoId()
                print(idPedido)


                # Cria dicionário do pedido
                novoPedido = {
                    "id": idPedido,
                    "usuario": usr["usuario"],
                    "itens": itens,  # apenas nomes de alimentos
                    "total": totalPedido,
                    "avaliacao": ""
                }

                # Adiciona à lista e salva no JSON
                pedidos.append(novoPedido)
                salvarPedidos()  # salva todos os pedidos no JSON

                os.system(limparTela)
                print("Fazendo o pedido...")
                time.sleep(tempoLongo)
                return "Pedido realizado com sucesso!"
        else:
            print("Alimento não encontrado no banco de dados, tente novamente...")

def listarAlimentos():
    os.system(limparTela)
    print("__________________________________________")
    print("|                                        |")
    print("|           LISTA DE ALIMENTOS           |")
    print("|________________________________________|\n")

    for alimento in alimentos:
        print("|     Nome : ", alimento["nome"], " Categoria: ", alimento["categoria"], " Preço: ",alimento["preco"])
        print("|________________________________________|")
    input("Pressione QUALQUER tecla para voltar a tela home\n")


def listarAlimentosBuscados(usr):
    os.system(limparTela)
    alimentos_usuario = []
    for busca in alimentosBuscados:
        if busca["usuario"] == usr["usuario"]:
            for alimento in busca["alimentos"]:
                alimentos_usuario.append(alimento["alimento"])

    if len(alimentos_usuario) == 0:
        print(" Você ainda não buscou por nenhum alimento.")

    else:
        print(" ______________________________________")
        print("|                                      ")
        print("|     ALIMENTOS BUSCADOS RECENTEMENTE: ")
        print("|")
        for nome in alimentos_usuario:
            print(f"| - {nome}")

    print("|________________________________________\n")
    input("Pressione QUALQUER tecla para voltar à tela home\n")



def buscarAlimento(usr, nomeAlimento):
    nomeUsuario = usr["usuario"]
    alimentoBuscado = []
    alimentoExistenteNoBanco = False
    os.system(limparTela)
    
    for alimento in alimentos:
        if alimento["nome"] in nomeAlimento:
            alimentoExistenteNoBanco = True

    if alimentoExistenteNoBanco == True:
        for alimento in alimentos:
            if alimento["nome"] == nomeAlimento:
                item = {
                    "usuario": nomeUsuario,
                    "alimento": nomeAlimento
                }
                alimentoBuscado.append(item)
                print(" ________________________________________")
                print("|                                        |")
                print("|             BUSCAR ALIMENTO            |")
                print("|________________________________________|")
                print("|                                        |")
                print("|     Nome : ",alimento["nome"])
                print("|     Categoria : ", alimento["categoria"])
                print("|     Preço : ",alimento["preco"])
        print("|________________________________________|\n")

    if alimentoExistenteNoBanco == False:
        time.sleep(tempoCurto)
        print("Alimento não encontrado no banco de dados...")
            
    busca = {
        "usuario": nomeUsuario,
        "alimentos": alimentoBuscado
    }
    alimentosBuscados.append(busca)
    input("Pressione QUALQUER tecla para voltar a tela home\n")


def telaHome(usr): # dicionario do usuario que acessou(que tem o acesso)
    acesso = True
    while acesso == True:

        os.system(limparTela)
        telamenuHome(usr)
        opcao = input("\nO que deseja fazer?\n")

        if opcao == "1":
            os.system(limparTela)
            nomeAlimento = input("Informe o nome do alimento que deseja buscar: \n")
            buscarAlimento(usr,nomeAlimento)
        
        elif opcao == "2":
            listarAlimentosBuscados(usr)
            
        elif opcao == "3":
            while True:
                os.system(limparTela)
                menuHomePedidos(usr)

                decisao = input("\nO que deseja fazer?\n")
                if decisao == "1":
                    mostrarPedidos(usr)
                    input("Pressione QUALQUER tecla para voltar a tela de pedidos\n")
                    break
                elif decisao == "2":
                    resposta = cadastrarPedido(usr)
                    print(resposta)
                    input("Pressione QUALQUER tecla para voltar à tela home\n")
                    break
                elif decisao == "3":
                    resposta = editarPedido(usr)
                    print(resposta)
                    input("Pressione QUALQUER tecla para voltar à tela home\n")
                    break
                elif decisao == "4":
                    resposta = excluirPedido(usr)
                    print(resposta)
                    input("Pressione QUALQUER tecla para voltar à tela home\n")
                    break
                elif decisao == "5":
                    print("Voltando...")
                    time.sleep(tempoLongo)
                    break
                else:
                    print("Informe uma opção válida!")
                    time.sleep(tempoLongo)           

        elif opcao == "4":
            resposta = avaliarPedido(usr)
            print(resposta)
            input("Pressione QUALQUER tecla para voltar à tela home\n")
        elif opcao == "5":
            input("Pressione QUALQUER tecla para voltar a tela de login\n")
            print("Voltando para a tela de login...")
            time.sleep(tempoLongo)
            acesso = False
        else:
            print("Informe uma opção válida!")
            time.sleep(tempoLongo)


def loginUsuario(usuario, senha):
    encontrado = False
    for usr in usuarios:
        if usuario == usr["usuario"] and senha == usr["senha"]:
            print("Acessando...")
            time.sleep(tempoLongo)
            telaHome(usr) # tela HOME
            encontrado = True

    if encontrado == False:
        print("Credenciais incorretas! ")
        time.sleep(tempoLongo)
        input("Pressione QUALQUER tecla para voltar a tela inicial\n")
         

def validarCadastro(usuario):
    existe = False
    for usr in usuarios:
        if usuario == usr["usuario"]:
            existe = True

    return existe #false



def CadastrarUsuario(nome, usuario, senha):

    jaCadastrado = True
    while jaCadastrado == True:
        jaCadastrado = validarCadastro(usuario)
        if jaCadastrado == True:
            print("Já existe alguém cadastrado com esse nome de usuário, tente outro...")
            usuario = input("Informe um novo nome de usuário: ")
    
    if jaCadastrado == False:
        print("Cadastrando usuario...")
        time.sleep(tempoLongo)

    user = {
        "nome": nome,
        "usuario": usuario,
        "senha": senha
    }
    
    usuarios.append(user)
    # gravar no banco de dedos, arquivo txt
    adicionarUsuario(user)
    return "Usuario cadastrado com sucesso" 


# loop principal
def main():
    carregarUsuarios()
    carregarPedidos()
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
