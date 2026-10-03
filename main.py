"""Sistema de Notas - interface de terminal."""

import notas as n

MENU = """
----- SISTEMA DE NOTAS -----
1 - Registrar aluno
2 - Relatório final
3 - Buscar aluno
4 - Editar notas de um aluno
5 - Remover aluno
6 - Ranking
7 - Fechar sistema"""


# ---------- Entrada de dados ----------

def pedir_nome(mensagem="Digite o nome do aluno: "):
    while True:
        try:
            return n.validar_nome(input(mensagem))
        except ValueError as erro:
            print(erro)


def pedir_nota(numero):
    while True:
        try:
            return n.validar_nota(input(f"Digite a nota {numero}: "))
        except ValueError as erro:
            print(erro)


def pedir_notas():
    return [pedir_nota(i) for i in range(1, n.QTD_NOTAS + 1)]


# ---------- Exibição ----------

def mostrar_aluno(aluno):
    notas = ", ".join(f"{x:.1f}" for x in aluno["notas"])
    print(f"Aluno: {aluno['nome']}")
    print(f"  Notas: {notas}")
    print(f"  Média: {aluno['media']:.2f} | Situação: {aluno['situacao']}")


# ---------- Ações do menu ----------

def registrar(alunos):
    nome = pedir_nome()
    if n.encontrar_aluno(alunos, nome):
        print(f"Já existe um aluno chamado '{nome}'. Use a opção 4 para editar.")
        return False

    aluno = n.criar_aluno(nome, pedir_notas())
    n.adicionar_aluno(alunos, aluno)
    print(f"\nMédia final: {aluno['media']:.2f} - {aluno['situacao']}")
    return True


def relatorio(alunos):
    if not alunos:
        print("\nNenhum aluno registrado ainda.")
        return

    print("\n----- RELATÓRIO FINAL -----")
    for aluno in alunos:
        mostrar_aluno(aluno)

    r = n.resumo(alunos)
    print(f"\nTotal: {r['total']} aluno(s) | Aprovados: {r['aprovados']} | "
          f"Reprovados: {r['reprovados']} | Média da turma: {r['media_geral']:.2f}")


def buscar(alunos):
    termo = input("Digite o nome (ou parte dele): ")
    encontrados = n.buscar_por_nome(alunos, termo)
    if not encontrados:
        print("Nenhum aluno encontrado.")
        return
    print(f"\n{len(encontrados)} resultado(s):")
    for aluno in encontrados:
        mostrar_aluno(aluno)


def editar(alunos):
    aluno = n.encontrar_aluno(alunos, input("Nome do aluno a editar: "))
    if aluno is None:
        print("Aluno não encontrado.")
        return False

    print(f"Editando '{aluno['nome']}'. Digite as novas notas:")
    n.atualizar_notas(aluno, pedir_notas())
    print(f"\nNova média: {aluno['media']:.2f} - {aluno['situacao']}")
    return True


def remover(alunos):
    nome = input("Nome do aluno a remover: ")
    if n.encontrar_aluno(alunos, nome) is None:
        print("Aluno não encontrado.")
        return False

    if input(f"Confirma remover '{nome.strip()}'? (s/n): ").strip().lower() != "s":
        print("Operação cancelada.")
        return False

    n.remover_aluno(alunos, nome)
    print("Aluno removido.")
    return True


def mostrar_ranking(alunos):
    if not alunos:
        print("\nNenhum aluno registrado ainda.")
        return

    print("\n----- RANKING -----")
    for posicao, aluno in enumerate(n.ranking(alunos), start=1):
        print(f"{posicao}º {aluno['nome']} - {aluno['media']:.2f} ({aluno['situacao']})")


# ---------- Programa principal ----------

def main():
    alunos = n.carregar_alunos()
    if alunos:
        print(f"{len(alunos)} aluno(s) carregado(s) de {n.ARQUIVO_PADRAO}.")

    while True:
        print(MENU)
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            alterou = registrar(alunos)
        elif opcao == "2":
            relatorio(alunos)
            alterou = False
        elif opcao == "3":
            buscar(alunos)
            alterou = False
        elif opcao == "4":
            alterou = editar(alunos)
        elif opcao == "5":
            alterou = remover(alunos)
        elif opcao == "6":
            mostrar_ranking(alunos)
            alterou = False
        elif opcao == "7":
            print("Sistema encerrado.")
            break
        else:
            print("Opção inválida. Tente novamente.")
            alterou = False

        if alterou:
            n.salvar_alunos(alunos)


if __name__ == "__main__":
    main()
