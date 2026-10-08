# Sistema de Análise e Validação de Dados em Python (Sprint 5)

Este projeto foi desenvolvido como entregável da **Semana 05 (Desafio Sprint 5)**, com foco em consolidar os conceitos de **manipulação de arquivos**, **expressões regulares (Regex)**, **tratamento de exceções** e **exceções personalizadas**.

---

## 🛠️ Funcionalidades

- **Leitura Segura de Arquivos:** Processamento de arquivos CSV com codificação `UTF-8`.
- **Validação Rigorosa com Regex:**
  - **E-mail:** Padrão com verificação de usuário, domínio e TLD.
  - **CPF:** Suporte a formato mascarado (`000.000.000-00`) e numérico (`00000000000`).
  - **Telefone:** Suporte a DDD, nono dígito e diferentes separadores.
  - **Data:** Padrões `DD/MM/AAAA` e `AAAA-MM-DD`.
- **Tratamento de Exceções Robusto:** Captura de `FileNotFoundError`, `KeyError`, `ValueError` e exceções customizadas.
- **Relatório de Saída Formatado:** Apresentação clara do total de registros, estatísticas de aprovação e erros mapeados usando *f-strings*.

---

## 🔍 Detalhamento das Expressões Regulares (Regex)

| Campo | Padrão Regex | Explicação dos Metacaracteres |
| :--- | :--- | :--- |
| **E-mail** | `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$` | `^/$` ancoram o início/fim. `+` garante ao menos 1 caractere no nome de usuário e no domínio. `\.` escapa o ponto do domínio. |
| **CPF** | `^(\d{3}\.\d{3}\.\d{3}-\d{2}\|\d{11})$` | `\d{3}` exige exatamente 3 dígitos. `\|` aceita o formato formatado com pontos e hífen **OU** apenas os 11 números seguidos. |
| **Telefone** | `^(\(?\d{2}\)?\s?)?(9?\d{4})[-.\s]?(\d{4})$` | `\(` e `\)` aceitam DDD opcional com ou sem parênteses. `9?` permite celular com ou sem o dígito 9 frontal. |
| **Data** | `^(\d{2}/\d{2}/\d{4}\|\d{4}-\d{2}-\d{2})$` | Valida datas no padrão `DD/MM/AAAA` ou no formato ISO `AAAA-MM-DD`. |

---

## 🛡️ Tratamento de Exceções

O sistema utiliza o ciclo completo `try / except / else / finally`:

- **`try`**: Bloco onde é feita a tentativa de abertura do arquivo e leitura das linhas.
- **`except FileNotFoundError`**: Trata situações em que o arquivo especificado não existe no diretório.
- **`except KeyError`**: Captura ausência de colunas obrigatórias no cabeçalho do arquivo CSV.
- **`except ValueError`**: Captura arquivos vazios ou erros de tipo.
- **`else`**: Executado somente se a leitura for concluída com sucesso.
- **`finally`**: Garante que o arquivo seja encerrado com segurança, liberando recursos do sistema.
- **Exceção Personalizada (`FormatoInvalidoError`)**: Herda de `Exception` para tratar cenários específicos em que um registro viole uma regra de negócio customizada.

---

## 💻 Como Executar o Projeto

1. Clone o repositório ou baixe os arquivos em uma mesma pasta.
2. Certifique-se de ter o Python 3.8+ instalado.
3. Execute o script principal:

```bash
python main.py