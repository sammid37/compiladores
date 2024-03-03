# Construção de Compiladores
# Analisador Léxico 
# Enthony e Samantha

import re
import csv

from tokens import Token

from termcolor import colored

class Lexer:
  def __init__(self):
    self.source_code = None # código fonte que passará pelo analisador léxico
    self.output_lexer = None # arquivo de saída
    self.tokens = []
    self.position = 0
    self.line_number = 1

  def set_source_code(self, source_code):
    self.source_code = source_code

  def set_output_lexer(self, output_lexer):
    self.output_lexer = output_lexer

  def tokenize(self):
    # Listas de elementos aceitos
    atr = ':='
    op_r = ['=', '<', '>', '<=', '>=', '<>']
    op_a = ['+', '-', 'or']
    op_m = ['*', '/', 'and']
    delimiter = [';', '.', ':', '(', ')', ',']
    rw = ['program', 'var', 'integer', 'real', 'boolean', 'procedure', 'begin','end', 'if', 'then', 'else', 'while', 'do', 'not']
    
    # Enquanto não chega ao fim do arquivo 
    try:
      while(self.position < len(self.source_code)):
        # encontra espaços em branco e quebras de linha (\n)
        if self.source_code[self.position].isspace():
          if self.source_code[self.position] == '\n':
            self.line_number += 1 # contabiliza linhas
          self.position += 1
          continue

        # Verificação de comentários 
        if self.source_code[self.position] == '{':
          # Encontra o índice do caractere de fechamento '}'
          closing_brace_index = self.source_code.find('}', self.position)
          
          # Se não encontrar o caractere de fechamento, isso indica um erro de comentário não fechado
          if closing_brace_index == -1:
            raise Exception("Erro léxico: Comentário não fechado.")
    
          # Contagem de linhas dentro do comentário
          comment_content = self.source_code[self.position+1:closing_brace_index] # fatiamento
          self.line_number += comment_content.count('\n')

          # Move a posição para o caractere seguinte ao '}'
          self.position = closing_brace_index + 1

          # Continua para o próximo caractere
          continue

        # Verifique se a palavra é uma palavra reservada
        if re.match(r'[a-zA-Z]\w*', self.source_code[self.position:]):
          match = re.match(r'[a-zA-Z]\w*', self.source_code[self.position:])
          value = match.group()

          # Verifique se a palavra é uma palavra reservada
          if value.lower() in rw:
            token_type = 'Palavra reservada'
          elif value.lower() in op_a: 
            token_type = 'Operador aditivo'
          elif value.lower() in op_m: 
            token_type = 'Operador multiplicativo'
          else:
            token_type = 'Identificador'

          self.tokens.append(Token(token_type, value, self.line_number))
          self.position += len(value)
          continue
        
        if re.match(r'\d', self.source_code[self.position]):
          # É número...
          number_match = re.match(r'-?\d*\.?\d+(?:[eE][-+]?\d+)?', self.source_code[self.position:])
          if number_match:
            value = number_match.group()
            # Verificar se é um número inteiro ou real
            if '.' in value or 'e' in value.lower():
              token_type = 'Número real'
            else:
              token_type = 'Número inteiro'

            self.tokens.append(Token(token_type, value, self.line_number))
            self.position += len(value)
          continue

        # Verificação de símbolos
        if self.source_code[self.position:self.position+2] == atr:
          self.tokens.append(Token('Atribuição', atr, self.line_number))
          self.position += 2  # Avança dois caracteres (o comprimento do símbolo de atribuição)
          continue

        if self.source_code[self.position] in delimiter:
          self.tokens.append(Token('Delimitador', self.source_code[self.position], self.line_number))
          self.position += 1
          continue
        
        if self.source_code[self.position] in op_a:
          self.tokens.append(Token('Operador aditivo', self.source_code[self.position], self.line_number))
          self.position += 1
          continue

        if self.source_code[self.position] in op_m:
          self.tokens.append(Token('Operador multiplicativo', self.source_code[self.position], self.line_number))
          self.position += 1
          continue

        if self.source_code[self.position] in ''.join(op_r):
          operator = self.source_code[self.position]

          # Verifica se o próximo caractere também faz parte de um operador relacional composto
          if self.position + 1 < len(self.source_code) and (operator + self.source_code[self.position + 1]) in op_r:
            operator += self.source_code[self.position + 1]
            self.position += 2  # Avança dois caracteres
          else:
            self.position += 1  # Avança apenas um caractere

          self.tokens.append(Token('Operador relacional', operator, self.line_number))
          continue

        # enquanto não chega ao fim da entrada
        self.position += 1    

        # Se não corresponder a nenhum padrão, gera um erro
        print(f"{self.source_code[self.position-1]}")
        raise Exception(f"Erro léxico: caractere inválido '{self.source_code[self.position]}' na linha {self.line_number}, posição {self.position}")

    except Exception as e:
      print(colored(e,"red"))
    # Retorna tokens classificados :)
    return self.tokens
