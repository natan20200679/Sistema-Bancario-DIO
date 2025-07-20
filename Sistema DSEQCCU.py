def menu():

  menu = """

  [d] Depositar
  [s] Sacar
  [e] Extrato
  [nc] Nova Conta
  [lc] Listar Contas
  [nu] Novo Usuário
  [q] Sair

=> """

  return input(menu)

def deposito(saldo, valor, extrato, /):

  if valor > 0:

    saldo += valor
    extrato += f"Depósito: R$ {valor:.2f}\n"
    print(f"\n=== Depósito de R$ {valor:.2f} realizado com sucesso! ===")

  else:

    print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

  return saldo, extrato

def saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques):

  excedeu_saldo = valor > saldo
  excedeu_limite = valor > limite
  excedeu_saques = numero_saques >= limite_saques

  if excedeu_saldo:

    print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

  elif excedeu_limite:

    print("\n@@@ Operação falhou! O valor do saque excede o limite! @@@")

  elif excedeu_saques:

    print("\n@@@ Operação falhou! Número máximo de saques diário excedido! @@@")

  elif valor > 0:

    saldo -= valor
    extrato += f"Saque: R$ {valor:.2f}\n"
    numero_saques += 1

  else:

    print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

  return saldo, extrato, numero_saques

def extrato(saldo, /, *, extrato):

  print("\n================ EXTRATO ================")
  print("Não foram realizadas movimentações." if not extrato else extrato)
  print(f"\nSaldo: R$ {saldo:.2f}")
  print("==========================================")

def novo_usuario(usuarios):

  cpf = input("Informe o CPF (somente números): ")
  usuario = filtro_usuario(cpf, usuarios)

  if usuario:

    print("\n@@@ Já existe 1 usuário com este CPF! @@@")

    return

  nome = input("informe o nome completo: ")
  data_nascimento = input("informe a data de nascimento (dd-mm-aaaa): ")
  endereco = input("informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

  usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

  print("\n=== Usuário criado com sucesso! ===")

def filtro_usuario(cpf, usuarios):

  usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]

  if usuarios_filtrados:

    return usuarios_filtrados[0]

  else:

    None

def nova_conta(agencia, numero_conta, usuarios):

  cpf = input("Informe o CPF (somente números): ")
  usuario = filtro_usuario(cpf, usuarios)

  if usuario:

    print("\n=== Conta criada com sucesso! ===")

    return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

  print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")

def lista_contas(contas):

  for conta in contas:

    linha = f"""\
      Agência:{conta['agencia']}
      C/C:{conta['numero_conta']}
      Titular:{conta['usuario']['nome']}
    """

    print("=" * 100)
    print(linha)

def principal():

  saldo = 0
  limite = 500
  extrato_str = "" # Renamed the variable here
  numero_saques = 0
  usuarios = []
  contas = []
  LIMITE_SAQUES = 3
  AGENCIA = "0001"

  while True:

    opcao = menu()

    if opcao == "d":

      valor = float(input("Informe o valor do depósito: "))

      saldo, extrato_str = deposito(saldo, valor, extrato_str) # Use the new variable name

    elif opcao == "s":

      valor = float(input("Informe o valor do saque: "))

      saldo, extrato_str, numero_saques = saque(saldo = saldo, valor = valor, extrato = extrato_str, limite = limite, # Use the new variable name
                             numero_saques = numero_saques, limite_saques = LIMITE_SAQUES)

    elif opcao == "e":

      extrato(saldo, extrato = extrato_str) # Use the new variable name

    elif opcao == "nu":

      novo_usuario(usuarios)

    elif opcao == "nc":

      numero_conta = len(contas) + 1
      conta = nova_conta(AGENCIA, numero_conta, usuarios)

      if conta:

        contas.append(conta)

    elif opcao == "lc":

      lista_contas(contas)

      if not contas:

        print("\n=== Nenhuma conta cadastrada! ===")

    elif opcao == "q":

      break

    else:

      print("Operação inválida! Por favor selecione novamente a operação desejada.")

principal()
