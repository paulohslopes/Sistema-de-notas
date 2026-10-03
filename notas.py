"""Lógica do Sistema de Notas: cálculos, validações e persistência em JSON.

Este módulo não faz nenhum print/input, o que facilita os testes automatizados.
"""

import json
from pathlib import Path

QTD_NOTAS = 5
MEDIA_APROVACAO = 6.0
ARQUIVO_PADRAO = Path("alunos.json")


# ---------- Validação ----------

def validar_nota(valor):
    """Converte o valor para float e garante que está entre 0 e 10.

    Aceita vírgula como separador decimal. Lança ValueError se for inválido.
    """
    try:
        nota = float(str(valor).strip().replace(",", "."))
    except ValueError:
        raise ValueError("Entrada inválida. Digite um número.") from None

    if not 0 <= nota <= 10:
        raise ValueError("A nota deve estar entre 0 e 10.")
    return nota


def validar_nome(nome):
    """Remove espaços extras e garante que o nome não é vazio."""
    nome = str(nome).strip()
    if not nome:
        raise ValueError("O nome não pode ficar vazio.")
    return nome


# ---------- Cálculos ----------

def calcular_media(notas):
    if not notas:
        raise ValueError("É necessário ao menos uma nota.")
    return sum(notas) / len(notas)


def definir_situacao(media):
    return "Aprovado" if media >= MEDIA_APROVACAO else "Reprovado"


def criar_aluno(nome, notas):
    """Monta o dicionário de um aluno já com média e situação calculadas."""
    media = calcular_media(notas)
    return {
        "nome": validar_nome(nome),
        "notas": list(notas),
        "media": media,
        "situacao": definir_situacao(media),
    }


# ---------- Consultas ----------

def encontrar_aluno(alunos, nome):
    """Busca exata (ignorando maiúsculas/minúsculas). Retorna o aluno ou None."""
    alvo = nome.strip().lower()
    for aluno in alunos:
        if aluno["nome"].lower() == alvo:
            return aluno
    return None


def buscar_por_nome(alunos, termo):
    """Retorna todos os alunos cujo nome contém o termo (sem diferenciar caixa)."""
    termo = termo.strip().lower()
    return [a for a in alunos if termo in a["nome"].lower()]


def ranking(alunos):
    """Retorna os alunos ordenados da maior para a menor média."""
    return sorted(alunos, key=lambda a: a["media"], reverse=True)


def resumo(alunos):
    """Estatísticas gerais da turma."""
    total = len(alunos)
    aprovados = sum(1 for a in alunos if a["situacao"] == "Aprovado")
    return {
        "total": total,
        "aprovados": aprovados,
        "reprovados": total - aprovados,
        "media_geral": calcular_media([a["media"] for a in alunos]) if total else 0.0,
    }


# ---------- Alterações ----------

def adicionar_aluno(alunos, aluno):
    """Adiciona o aluno à lista. Lança ValueError se o nome já existir."""
    if encontrar_aluno(alunos, aluno["nome"]):
        raise ValueError(f"Já existe um aluno chamado '{aluno['nome']}'.")
    alunos.append(aluno)


def atualizar_notas(aluno, novas_notas):
    """Atualiza as notas do aluno e recalcula média e situação."""
    aluno.update(criar_aluno(aluno["nome"], novas_notas))


def remover_aluno(alunos, nome):
    """Remove o aluno pelo nome. Retorna True se removeu, False se não achou."""
    aluno = encontrar_aluno(alunos, nome)
    if aluno is None:
        return False
    alunos.remove(aluno)
    return True


# ---------- Persistência ----------

def salvar_alunos(alunos, caminho=ARQUIVO_PADRAO):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(alunos, f, ensure_ascii=False, indent=2)


def carregar_alunos(caminho=ARQUIVO_PADRAO):
    """Carrega os alunos do JSON. Retorna lista vazia se não existir ou estiver corrompido."""
    caminho = Path(caminho)
    if not caminho.exists():
        return []
    try:
        with open(caminho, encoding="utf-8") as f:
            dados = json.load(f)
    except (json.JSONDecodeError, OSError):
        return []
    return dados if isinstance(dados, list) else []
