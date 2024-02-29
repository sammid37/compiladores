# Construção de Compiladores
# Compilador, arquivo principal
# Enthony e Samantha

from lexico import Lexer
from sintatico import Sintatico

from termcolor import colored

def main():
  # Defina o nome do arquivo de entrada
  source_code = "input_code.txt"
  
  # Defina o nome do arquivo de saída para o analisador léxico
  lexico_file = "lex_output.csv"
  
  # Defina o nome do arquivo de saída para o analisador sintático
  sintatico_file = "sint_output.csv"

  # Realize a análise léxica
  lexer = Lexer(source_code)
  tokens = lexer.tokenize()

  # TODO: seguir o padrão que está no analisador léxico
  # Escreva os resultados da análise léxica no arquivo de saída
  with open(lexico_file, "w") as f:
    for token in tokens:
      f.write(f"{token}\n")

  # TODO: Verificar se precisa de ajustes
  # Realize a análise sintática
  sintatico = Sintatico(tokens, sintatico_file, lexico_file)
  sintatico.analisar()

  print("Análise léxica e sintática concluídas.")