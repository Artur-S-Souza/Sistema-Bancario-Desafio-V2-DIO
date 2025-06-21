usuarios = []
contas = []
numero_de_contas = 1
AGENCIA = "0001"
SAQUES_DIARIOS = 3
LIMITE_DE_SAQUE = 500


def exibir_menu(menu):
    print(menu)


def obter_opcao():
    return input()


def realizar_saque(*, quantidade_de_saques: int, saques_diarios: int, saldo: float, limite_saque: float, extrato: str):
    valor_do_saque = float(input("Digite o valor do saque: "))
    if quantidade_de_saques >= saques_diarios:
        print("Número máximo de saques diários atingido.")
        return 0
    elif quantidade_de_saques < saques_diarios:
        if valor_do_saque > saldo:
            print("Saldo insuficiente.")
        elif valor_do_saque > limite_saque:
            print(f"Límite de saque não permitido, seu límite é de R$ {limite_saque:.2f}.")
        elif valor_do_saque <= limite_saque:
            saldo -= valor_do_saque
            quantidade_de_saques += 1
            print(f"Saque de R$ {valor_do_saque:.2f} realizado com sucesso.")
    return valor_do_saque


def realizar_deposito(saldo: float, /):
    valor_do_deposito = float(input("Digite o valor do depósito: "))
    while valor_do_deposito == 0:
        print("Valor de deposito inválido, tente novamente.")
        valor_do_deposito = float(input("Digite o valor do deposito: "))
    saldo += valor_do_deposito
    print(f"Depósito de R$ {valor_do_deposito:.2f} realizado com sucesso.")
    return saldo, valor_do_deposito


def exibir_extrato(extrato: str, /, *, saldo: float):
    if not extrato:
        print("Nenhuma transação realizada.")
    else:
        print("Extrato:")
        print(extrato)
        print(f"Saldo: R$ {saldo:.2f}")


def cadastrar_usuario():
    while True:
        nome = input("Digite o nome do usuário: ").lower().replace(" ", "_")
        cpf = input("Digite o CPF do usuário: ").replace(".", "").replace("-", "")
        data_nascimento = input("Digite a data de nascimento (DD/MM/AAAA): ")
        endereco = input("Digite o endereço do usuário: ")
        if cpf_invalido(cpf):
            print("Cadastro não realizado devido a CPF inválido.")
            return None
        if usuario_existe(usuarios, cpf):
            print("Usuário já cadastrado com este CPF.")
            return None
        print(f"Usuário {nome} cadastrado com sucesso!")
        return {f"usuario_{nome}": {"nome": nome, "cpf": cpf, "data_nascimento": data_nascimento, "endereco": endereco}}


def usuario_existe(usuarios, cpf):
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return True
    return False


def cpf_invalido(cpf):
    if len(cpf) != 11 or not cpf.isdigit():
        print("CPF inválido. Deve conter 11 dígitos numéricos.")
        return True
    return False


def selecionar_usuario():
    cpf = input("Digite o CPF do usuário: ").replace(".", "").replace("-", "")
    for usuario in usuarios:
        for u in usuario.values():
            if u["cpf"] == cpf:
                print(f"Usuário encontrado: {u['nome']}")
                return u
    print("Usuário não encontrado.")
    return None


def criar_conta():
    global numero_de_contas
    usuario = selecionar_usuario()
    if not usuario:
        print("Conta não criada, usuário não encontrado.")
        return None
    nome_da_conta = AGENCIA + str(numero_de_contas) + usuario["nome"]
    numero_de_contas += 1
    conta = {"conta": {"numero_da_conta": nome_da_conta, "agencia": AGENCIA, "usuario": usuario}}
    return conta



def main():
    menu = {
        "tela_de_cadastro": """
        ## Sistema Bancário - Desafio DIO##
        #         1- Acessar Conta        #
        #       2- Cadastrar Usuário      #
        #          3- Criar Conta         #
        ###################################
        """,
        "menu_principal": """
        ## Sistema Bancário - Desafio DIO##
        #             1- Sacar            #
        #           2- Depositar          #
        #            3- Extrato           #
        #             0- Sair             #
        ###################################
        """}

    extrato = ""
    quantidade_de_saques = 0
    saldo = 0

    while True:
        exibir_menu(menu["tela_de_cadastro"])
        opcao = obter_opcao()

        if opcao == "1":
            if not usuarios:
                print("Nenhum usuário cadastrado. Por favor, cadastre um usuário primeiro.")
                continue
            while True:
                exibir_menu(menu["menu_principal"])
                opcao_principal = obter_opcao()
                print(saldo)
                if opcao_principal == "1":
                    valor_sacado = realizar_saque(extrato=extrato, saldo=saldo,
                                                  quantidade_de_saques=quantidade_de_saques,
                                                  saques_diarios=SAQUES_DIARIOS, limite_saque=LIMITE_DE_SAQUE)
                    saldo -= valor_sacado
                    extrato += f"Saque: R$ {valor_sacado:.2f}\n"
                    continue
                elif opcao_principal == "2":
                    saldo, valor_do_deposito = realizar_deposito(saldo)
                    extrato += f"Depósito: R$ {valor_do_deposito:.2f}\n"
                    continue
                elif opcao_principal == "3":
                    exibir_extrato(extrato, saldo=saldo)
                    continue
                elif opcao_principal == "0":
                    print("Saindo do sistema. Até logo!")
                    return
                else:
                    print("Opção inválida. Tente novamente.")
        elif opcao == "2":
            usuarios.append(cadastrar_usuario())
        elif opcao == "3":
            conta = criar_conta()
            contas.append(conta) if conta is not None else None
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()