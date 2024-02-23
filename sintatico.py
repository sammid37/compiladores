# Construção de Compiladores
# Analisador Sintático
# Enthony e Samantha

import re
import csv

from constantes import *

class Token:
  def __init__(self, token_type, value, line):
    self.type = token_type
    self.value = value
    self.line = line

  def __str__(self):
    return f"({self.value}, {self.type}, linha {self.line})"

class Sintatico:
  def __init__(self, tokens, output_file):
    self.tokens = tokens # a lista de tokens (formado por uma tupla << type, value, line >>)
    self.posicao = 0 # posição na lista de tuplas
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
    self.programa()
    print("Análise sintática concluída com sucesso.")

  # TODO: realiza a chamada das gramáticas
  def programa(self):
    # Inicial: verificar se o arquivo começa com: << program id ; >>
    self.f_program()
    self.f_id()
    self.f_delimiter()

    self.f_comando_composto() 

    # TODO: chamada de 
    # -[] declarações_variáveis
    # -[] declarações_de_subprogramas
    # -[] comando_composto
     
  # TODO: método para gerar a saída do Analisador Sintático
    
  # TODO: definição de regras gramaticais a seguir
  # As regras gramaticais farão uso do método consumir()

  def f_program(self):
    token_atual = self.tokens[self.posicao]
    if(token_atual.value) == 'program':
      self.consumir(token_atual.type)
    else: 
      # TODO: chamada de função para escrever em documento de saída
      raise SyntaxError(f"Esperava palavra reservada program, mas foi encontrado {token_atual.value}")

  def f_id(self):
    token_atual = self.tokens[self.posicao]
    self.consumir(token_atual.type)
  
  def f_delimiter(self):
    token_atual = self.tokens[self.posicao]
    print(token_atual)
    if token_atual.value in DELIMITER:
      print("Delimitador yay")
      self.consumir(token_atual.type)
    else:
      # TODO: chamada de função para escrever em documento de saída
      raise SyntaxError(f"Esperava delimitador, mas foi encontrado {token_atual.value} na linha {token_atual.line}")

  # * Regras não dependentes
  def f_op_aditivo(self):
    token_atual = self.tokens[self.posicao]
    if token_atual.value in OP_ADITIVO:
      self.consumir(token_atual.type)
    else:
      # TODO: chamada de função para escrever em documento de saída
      raise SyntaxError(f"Esperava operador aditivo, mas foi encontrado {token_atual.type}")

  def f_op_multiplicativo(self): 
    token_atual = self.tokens[self.posicao]
    if token_atual.value in OP_MULTIPLICATIVO:
      self.consumir(token_atual.type)
    else:
      # TODO: chamada de função para escrever em documento de saída
      raise SyntaxError(f"Esperava operador multiplicativo, mas foi encontrado {token_atual.type}")

  def f_op_relacional(self):
    token_atual = self.tokens[self.posicao]
    if token_atual.value in OP_RELACIONAL:
      self.consumir(token_atual.type)
    else:
      # TODO: chamada de função para escrever em documento de saída
      raise SyntaxError(f"Esperava operador relacional, mas foi encontrado {token_atual.type}")

  def f_sinal(self):
    token_atual = self.tokens[self.posicao]
    if token_atual.value in SINAL:
      self.consumir(token_atual.type)
    else:
      # TODO: chamada de função para escrever em documento de saída
      raise SyntaxError(f"Esperava sinal, mas foi encontrado {token_atual.type}")
    
  def f_tipo(self):
    token_atual = self.tokens[self.posicao].value
    if token_atual in TIPO:
      self.consumir(token_atual.type)
    else:
      # TODO: chamada de função para escrever em documento de saída
      raise SyntaxError(f"Esperava sinal, mas foi encontrado {token_atual.tipo}")

  # * Regras dependentes simples
  # * Regras dependentes mais complexas
  def f_comando_composto(self):

    token_atual = self.tokens[self.posicao]
    print(token_atual)
    if(token_atual.value) == 'begin':
      self.consumir('Palavra reservada')
    else: 
      # TODO: chamada de função para escrever em documento de saída
      raise SyntaxError(f"Esperava palavra reservada begin, mas foi encontrado {token_atual.value}")
    
    # TODO: chama f_comandos_opcionais()

    if(token_atual.value) == 'end':
      self.consumir('Palavra reservada')
    else: 
      # TODO: chamada de função para escrever em documento de saída
      raise SyntaxError(f"Esperava palavra reservada end, mas foi encontrado {token_atual.value}")
    
# Main do Analisador Sintático
# Lendo arquivo de entrada
def ler_tokens(nome_do_arquivo):
  tokens = []
  with open(nome_do_arquivo, 'r') as csvfile:
    leitor = csv.DictReader(csvfile)
    for linha in leitor:
      # criando uma tupla com o próprio token, o seu tipo e a linha que se encontra
      tokens.append(Token(linha['Classificação'], linha['Token'], int(linha['Linha'])))
  return tokens

source_file = 'lexico.csv'
output_file = 'sintatico.csv'  # Nome do arquivo de saída

tokens = ler_tokens(source_file)
# for token in tokens:
#   print(f'Tipo: {token.type}, Valor: {token.value}, Linha: {token.line}')

analisador = Sintatico(tokens, output_file="sintatico.csv")
analisador.analisar()