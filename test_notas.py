import pytest

import notas as n


def aluno_exemplo(nome="Ana", valores=(10, 8, 6, 7, 9)):
    return n.criar_aluno(nome, list(valores))


# ---------- Validação ----------

@pytest.mark.parametrize("entrada, esperado", [("7", 7.0), ("7,5", 7.5), (" 10 ", 10.0), (0, 0.0)])
def test_validar_nota_valida(entrada, esperado):
    assert n.validar_nota(entrada) == esperado


@pytest.mark.parametrize("entrada", ["abc", "", "-1", "10.1", "11"])
def test_validar_nota_invalida(entrada):
    with pytest.raises(ValueError):
        n.validar_nota(entrada)


def test_validar_nome():
    assert n.validar_nome("  Ana  ") == "Ana"
    with pytest.raises(ValueError):
        n.validar_nome("   ")


# ---------- Cálculos ----------

def test_calcular_media():
    assert n.calcular_media([10, 8, 6, 7, 9]) == 8.0


def test_calcular_media_sem_notas():
    with pytest.raises(ValueError):
        n.calcular_media([])


@pytest.mark.parametrize("media, esperado", [(6.0, "Aprovado"), (9.5, "Aprovado"), (5.99, "Reprovado"), (0, "Reprovado")])
def test_definir_situacao(media, esperado):
    assert n.definir_situacao(media) == esperado


def test_criar_aluno():
    aluno = aluno_exemplo()
    assert aluno["nome"] == "Ana"
    assert aluno["media"] == 8.0
    assert aluno["situacao"] == "Aprovado"


# ---------- Consultas ----------

def test_encontrar_aluno_ignora_caixa():
    alunos = [aluno_exemplo("Ana")]
    assert n.encontrar_aluno(alunos, "  ana ") is alunos[0]
    assert n.encontrar_aluno(alunos, "Bia") is None


def test_buscar_por_nome_parcial():
    alunos = [aluno_exemplo("Ana Souza"), aluno_exemplo("Mariana"), aluno_exemplo("Bruno")]
    assert [a["nome"] for a in n.buscar_por_nome(alunos, "ana")] == ["Ana Souza", "Mariana"]


def test_ranking_ordem_decrescente():
    alunos = [
        aluno_exemplo("A", (5, 5, 5, 5, 5)),
        aluno_exemplo("B", (9, 9, 9, 9, 9)),
        aluno_exemplo("C", (7, 7, 7, 7, 7)),
    ]
    assert [a["nome"] for a in n.ranking(alunos)] == ["B", "C", "A"]


def test_resumo():
    alunos = [aluno_exemplo("A", (10,) * 5), aluno_exemplo("B", (2,) * 5)]
    r = n.resumo(alunos)
    assert (r["total"], r["aprovados"], r["reprovados"], r["media_geral"]) == (2, 1, 1, 6.0)


def test_resumo_lista_vazia():
    assert n.resumo([]) == {"total": 0, "aprovados": 0, "reprovados": 0, "media_geral": 0.0}


# ---------- Alterações ----------

def test_adicionar_aluno_duplicado():
    alunos = []
    n.adicionar_aluno(alunos, aluno_exemplo("Ana"))
    with pytest.raises(ValueError):
        n.adicionar_aluno(alunos, aluno_exemplo("ANA"))
    assert len(alunos) == 1


def test_atualizar_notas_recalcula():
    aluno = aluno_exemplo("Ana", (10, 10, 10, 10, 10))
    n.atualizar_notas(aluno, [2, 2, 2, 2, 2])
    assert aluno["media"] == 2.0
    assert aluno["situacao"] == "Reprovado"
    assert aluno["nome"] == "Ana"


def test_remover_aluno():
    alunos = [aluno_exemplo("Ana")]
    assert n.remover_aluno(alunos, "ana") is True
    assert alunos == []
    assert n.remover_aluno(alunos, "ana") is False


# ---------- Persistência ----------

def test_salvar_e_carregar(tmp_path):
    arquivo = tmp_path / "alunos.json"
    alunos = [aluno_exemplo("José"), aluno_exemplo("Ana")]
    n.salvar_alunos(alunos, arquivo)
    assert n.carregar_alunos(arquivo) == alunos


def test_carregar_arquivo_inexistente(tmp_path):
    assert n.carregar_alunos(tmp_path / "nao_existe.json") == []


def test_carregar_arquivo_corrompido(tmp_path):
    arquivo = tmp_path / "alunos.json"
    arquivo.write_text("{ isso não é json", encoding="utf-8")
    assert n.carregar_alunos(arquivo) == []
