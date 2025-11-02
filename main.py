# Um software python de terminal que busca ser uma pequena
# versão funcional do ifood

import os
import time
from menu import *
from dados import alimentos, usuarios, pedidos, alimentosBuscados

arquivoUsuarios = "./dados/usuarios.txt"
arquivoPedidos = "./dados/pedidos.txt"
arquivoAlimentos = "./dados/alimentos.txt"
arquivoAlimentosBuscados = "./dados/alimentosBuscados.txt"

limparTela = "clear"

def adicionarDadosUsuario(usr):
    with open(arquivoUsuarios, "a") as f:
        for usr in usuarios:
            f.write(f"{usr['nome']},{usr['usuario']},{usr['senha']}\n")


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
    mostrarPedidos(usr)
    possui = verificarSePossuiPedidos(usr)
    if possui == False:
        print("Você não possui pedidos para avaliar...")
        input("Pressione QUALQUER tecla para voltar a tela home\n")
        return "finalizado"

    idPedido = input("Informe o ID do pedido que deseja avaliar: \n")
    for pedido in pedidos:
        if pedido["usuario"] == usr["usuario"]: # usuario que tem o acesso
            if str(pedido["id"]) == idPedido:
                avaliacao = input("Informe sua avaliação para o pedido (de 1 a 5 estrelas): \n")
                pedido["avaliacao"] = avaliacao
                print("Avaliação registrada com sucesso!")
                input("Pressione QUALQUER tecla para voltar a tela home\n")
                return "finalizado"


def mostrarPedidos(usr):
    for pedido in pedidos:
        if pedido["usuario"] == usr["usuario"]:
            print("--------------- Pedido -----------------")
            print("ID: ",pedido["id"]," Itens: ",pedido["itens"]," Total: ",pedido["total"])
    print(f"{len(pedidos)} pedidos encontrados")

def verificarSePossuiPedidos(usr):
    for pedido in pedidos:
        if pedido["usuario"] == usr["usuario"]:
            return True
    return False

def excluirPedido(usr):
    os.system(limparTela)
    pedidoExcluido = False
    print(" ________________________________________ ")
    print("|                                        |")
    print("|             EXCLUIR PEDIDO             |")
    print("|________________________________________|\n")
    while pedidoExcluido == False:
        os.system(limparTela)
        mostrarPedidos(usr)
        possuiPedidos = verificarSePossuiPedidos(usr)
        if possuiPedidos == False:
            print("Você não possui pedidos para excluir...")
            input("Pressione QUALQUER tecla para voltar a tela home\n")
            break

        idPedido = input("Informe o ID do pedido que deseja excluir: \n")

        for pedido in pedidos:
            if str(pedido["id"]) == idPedido and pedido["usuario"] == usr["usuario"]:
                pedidos.remove(pedido)
                pedidoExcluido = True
                print("Pedido excluído com sucesso!")
                input("Pressione QUALQUER tecla para voltar a tela home\n")
                break

        if pedidoExcluido == False:
            print("Pedido não encontrado, tente novamente...")
            time.sleep(1)

def editarPedido(usr):
    os.system(limparTela)
    edicaoFinalizada = False
    print(" ________________________________________ ")
    print("|                                        |")
    print("|             EDITAR PEDIDO              |")
    print("|________________________________________|\n")
    while edicaoFinalizada == False:
        os.system(limparTela)
        mostrarPedidos(usr)
        possuiPedidos = verificarSePossuiPedidos(usr)
        if possuiPedidos == False:
            print("Você não possui pedidos para editar...")
            input("Pressione QUALQUER tecla para voltar a tela home\n")
            break

        idPedido = input("Informe o ID do pedido que deseja editar: \n")

        for pedido in pedidos:
            if str(pedido["id"]) == idPedido and pedido["usuario"] == usr["usuario"]:
                print("Pedido encontrado: ",pedido)
                print("1) Adicionar item")
                print("2) Remover item")
                print("3) Voltar")
                decisao = input("\nO que deseja fazer?\n")
                if decisao == "1":
                    novoItem = input("Informe o nome do novo alimento a ser adicionado: \n")
                    alimentoExiste = verificarSeAlimentoExisteNoBanco(novoItem)
                    if alimentoExiste == True:
                        pedido["itens"].append(novoItem)
                        for alimento in alimentos:
                            if alimento["nome"] == novoItem:
                                pedido["total"] += alimento["preco"]
                    print("Pedido atualizado com sucesso: ",pedido)
                    edicaoFinalizada = True
                    input("Pressione QUALQUER tecla para voltar a tela home\n")
                elif decisao == "2":
                    alimentoParaRemover = input("Informe o nome do alimento a ser removido: \n")
                    if alimentoParaRemover in pedido["itens"]:
                        pedido["itens"].remove(alimentoParaRemover)
                        for alimento in alimentos:
                            if alimento["nome"] == alimentoParaRemover:
                                pedido["total"] -= alimento["preco"]
                        print(f"Pedido {pedido["id"]} atualizado com sucesso: ")
                    else:
                        print("Item não encontrado no pedido.")
                    edicaoFinalizada = True
                    input("Pressione QUALQUER tecla para voltar a tela home\n")
                    
                elif decisao == "3":
                    edicaoFinalizada = True
                    break
                else:
                    print("Opção inválida, tente novamente...")
                    time.sleep(1)    

        if edicaoFinalizada == False:
            print("Pedido não encontrado, tente novamente...")

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
    print("|           CADASTRAR PEDIDO             |")
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
                            itensPedido.append(alimento)
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
    os.system(limparTela)
    print("__________________________________________")
    print("|                                        |")
    print("|           LISTA DE ALIMENTOS           |")
    print("|________________________________________|\n")

    for alimento in alimentos:
        print("|     Nome : ",alimento["nome"], " Categoria: ", alimento["categoria"], " Preço: ",alimento["preco"])
        print("|________________________________________|")
    input("Pressione QUALQUER tecla para voltar a tela home\n")

def listarAlimentosBuscados(usr):
    os.system(limparTela)
    print("__________________________________________")
    print("|                                        |")
    print("|        ALIMENTOS BUSCADOS              |")
    print("|________________________________________|\n")
    print("|     Usuario : ",usr["usuario"])

    for busca in alimentosBuscados:
        if busca["usuario"] == usr["usuario"]:
            print("|     Alimentos : ", busca["alimentos"])
    print("|________________________________________|\n")
    input("Pressione QUALQUER tecla para voltar a tela home\n")

def buscarAlimento(nomeUsuario,nomeAlimento):
    alimentoBuscado = []
    alimentoExistenteNoBanco = False
    os.system(limparTela)
    print("__________________________________________")
    print("|                                        |")
    print("|             BUSCAR ALIMENTO            |")
    print("|________________________________________|\n")
    
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
            
    busca = {
        "usuario": nomeUsuario,
        "alimentos": alimentoBuscado
    }
    alimentosBuscados.append(busca)
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
                    cadastrarPedido(usr)
                    break
                elif decisao == "3":
                    editarPedido(usr)
                    break
                elif decisao == "4":
                    excluirPedido(usr)
                    break
                elif decisao == "5":
                    print("Voltando...")
                    time.sleep(1)
                    break
                else:
                    print("Informe uma opção válida!")
                    time.sleep(1)           

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
    with open(arquivoUsuarios, "a") as f:
        f.write(f"{user['nome']},{user['usuario']},{user['senha']}\n")
    
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