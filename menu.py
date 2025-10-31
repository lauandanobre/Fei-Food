
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
    print("Pedidos de ",usr["usuario"],"\n")
    print("1) Visualizar pedidos")
    print("2) Cadastrar pedido")
    print("3) Editar pedido")
    print("4) Excluir pedido")
    print("5) Voltar")
