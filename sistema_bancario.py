from datetime import datetime
import getpass

class Conta:
    def __init__(self, agencia, numero_conta, usuario, senha):
        self.agencia = agencia
        self.numero_conta = numero_conta
        self.usuario = usuario
        self.senha = senha
        self.valorConta = 0.0
        self.saques = []
        self.depositos = []
        self.limiteDiario = 3

    def deposito(self, valor):
        if valor > 0:
            self.valorConta += valor
            data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            self.depositos.append((data, valor))
            print(f"O valor de R${valor:.2f} foi depositado com sucesso.")
        else:
            print("Erro: O valor deve ser positivo e maior que zero.")

    def realizar_saque(self, valor):
        if len(self.saques) >= self.limiteDiario:
            print("Erro: Você já atingiu o limite diário de saques!")
        elif valor <= 0:
            print("Erro: O valor deve ser maior que zero!")
        elif self.valorConta < valor:
            print("Erro: Saldo insuficiente para saque!")
        else:
            self.valorConta -= valor
            data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            self.saques.append((data, valor))
            print(f"Saque de R${valor:.2f} realizado com sucesso!")

    def exibir_extrato(self):
        print("\n------ EXTRATO COMPLETO ------")

        print("\n>> DEPÓSITOS:")
        if self.depositos:
            for i, (data, valor) in enumerate(self.depositos, 1):
                print(f"{i}. Data: {data} | Valor: R${valor:.2f}")
        else:
            print("Nenhum depósito realizado.")

        print("\n>> SAQUES:")
        if self.saques:
            for i, (data, valor) in enumerate(self.saques, 1):
                print(f"{i}. Data: {data} | Valor: R${valor:.2f}")
        else:
            print("Nenhum saque realizado.")

        print(f"\n>> Saldo atual: R${self.valorConta:.2f}")
        print("------------------------------")

class bancoDio:
    def __init__(self):
        self.contas = {} 
        self.usuario_logado = None  

    def criar_conta(self):
        print("\n----- Criar Conta -----")
        agencia = input("Informe a agência: ").strip()
        numero_conta = input("Informe o número da conta: ").strip()

        if numero_conta in self.contas:
            print("Erro: Conta já existe!")
            return

        usuario = input("Informe o nome do usuário: ").strip()
        senha = getpass.getpass("Crie uma senha: ")

        conta = Conta(agencia, numero_conta, usuario, senha)
        self.contas[numero_conta] = conta
        print(f"Conta criada com sucesso para o usuário {usuario}!\n")

    def login_conta(self):
        print("\n----- Login -----")
        numero_conta = input("Informe o número da conta: ").strip()
        senha = getpass.getpass("Informe a senha: ")

        conta = self.contas.get(numero_conta)
        if conta and conta.senha == senha:
            self.usuario_logado = conta
            print(f"Login realizado com sucesso! Bem-vindo(a), {conta.usuario}.\n")
            return True
        else:
            print("Erro: Número da conta ou senha inválidos.\n")
            return False

    def logout(self):
        if self.usuario_logado:
            print(f"Usuário {self.usuario_logado.usuario} desconectado.")
            self.usuario_logado = None

def executar_opcao(opcao, banco):
    if banco.usuario_logado is None:
        # Menu inicial: criar conta, login ou sair
        if opcao == "1":
            banco.criar_conta()
            return True
        elif opcao == "2":
            if banco.login_conta():
                return True
            else:
                return True
        elif opcao == "0":
            print("Obrigado por usar o BancoDio. Até logo!")
            return False
        else:
            print("Opção inválida, tente novamente.")
            return True
    else:
        # Menu da conta logada
        conta = banco.usuario_logado

        if opcao == "1":
            try:
                valor = float(input("Digite o valor que deseja depositar: "))
                conta.deposito(valor)
            except ValueError:
                print("Erro: Digite um valor numérico válido.")
            return True

        elif opcao == "2":
            try:
                valor = float(input("Digite o valor que deseja sacar: "))
                conta.realizar_saque(valor)
            except ValueError:
                print("Erro: Digite um valor numérico válido.")
            return True

        elif opcao == "3":
            conta.exibir_extrato()
            return True

        elif opcao == "4":
            banco.logout()
            return True

        elif opcao == "0":
            print("Obrigado por usar o BancoDio. Até logo!")
            return False

        else:
            print("Opção inválida, tente novamente.")
            return True

# Programa principal
def main():
    banco = bancoDio()
    while True:
        if banco.usuario_logado is None:
            print("\n------ BancoDio ------")
            print("1 - Criar Conta")
            print("2 - Login")
            print("0 - Sair")
        else:
            print(f"\n------ BancoDio - Usuário: {banco.usuario_logado.usuario} ------")
            print("1 - Depositar")
            print("2 - Sacar")
            print("3 - Extrato")
            print("4 - Logout")
            print("0 - Sair")

        opcao = input("Escolha uma opção: ")
        if not executar_opcao(opcao, banco):
            break

if __name__ == "__main__":
    main()
