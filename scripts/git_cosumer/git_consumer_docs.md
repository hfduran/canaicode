# 📊 Exportador de Commits Git para CSV (via Python)

Este script em Python extrai commits de um repositório Git local, filtrando por um intervalo de datas fornecido pelo usuário, e exporta os dados em formato CSV usando `pandas`.

---

## ✅ Requisitos

Antes de executar o script, certifique-se de que seu sistema possui:

- **Python 3.10 ou superior**
- **Git** instalado
- **pip** (gerenciador de pacotes do Python)

---

## 📦 Instalação das Bibliotecas

O script depende das seguintes bibliotecas Python:

- [`GitPython`](https://pypi.org/project/GitPython/)
- [`pandas`](https://pypi.org/project/pandas/)
- [`pydantic`](https://pypi.org/project/pydantic/)

Para instalá-las, execute:

```bash
pip install gitpython pandas pydantic
```

---

## 📁 Estrutura do Script

1. Crie um arquivo chamado `git_consumer.py`.
2. Cole o código Python completo fornecido neste script.
3. Garanta que você tenha um repositório Git clonado em seu computador.

---

## 🚀 Executando o Script

No terminal, navegue até a pasta onde está o script:

```bash
cd caminho/para/o/script
```

E execute:

```bash
python git_consumer.py
```

---

## 💬 Entradas do Usuário

Durante a execução, o script pedirá:

- **Caminho do repositório Git local**  
  Exemplo: `C:\Users\SeuUsuario\projetos\meu-repositorio`

- **Data inicial** no formato `YYYY-MM-DD`  
  Exemplo: `2024-07-01`

- **Data final** no formato `YYYY-MM-DD`  
  Exemplo: `2024-07-05`

---

## 📄 Saída Gerada

Se houver commits no intervalo especificado, será criado um arquivo chamado:

```
commits_{data_inicial}_a_{data_final}.csv
```

Exemplo:

```
commits_2024-07-01_a_2024-07-05.csv
```

### Colunas do CSV:

| hash | repository | date | author | language | added_lines | removed_lines |
| ---- | ---------- | ---- | ------ | -------- | ----------- | ------------- |

Cada linha representa um arquivo modificado em um commit.

---

## 🧪 Teste Rápido

Você pode testar o script clonando um repositório de código aberto:

```bash
git clone https://github.com/git/git.git
cd git
```

Use o caminho dessa pasta como entrada no script.

---

## ❗ Possíveis Erros e Soluções

| Erro                                              | Causa Provável                                 | Solução                                       |
| ------------------------------------------------- | ---------------------------------------------- | --------------------------------------------- |
| `Erro: caminho do repositório inválido.`          | Caminho informado não contém um `.git` válido. | Verifique se é uma pasta com repositório Git. |
| `Data inválida.`                                  | Data fora do formato `YYYY-MM-DD`.             | Corrija a entrada da data.                    |
| `Nenhum commit encontrado no intervalo de datas.` | O intervalo escolhido não contém atividade.    | Tente um período diferente.                   |

---
