# Construção de Compiladores
# Analisador Léxico 
# Enthony e Samantha

import re
import ply.lex as lex

class Token:
  def __init__(self, token_type, value, line):
    self.type = token_type
    self.value = value
    self.line = line

  # imprime as linhas da tabela de token
  def __str__(self):
    return f"({self.type}, {self.value}, linha {self.line})

class Lexer:
  def __init__(self, input_code):
    self.input_code = input_code # código fonte que passará pelo analisador léxico
    self.tokens = []
    self.position = 0
    self.line_number = 1

  def tokenize(self):
    pass
    #* Criar expressão regular para 
    re_num = ''
    re_id_rw = ''
    re_op = ''

    # Listas de elementos aceitos
    atr = ':='
    op_r = ['=', '<', '>', '<=', '>=', '<>']
    op_a = ['+', '-']
    op_m = ['*', '/']
    comment = ['{', '}']
    delimiter = [';', '.', ':', '(', ')', ',']
    rw = ['program', 'var', 'integer', 'real', 'boolean', 'procedure', 'begin','end', 'if', 'then', 'else', 'while', 'do', 'not']
    
    # Enquanto não chega ao fim do arquivo 
    while():

      #* Fazer verificação para cada tipo, usando as expressoes regulares
      # e imprimir utilizando a classe Token
      # exemplo de uso: self.tokens.append(Token('TIPO', value, self.line_number))

      # enquanto não chega ao fim da entrada
      self.position += 1    

  return self.tokens

  
# Lendo arquivo de entrada
source_file = 'entrada.txt'

with open(source_file, 'r') as f: 
  source_code = f.read()
print(source_code)

# Inicializando analisador léxico
lexer = Lexer(source_code)
tokens = lexer.tokenize()

for token in tokens:
  print(token)