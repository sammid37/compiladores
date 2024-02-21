# Construção de Compiladores
# Analisador Sintático
# Enthony e Samantha

import re
import csv

class Token:
  def __init__(self, token_type, value, line):
    self.type = token_type
    self.value = value
    self.line = line

  def __str__(self):
    return f"({self.value}, {self.type}, linha {self.line})"

class Sintatico:
  def __init__(self, tokens, output_file):
    self.tokens = tokens
    self.posicao = 0
    self.pilha = []
    self.output_file = output_file

  def avancar(self):
    self.posicao += 1

  def verificar(self, tipo):
    return self.tokens[self.posicao].type == tipo

  # Método responsável por consumir o tipo de um token e verificar sintaxe
  def consumir(self, tipo):
    # Se o tipo for correspondente ao esperado da regra, avança
    if self.verificar(tipo):
      self.avancar()
    # Se não, exibe erro de sintaxe
    else:
      raise SyntaxError(f"Erro de sintaxe: esperado {tipo}, encontrado {self.tokens[self.posicao].type}")
    
  # A análise sintática é concluída ao passar por todas as regras gramaticias da linguagem
  def analisar(self):
    # self.programa()
    print("Análise sintática concluída com sucesso.")

  # TODO: realiza a chamada das gramáticas
  def programa(self):
    pass 

  # TODO: método para gerar a saída do Analisador Sintático
    
  # TODO: definição de regras gramaticais a seguir
    # As regras gramaticais farão uso do método consumir()

  # * Regras não dependentes
  # * Regras dependentes simples
  # * Regras dependentes mais complexas
    
# Main do Analisador Sintático
  
# Lendo arquivo de entrada
def ler_tokens(nome_do_arquivo):
  tokens = []
  with open(nome_do_arquivo, 'r') as csvfile:
    leitor = csv.DictReader(csvfile)
    for linha in leitor:
      # criando uma tupla com o próprio token, o seu tipo e a linha que se encontra
      tokens.append(Token(linha['Token'], linha['Classificação'], int(linha['Linha'])))
  return tokens

source_file = 'lexico.csv'
output_file = 'sintatico.csv'  # Nome do arquivo de saída

tokens = ler_tokens(source_file)

analisador = Sintatico(tokens, output_file="sintatico.csv")
analisador.analisar()