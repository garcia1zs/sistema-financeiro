from datetime import datetime
import json
import random as rd
def carregarDados():
    try:
        with open("projeto-financeiro/historicoDeTransacoes.json", "r", encoding="utf-8") as arq:
            return json.load(arq)

    except FileNotFoundError:
        return {
            "saldo": 0,
            "entrou": 0,
            "saiu": 0,
            "transacoes": []
        }
    
dados = carregarDados()

def menu():
    print("""
        1-Adcionar Transaçoes
        2-Mostrar Saldo
        3-Listar Histórico
        4- Salvar em Arquivo
        5 -Filtrar
        6-Sair""")

def adicionarTransacoes(dados):
    data = datetime.now()
    codigo = rd.randint(000,9999)
    tipo = input("Qual o tipo de transação -> Entrada ou Saida? ")
    if tipo == 'Entrada':
        while True:
            try:
                entradas = float(input("Entradas: "))
                break
            except ValueError:
                print("Valor digitado inválido...")

        dados["saldo"] += entradas
        dados["entrou"] += entradas
        
        motivo = input("Motivo: ")

        dados["transacoes"].append({"tipo": tipo,
                                    "valor": entradas,
                                    "motivo" : motivo,
                                    "data" : f"{data.strftime('%d/%m/%Y')} ",
                                    "codigo" : codigo
                                    })
        salvarArquivo()

    elif tipo == 'Saida':
        while True:
            try:
                saidas = float(input("Saidas: "))
                break
            except ValueError:
                print("Valor digitado inválido...")
        motivo = input("Motivo: ")
        

        dados['saldo'] -= saidas
        dados['saiu'] += saidas

        dados["transacoes"].append(
            {"tipo": tipo,
              "valor": saidas,
              "motivo" : motivo,
              "data" : f"{data.strftime('%d/%m/%Y')} ",
              "codigo": codigo 
              })
        salvarArquivo()
    
def mostrarSaldo(dados):
    print(f"Entradas: {dados['entrou']}")
    print(f"Saiu: {dados['saiu']}")
    print(f"Saldo: {dados['saldo']}")

def listaHistorico():
    for t in dados['transacoes']:
        print(f"""
Tipo: {t['tipo']}
Valor: R$ {t['valor']:.2f}
Motivo: {t['motivo']}
Data: {t['data']}
Código: {t['codigo']}
""")
        
def filtrar():

    filtro = int(input("Digite 1 para Entradas e 2 para Saídas: "))
    if filtro == 1:
        tipo = "Entrada"
    elif filtro == 2:
        tipo = "Saida"
    else:
        print("Você digitou algo inválido.")
        return

    encontrou = False

    for c in dados['transacoes']:
        if c['tipo'] == tipo:
            print(f"""
Tipo: {c['tipo']}
Valor: R$ {c['valor']:.2f}
Descrição: {c['motivo']}
Código: {c['codigo']}
""")
            encontrou = True

    if not encontrou:
        print("Nenhuma transação encontrada.")

def salvarArquivo():
    with open("projeto-financeiro/historicoDeTransacoes.json", "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)

    print("Salvo com sucesso...")

def alterarTransacao(dados):
    acao = input("Oque voce deseja fazer, 1-Remover transacao / 2-Alterar transacao")
    if acao == "1":
        print(dados)
        codigo = int(input("Digite o código da transação que deseja remover: "))
        for t in dados['transacoes']:
            if t['codigo'] == codigo:
                if t['tipo'] == 'Entrada':
                    dados['saldo'] -= t['valor']
                    dados['entrou'] -= t['valor']
                elif t['tipo'] == 'Saida':
                    dados['saldo'] += t['valor']
                    dados['saiu'] -= t['valor']
                dados['transacoes'].remove(t)
                print("Transação removida com sucesso.")
                salvarArquivo()
                return


def main():
    carregarDados()
    while True: 
        menu()
        op = input("Digite a sua escolha: ")
        match op:
            case "1":
                adicionarTransacoes(dados)
            case "2":
                mostrarSaldo(dados)
            case "3":
                listaHistorico()
            case "4":
                salvarArquivo()
            case "5":
                filtrar()
            case "6":
                certeza = input("Tem certeza que deseja sair? ").lower()
                if certeza and certeza[0] == 's':
                    break


