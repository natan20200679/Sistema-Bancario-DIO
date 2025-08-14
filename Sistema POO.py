from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

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

def principal():

  saldo = 0
  limite = 500
  extrato_str = ""
  numero_saques = 0
  usuarios = []
  contas = []
  LIMITE_SAQUES = 3
  AGENCIA = "0001"

  while True:

    opcao = menu()

    if opcao == "d":

      valor = float(input("Informe o valor do depósito: "))
      deposito(usuarios)

    elif opcao == "s":

      valor = float(input("Informe o valor do saque: "))
      saque(usuarios)

    elif opcao == "e":

      extrato(usuarios)

    elif opcao == "nu":

      novo_usuario(usuarios)

    elif opcao == "nc":

      numero_conta = len(contas) + 1
      conta = nova_conta(contas, numero_conta, usuarios)

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

class Cliente:

  def __init__(self, endereco):

    self.endereco = endereco
    self.contas = []

  def realizar_transacao(self, conta, transacao):

    transacao.registrar(conta)

  def adicionar_conta(self, conta):

    self.contas.append(conta)

class PessoaFisica(Cliente):

  def __init__(self, nome, data_nascimento, cpf, endereco):

    super().__init__(endereco)
    self.nome = nome
    self.data_nascimento = data_nascimento
    self.cpf = cpf

class Conta:

  def __init__(self, numero, usuario):

    self._saldo = 0
    self._numero = numero
    self._agencia = "0001"
    self._usuario = usuario
    self._historico = Historico()

  def deposito(self, valor):

    if valor > 0:

      self._saldo += valor
      print(f"\n=== Depósito de R$ {valor:.2f} realizado com sucesso! ===")
      return True

    else:

      print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
      return False

  def saque(self, valor):

    excedeu_saldo = valor > self._saldo

    if excedeu_saldo:

      print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
      return False

    elif valor > 0:

      self._saldo -= valor
      return True

    else:

      print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
      return False

  @classmethod
  def nova_conta(cls, usuario, numero):

    return cls(numero, usuario)

  @property
  def saldo(self):

    return self._saldo

  @property
  def numero(self):

    return self._numero

  @property
  def agencia(self):

    return self._agencia

  @property
  def usuario(self):

    return self._usuario

  @property
  def historico(self):

    return self._historico

class ContaCorrente(Conta):

  def __init__(self, numero, usuario, limite = 500, limite_saques = 3):

    super().__init__(numero, usuario)
    self._limite = limite
    self._limite_saques = limite_saques

  def saque(self, valor):

    numero_saques = len([transacao for transacao in self.historico.transacoes
         if transacao["tipo"] == "Saque"])

    excedeu_limite = valor > self._limite
    excedeu_saques = numero_saques >= self._limite_saques

    if excedeu_limite:

      print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
      return False

    elif excedeu_saques:

      print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
      return False

    else:

      return super().saque(valor)

  def __str__(self):

    return f"""\
      Agência:\t{self.agencia}
      C/C:\t\t{self.numero}
      Titular:\t{self.usuario.nome}
    """

class Historico:

  def __init__(self):

    self._transacoes = []

  @property
  def transacoes(self):

    return self._transacoes

  def adicionar_transacao(self, transacao):

    self._transacoes.append(
      {
        "tipo": transacao.__class__.__name__,
        "valor": transacao.valor,
        "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
      }
    )

class Transacao(ABC):

  @property
  @abstractproperty
  def valor(self):

    pass

  @abstractclassmethod
  def registrar(self, conta):

    pass

class Saque(Transacao):

  def __init__(self, valor):

    self._valor = valor

  @property
  def valor(self):

    return self._valor

  def registrar(self, conta):

    sucesso_transacao = conta.saque(self.valor)

    if sucesso_transacao:

      conta.historico.adicionar_transacao(self)

class Deposito(Transacao):

  def __init__(self, valor):

    self._valor = valor

  @property
  def valor(self):

    return self._valor

  def registrar(self, conta):

    sucesso_transacao = conta.depositar(self.valor)

    if sucesso_transacao:

      conta.historico.adicionar_transacao(self)


def extrato(usuarios):

  cpf = input("Informe o CPF do cliente: ")
  usuario = filtro_usuario(cpf, usuarios)

  if not usuario:

    print("\n@@@ Cliente não encontrado! @@@")
    return

  conta = recuperar_conta_usuario(usuario)

  if not conta:

    return

  print("\n================ EXTRATO ================")
  transacoes = conta.historico.transacoes
  extrato_str = ""

  if not transacoes:

    extrato_str = "Não foram realizadas movimentações."

  else:

    for transacao in transacoes:

      extrato_str += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

  print(extrato_str)
  print(f"\nSaldo: R$ {conta.saldo:.2f}")
  print("==========================================")

def novo_usuario(usuarios):

  cpf = input("Informe o CPF (somente números): ")
  usuario = filtro_usuario(cpf, usuarios)

  if usuario:

    print("\n@@@ Já existe usuário com este CPF! @@@")
    return

  nome = input("informe o nome completo: ")
  data_nascimento = input("informe a data de nascimento (dd-mm-aaaa): ")
  endereco = input("informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
  cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
  usuarios.append(cliente)
  print("\n=== Usuário criado com sucesso! ===")

def filtro_usuario(cpf, usuarios):

  usuarios_filtrados = [usuario for usuario in usuarios if usuario.cpf == cpf] # Access cpf attribute directly

  if usuarios_filtrados:

    return usuarios_filtrados[0]

  else:

    return None

def nova_conta(contas, numero_conta, usuarios):

  cpf = input("Informe o CPF (somente números): ")
  usuario = filtro_usuario(cpf, usuarios)

  if usuario:

    conta = ContaCorrente.nova_conta(usuario=usuario, numero=numero_conta)
    contas.append(conta)
    usuario.contas.append(conta)
    print("\n=== Conta criada com sucesso! =====")
    return conta

  print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")
  return None

def lista_contas(contas):

  for conta in contas:

    linha = f"""\
      Agência:\t{conta.agencia}
      C/C:\t\t{conta.numero}
      Titular:\t{conta.usuario.nome}
    """

    print("=" * 100)
    print(linha)

def recuperar_conta_usuario(usuario):

  if not usuario.contas:

    print("\n@@@ Cliente não possui conta! @@@")
    return None

  # FIXME: não permite cliente escolher a conta
  return usuario.contas[0]

def deposito(usuarios):

  cpf = input("Informe o CPF do cliente: ")
  usuario = filtro_usuario(cpf, usuarios)

  if not usuario:

    print("\n@@@ Cliente não encontrado! @@@")
    return

  valor = float(input("Informe o valor do depósito: "))
  transacao = Deposito(valor)
  conta = recuperar_conta_usuario(usuario)

  if not conta:

    return

  usuario.realizar_transacao(conta, transacao)

def saque(usuarios): # Corrected the argument to users

  cpf = input("Informe o CPF do cliente: ")
  usuario = filtro_usuario(cpf, usuarios) # Corrected the argument to users

  if not usuario:

    print("\n@@@ Cliente não encontrado! @@@")

    return

  valor = float(input("Informe o valor do saque: "))
  transacao = Saque(valor)
  conta = recuperar_conta_usuario(usuario)

  if not conta:

    return

  usuario.realizar_transacao(conta, transacao)
