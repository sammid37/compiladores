# Construção de Compiladores
# Analisador Sintático
# Enthony e Samantha

import re
import csv

class Sintatico:
  def __init__(self, token_type, value, line):
    self.type = token_type
    self.value = value
    self.line = line

  def analisar_erros_sintaticos():
    pass

  def analisar_gramatica():
    pass

# Main do Analisador Sintático
# Lendo arquivo de entrada
source_file = 'entrada.txt'

with open(source_file, 'r') as f: 
  source_code = f.read()
  # print(source_code)

# Gerando saída do Analisador Sintático