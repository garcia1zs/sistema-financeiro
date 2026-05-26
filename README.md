# sistema-financeiro

from supabase import create_client

# =========================
# CONEXÃO SUPABASE
# =========================

SUPABASE_URL = "https://tsgyaxeveplqgtyrlxiv.supabase.co"
SUPABASE_KEY = "sb_publishable_8uJUbwg6gyn_CX0o1oub5Q_HJUwbPB8"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# =========================
# CLASSE PESSOA
# =========================

class Pessoa:

    def __init__(self, nome, cpf, nascimento, endereco):
        self.nome = nome
        self.cpf = cpf
        self.nascimento = nascimento
        self.endereco = endereco

# =========================
# CLASSE DISCIPLINA
# =========================

class Disciplina:

    def __init__(self, nome, carga_horaria):
        self.nome = nome
        self.carga_horaria = carga_horaria

# =========================
# CLASSE NOTA
# =========================

class Nota:

    def __init__(self, disciplina, valor):
        self.disciplina = disciplina
        self.valor = valor

# =========================
# CLASSE ALUNO
# =========================

class Aluno(Pessoa):

    def __init__(self, nome, cpf, nascimento,
                 endereco, matricula):

        super().__init__(nome, cpf, nascimento, endereco)

        self.matricula = matricula
        self.notas = []

    def adicionar_nota(self, nota):
        self.notas.append(nota)

    def calcular_media(self):

        if len(self.notas) == 0:
            return 0

        soma = sum([nota.valor for nota in self.notas])

        return soma / len(self.notas)

    def salvar_no_supabase(self):

        pessoa_data = {
            "nome": self.nome,
            "cpf": self.cpf,
            "nascimento": self.nascimento,
            "endereco": self.endereco
        }

        pessoa = supabase.table("pessoas").insert(pessoa_data).execute()

        pessoa_id = pessoa.data[0]["id"]

        aluno_data = {
            "pessoa_id": pessoa_id,
            "matricula": self.matricula
        }

        supabase.table("aluno").insert(aluno_data).execute()

        print("\nAluno salvo com sucesso!")

# =========================
# CLASSE PROFESSOR
# =========================

class Professor(Pessoa):

    def __init__(self, nome, cpf, nascimento,
                 endereco, especialidade, salario):

        super().__init__(nome, cpf, nascimento, endereco)

        self.especialidade = especialidade
        self.salario = salario

    def salvar_no_supabase(self):

        pessoa_data = {
            "nome": self.nome,
            "cpf": self.cpf,
            "nascimento": self.nascimento,
            "endereco": self.endereco
        }

        pessoa = supabase.table("pessoas").insert(pessoa_data).execute()

        pessoa_id = pessoa.data[0]["id"]

        professor_data = {
            "pessoa_id": pessoa_id,
            "especialidade": self.especialidade,
            "salario": self.salario
        }

        supabase.table("professor").insert(professor_data).execute()

        print("\nProfessor salvo com sucesso!")

# =========================
# CLASSE TURMA
# =========================

class Turma:

    def __init__(self, nome, ano_letivo):

        self.nome = nome
        self.ano_letivo = ano_letivo
        self.alunos = []

    def adicionar_aluno(self, aluno):
        self.alunos.append(aluno)

    def listar_alunos(self):

        print(f"\nTurma: {self.nome}")

        for aluno in self.alunos:
            print(aluno.nome)

# =========================
# CLASSE DIREÇÃO
# =========================

class Direcao:

    def __init__(self, diretor):
        self.diretor = diretor

    def aprovar_aluno(self, aluno):

        media = aluno.calcular_media()

        print(f"\nMédia do aluno: {media}")

        if media >= 6:
            print(f"{aluno.nome} foi aprovado!")
        else:
            print(f"{aluno.nome} foi reprovado!")

# =========================
# MENU
# =========================

alunos = []
professores = []
turmas = []

while True:

    print("""
==============================
      SISTEMA ESCOLAR
==============================

1 - Cadastrar aluno
2 - Cadastrar professor
3 - Criar turma
4 - Listar alunos
5 - Listar professores
6 - Listar turmas
7 - Sair

==============================
""")

    opcao = input("Escolha uma opção: ")

    # =========================
    # CADASTRAR ALUNO
    # =========================

    if opcao == "1":

        print("\n=== CADASTRO DE ALUNO ===")

        nome = input("Nome: ")
        cpf = input("CPF: ")
        nascimento = input("Nascimento: ")
        endereco = input("Endereço: ")
        matricula = input("Matrícula: ")

        aluno = Aluno(
            nome,
            cpf,
            nascimento,
            endereco,
            matricula
        )

        alunos.append(aluno)

        salvar = input("Salvar no Supabase? (s/n): ")

        if salvar.lower() == "s":
            aluno.salvar_no_supabase()

        print("\nAluno cadastrado!")

    # =========================
    # CADASTRAR PROFESSOR
    # =========================

    elif opcao == "2":

        print("\n=== CADASTRO DE PROFESSOR ===")

        nome = input("Nome: ")
        cpf = input("CPF: ")
        nascimento = input("Nascimento: ")
        endereco = input("Endereço: ")
        especialidade = input("Especialidade: ")
        salario = float(input("Salário: "))

        professor = Professor(
            nome,
            cpf,
            nascimento,
            endereco,
            especialidade,
            salario
        )

        professores.append(professor)

        salvar = input("Salvar no Supabase? (s/n): ")

        if salvar.lower() == "s":
            professor.salvar_no_supabase()

        print("\nProfessor cadastrado!")

    # =========================
    # CRIAR TURMA
    # =========================

    elif opcao == "3":

        print("\n=== CRIAR TURMA ===")

        nome = input("Nome da turma: ")
        ano = int(input("Ano letivo: "))

        turma = Turma(nome, ano)

        turmas.append(turma)

        print("\nTurma criada!")

    # =========================
    # LISTAR ALUNOS
    # =========================

    elif opcao == "4":

        print("\n=== LISTA DE ALUNOS ===")

        for aluno in alunos:
            print(f"""
Nome: {aluno.nome}
Matrícula: {aluno.matricula}
""")

    # =========================
    # LISTAR PROFESSORES
    # =========================

    elif opcao == "5":

        print("\n=== LISTA DE PROFESSORES ===")

        for professor in professores:
            print(f"""
Nome: {professor.nome}
Especialidade: {professor.especialidade}
""")

    # =========================
    # LISTAR TURMAS
    # =========================

    elif opcao == "6":

        print("\n=== LISTA DE TURMAS ===")

        for turma in turmas:
            print(f"""
Turma: {turma.nome}
Ano: {turma.ano_letivo}
""")

    # =========================
    # SAIR
    # =========================

    elif opcao == "7":

        print("\nEncerrando sistema...")
        break

    else:
        print("\nOpção inválida!")
