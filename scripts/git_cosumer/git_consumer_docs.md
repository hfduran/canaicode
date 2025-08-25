# 📊 Exportador de Commits Git para Excel com múltiplas abas (via Python)

Este script em Python extrai commits de múltiplos repositórios Git informados via URLs, filtrando por um intervalo de datas fornecido pelo usuário. Para cada repositório, o script clona o projeto temporariamente, coleta os commits, apaga o repositório clonado e gera um arquivo Excel `.xlsx` com uma aba para cada repositório contendo os commits correspondentes.

---

## ✅ Requisitos

Antes de executar o script, certifique-se de que seu sistema possui:

- **Python 3.10 ou superior**
- **Git** instalado e acessível pelo terminal
- **pip** (gerenciador de pacotes do Python)

---

## 📦 Instalação das Bibliotecas

O script depende das seguintes bibliotecas Python:

- [`GitPython`](https://pypi.org/project/GitPython/)
- [`pandas`](https://pypi.org/project/pandas/)
- [`pydantic`](https://pypi.org/project/pydantic/)
- [`xlsxwriter`](https://pypi.org/project/XlsxWriter/) — para gerar o arquivo Excel

Para instalá-las, execute no terminal:

```bash
pip install gitpython pandas pydantic xlsxwriter
```

---

## 📁 Estrutura do Script

1. Crie um arquivo chamado `git_consumer.py`.
2. Cole o código Python completo fornecido neste script.
3. Crie um arquivo .txt com as URLs dos repositórios Git que deseja analisar, uma URL por linha. Exemplo de conteúdo:

```txt
https://github.com/user/repo1.git
https://github.com/user/repo2.git
https://github.com/user/repo3.git
```

---

## 🚀 Executando o Script

No terminal, navegue até a pasta onde está o script:

```bash
cd caminho/para/o/script
```

E execute passando os parâmetros diretamente:

```bash
python git_consumer.py repos.txt 2024-01-01 2025-08-18
```

Onde:

- `repos.txt` → caminho para o arquivo com as URLs dos repositórios

- `2024-01-01` → data inicial

- `2025-08-18` → data final

---

## 💬 Argumentos da Linha de Comando

O script agora aceita argumentos diretamente:

| Argumento    | Obrigatório | Descrição                                                       |
| ------------ | ----------- | --------------------------------------------------------------- |
| `urls_file`  | ✅          | Caminho para o arquivo `.txt` contendo as URLs dos repositórios |
| `start_date` | ✅          | Data inicial no formato `YYYY-MM-DD`                            |
| `end_date`   | ✅          | Data final no formato `YYYY-MM-DD`                              |

---

## 📄 Saída Gerada

Se houver commits no intervalo especificado, será criado um arquivo Excel `.xlsx` chamado:

```
commits_{data_inicial}_to_{data_final}.xlsx
```

Exemplo:

```
commits_2024-07-01_to_2024-07-05.xlsx
```

### Estrutura do Excel:

- Cada aba representa um repositório analisado.

- O nome da aba é o nome do repositório (limite de 31 caracteres devido ao Excel).

- As colunas em cada aba são:

| hash | repository | date | author | language | added_lines | removed_lines |
| ---- | ---------- | ---- | ------ | -------- | ----------- | ------------- |

Cada linha representa um arquivo modificado em um commit.

---

## 🧪 Teste Rápido

Você pode criar um arquivo `.txt` com uma URL pública para testar, por exemplo:

```txt
https://github.com/git/git.git
```

E usar uma data inicial e final dentro do histórico do repositório para ver a extração funcionar.

---

## ❗ Possíveis Erros e Soluções

| Erro                                           | Causa Provável                                | Solução                                                                          |
| ---------------------------------------------- | --------------------------------------------- | -------------------------------------------------------------------------------- |
| `Error: Invalid file path.`                    | O arquivo `.txt` com URLs não foi encontrado. | Verifique se o caminho e nome do arquivo estão corretos.                         |
| `Invalid date. Use the format YYYY-MM-DD.`     | Data informada com formato incorreto.         | Corrija a data para o formato `YYYY-MM-DD`.                                      |
| `Error: Start date is later than end date.`    | Data inicial maior que a final.               | Corrija o intervalo de datas informado.                                          |
| Nenhum commit encontrado no intervalo de datas | O intervalo de datas não contém commits.      | Tente outro intervalo ou confirme que o repositório tem atividade nesse período. |

---
