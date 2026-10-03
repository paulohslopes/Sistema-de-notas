# 📚 Sistema de Notas

Sistema de terminal em Python para gerenciar notas de alunos: registra, calcula médias, gera relatórios e salva tudo em arquivo JSON.

## Funcionalidades

- Registro de vários alunos com 5 notas cada
- Validação de entradas (nome não vazio, notas entre 0 e 10, aceita vírgula decimal)
- Cálculo automático de média e situação (aprovado com média ≥ 6)
- Relatório final com resumo da turma
- Busca por nome (parcial, sem diferenciar maiúsculas)
- Edição de notas e remoção de alunos (com confirmação)
- Ranking por média
- Persistência automática em `alunos.json`
- Testes automatizados com `pytest`

## Como executar

Requer Python 3.8+.

```bash
python main.py
```

## Como rodar os testes

```bash
pip install -r requirements.txt
pytest
```

## Estrutura

```
sistema-de-notas/
├── main.py          # interface de terminal (menu e entrada/saída)
├── notas.py         # lógica: validação, cálculos, busca e persistência
├── test_notas.py    # testes automatizados
├── requirements.txt
└── README.md
```

A lógica fica separada da interface, o que torna o código testável e reutilizável (por exemplo, em uma futura versão web).

## Exemplo de uso

```
----- SISTEMA DE NOTAS -----
1 - Registrar aluno
2 - Relatório final
3 - Buscar aluno
4 - Editar notas de um aluno
5 - Remover aluno
6 - Ranking
7 - Fechar sistema
```

## Próximos passos

- Interface web com Flask ou Streamlit
- Exportar relatório para CSV/PDF
- Quantidade de notas e média de aprovação configuráveis pelo usuário

## Autor

Paulo Henrique — [GitHub](https://github.com/paulohslopes)
