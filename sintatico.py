# Construção de Compiladores
# Analisador Sintático
# Enthony e Samantha

import re
import csv

from constantes import *

# Definição de um Token: tipo, valor e linha onde se localiza
class Token:
  def __init__(self, token_type, value, line):
    self.type = token_type
    self.value = value
    self.line = line

  def __str__(self):
    return f"({self.value}, {self.type}, linha {self.line})"

class Sintatico:
  def __init__(self, tokens, output_file, input_file):
    self.tokens = tokens # a lista de tokens (formado por uma tupla << type, value, line >>)
    self.posicao = 0 # ? posição do token na lista de tuplas
    self.input_file = input_file
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
    
    # TODO: chamada de 
    # -[] declarações_variáveis
    # -[] declarações_de_subprogramas
    # -[] comando_composto

    self.f_comando_composto() # TODO: está incompleto!
    
    self.f_delimiter()
 
  # TODO: método para gerar a saída do Analisador Sintático
    
  # TODO: definição de regras gramaticais a seguir
  # As regras gramaticais farão uso do método consumir()

  def f_program(self): 
    if(self.tokens[self.posicao].value) == 'program':
      self.consumir(self.tokens[self.posicao].type)
    else: 
      # TODO: chamada de função para escrever em documento de saída
      raise SyntaxError(f"Esperava palavra reservada program, mas foi encontrado {self.tokens[self.posicao].value}")

  def f_id(self): 
    # TODO: verificar se é necessário fazer um tratamento para tokens do tipo ID
    self.consumir(self.tokens[self.posicao].type)
  
  def f_delimiter(self): 
    if self.tokens[self.posicao].value in DELIMITER:
      self.consumir(self.tokens[self.posicao].type)
    else:
      # TODO: chamada de função para escrever em documento de saída
      raise SyntaxError(f"Esperava delimitador, mas foi encontrado {self.tokens[self.posicao].value} na linha {self.tokens[self.posicao].line}")

  # * Regras não dependentes
  def f_op_aditivo(self):

    if self.tokens[self.posicao].value in OP_ADITIVO:
      self.consumir(self.tokens[self.posicao].type)
    else:
      # TODO: chamada de função para escrever em documento de saída
      raise SyntaxError(f"Esperava operador aditivo, mas foi encontrado {self.tokens[self.posicao].type}")

  def f_op_multiplicativo(self):  
    if self.tokens[self.posicao].value in OP_MULTIPLICATIVO:
      self.consumir(self.tokens[self.posicao].type)
    else:
      # TODO: chamada de função para escrever em documento de saída
      raise SyntaxError(f"Esperava operador multiplicativo, mas foi encontrado {self.tokens[self.posicao].type}")

  def f_op_relacional(self):
    if self.tokens[self.posicao].value in OP_RELACIONAL:
      self.consumir(self.tokens[self.posicao].type)
    else:
      # TODO: chamada de função para escrever em documento de saída
      raise SyntaxError(f"Esperava operador relacional, mas foi encontrado {self.tokens[self.posicao].type}")

  def f_sinal(self):
    if self.tokens[self.posicao].value in SINAL:
      self.consumir(self.tokens[self.posicao].type)
    else:
      # TODO: chamada de função para escrever em documento de saída
      raise SyntaxError(f"Esperava sinal, mas foi encontrado {self.tokens[self.posicao].type}")
    
  def f_tipo(self):
    if self.tokens[self.posicao].value in TIPO:
      self.consumir(self.tokens[self.posicao].type)
    else:
      # TODO: chamada de função para escrever em documento de saída
      raise SyntaxError(f"Esperava sinal, mas foi encontrado {self.tokens[self.posicao].tipo}")

  # * Regras dependentes simples
    
  # * Regras dependentes mais complexas
  def f_comando_composto(self):
    if(self.tokens[self.posicao].value) == 'begin':
      self.consumir('Palavra reservada')
    else: 
      # TODO: chamada de função para escrever em documento de saída
      raise SyntaxError(f"Esperava palavra reservada begin, mas foi encontrado {self.tokens[self.posicao].value}")
    
    # TODO: chama f_comandos_opcionais()
    # self.avancar()
    # print("avancei")
    # print(self.tokens[self.posicao])

    if(self.tokens[self.posicao].value) == 'end':
      self.consumir('Palavra reservada')
    else: 
      # TODO: chamada de função para escrever em documento de saída
      raise SyntaxError(f"Esperava palavra reservada end, mas foi encontrado {self.tokens[self.posicao].value}")
    
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