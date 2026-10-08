"""
Entregável de Desenvolvimento em Python - Semana 05 (Sprint 5)
Sistema de Análise de Dados e Validação com Regex, Exceções e Manipulação de Arquivos.
"""

import csv
import re
from typing import Dict, List, Tuple


# =============================================================================
# EXCEÇÃO PERSONALIZADA
# =============================================================================
class FormatoInvalidoError(Exception):
    """Exceção lançada quando um dado obrigatório não atende às regras de validação."""

    pass


# =============================================================================
# MÓDULO DE VALIDAÇÃO (EXPRESSÕES REGULARES - REGEX)
# =============================================================================
class ValidadorDados:
    """Classe responsável por conter todos os padrões de Regex do sistema."""

    # E-mail: usuario@dominio.extensao (suporta subdomínios)
    REGEX_EMAIL = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    # CPF: 000.000.000-00 ou 00000000000
    REGEX_CPF = r"^(\d{3}\.\d{3}\.\d{3}-\d{2}|\d{11})$"

    # Telefone: (00) 90000-0000 ou (00) 0000-0000 com ou sem máscara
    REGEX_TELEFONE = r"^(\(?\d{2}\)?\s?)?(9?\d{4})[-.\s]?(\d{4})$"

    # Data: DD/MM/AAAA ou AAAA-MM-DD
    REGEX_DATA = (
        r"^(\d{2}/\d{2}/\d{4}|\d{4}-\d{2}-\d{2})$"
    )

    @classmethod
    def validar_email(cls, email: str) -> bool:
        return bool(re.match(cls.REGEX_EMAIL, email.strip()))

    @classmethod
    def validar_cpf(cls, cpf: str) -> bool:
        return bool(re.match(cls.REGEX_CPF, cpf.strip()))

    @classmethod
    def validar_telefone(cls, telefone: str) -> bool:
        return bool(re.match(cls.REGEX_TELEFONE, telefone.strip()))

    @classmethod
    def validar_data(cls, data: str) -> bool:
        return bool(re.match(cls.REGEX_DATA, data.strip()))


# =============================================================================
# PROCESSADOR DE ARQUIVOS E ANÁLISE DE DADOS
# =============================================================================
class ProcessadorDeDados:
    """Classe para gerenciar leitura de arquivos, tratamento de exceções e relatórios."""

    COLUNAS_OBRIGATORIAS = {"nome", "email", "cpf", "telefone", "data"}

    def __init__(self, caminho_arquivo: str):
        self.caminho_arquivo = caminho_arquivo
        self.registros_validos: List[Dict[str, str]] = []
        self.registros_invalidos: List[Tuple[Dict[str, str], List[str]]] = []
        self.total_registros = 0

    def processar_arquivo(self) -> None:
        """Lê o arquivo CSV e realiza a validação campo por campo."""
        arquivo = None
        try:
            # Abertura segura do arquivo com encoding UTF-8
            arquivo = open(self.caminho_arquivo, mode="r", encoding="utf-8")
            leitor_csv = csv.DictReader(arquivo)

            # Validação de KeyError (Verifica se as colunas necessárias existem no CSV)
            if not leitor_csv.fieldnames:
                raise ValueError("O arquivo CSV está vazio.")

            colunas_existentes = set(map(str.lower, leitor_csv.fieldnames))
            if not self.COLUNAS_OBRIGATORIAS.issubset(colunas_existentes):
                colunas_faltantes = (
                    self.COLUNAS_OBRIGATORIAS - colunas_existentes
                )
                raise KeyError(
                    f"Colunas obrigatórias ausentes no arquivo: {colunas_faltantes}"
                )

            for linha in leitor_csv:
                self.total_registros += 1
                erros = []

                # Validações dos campos
                if not ValidadorDados.validar_email(linha.get("email", "")):
                    erros.append("E-mail inválido")
                if not ValidadorDados.validar_cpf(linha.get("cpf", "")):
                    erros.append("CPF inválido")
                if not ValidadorDados.validar_telefone(
                    linha.get("telefone", "")
                ):
                    erros.append("Telefone inválido")
                if not ValidadorDados.validar_data(linha.get("data", "")):
                    erros.append("Data inválida")

                # Separação de registros válidos e inválidos
                if not erros:
                    self.registros_validos.append(linha)
                else:
                    self.registros_invalidos.append((linha, erros))

        except FileNotFoundError:
            print(
                f"[ERRO CRÍTICO] O arquivo '{self.caminho_arquivo}' não foi encontrado!"
            )
        except KeyError as error:
            print(f"[ERRO DE ESTRUTURA] {error}")
        except ValueError as error:
            print(f"[ERRO DE CONVERSÃO/DADO] {error}")
        except Exception as error:
            print(f"[ERRO INESPERADO] Ocorreu uma falha não mapeada: {error}")
        else:
            print("\n[SUCESSO] Leitura e análise concluídas sem falhas na estrutura!")
        finally:
            # Garantia de execução do fechamento de recurso (embora o with open seja preferencial)
            if arquivo and not arquivo.closed:
                arquivo.close()
                print("[SISTEMA] Conexão com o arquivo encerrada com segurança (finally).")

    def gerar_relatorio(self) -> None:
        """Imprime o relatório final utilizando f-strings."""
        print("\n" + "=" * 60)
        print(f"{'RELATÓRIO FINAL DE ANÁLISE DE DADOS':^60}")
        print("=" * 60)

        taxa_sucesso = (
            (len(self.registros_validos) / self.total_registros * 100)
            if self.total_registros > 0
            else 0
        )

        print("\n--- ESTATÍSTICAS DA ANÁLISE ---")
        print(f"• Total de registros processados : {self.total_registros}")
        print(f"• Registros válidos               : {len(self.registros_validos)}")
        print(f"• Registros com inconsistências   : {len(self.registros_invalidos)}")
        print(f"• Taxa de conformidade            : {taxa_sucesso:.2f}%")

        print("\n--- DETALHAMENTO DE REGISTROS VÁLIDOS ---")
        if self.registros_validos:
            for reg in self.registros_validos:
                print(
                    f"✓ [{reg['nome']:<18}] | CPF: {reg['cpf']:<14} | Email: {reg['email']}"
                )
        else:
            print("  Nenhum registro 100% válido encontrado.")

        print("\n--- DETALHAMENTO DE REGISTROS INVÁLIDOS ---")
        if self.registros_invalidos:
            for reg, falhas in self.registros_invalidos:
                falhas_str = ", ".join(falhas)
                print(
                    f"✗ [{reg.get('nome', 'N/A'):<18}] | Inconsistências: {falhas_str}"
                )
        else:
            print("  Nenhuma inconsistência encontrada.")

        print("=" * 60)


# =============================================================================
# PONTO DE ENTRADA DO SCRIPT
# =============================================================================
if __name__ == "__main__":
    caminho = "dados.csv"

    processador = ProcessadorDeDados(caminho_arquivo=caminho)
    processador.processar_arquivo()
    processador.gerar_relatorio()