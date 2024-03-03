# Construção de Compiladores
# Compilador, arquivo principal
# Enthony e Samantha

import csv
import time

from tqdm import tqdm
from termcolor import colored

from tokens import Token
from lexico import Lexer
from sintatico import Sintatico

def main():
  # Defina o nome do arquivo de entrada (código fonte)
  source_code = "test/syntax_tests/Test3.pas"  # Ex.: 'test/syntax_tests/Test1.pas'
  with open(source_code, 'r') as f: 
    source_code = f.read()
  # print(source_code)

  # Defina o nome do arquivo de saída para o analisador léxico e sintático
  lexer_file = "lex_output.csv"        # Ex.: 'outputs/lexer_o/result1.csv'
  syntax_file = "sint_output.csv"      # Ex.: 'outputs/syntax_o/result1.csv'

  # Realize a análise léxica a partir de um código fonte
  print("⌛ Inicializando análise léxica...")
  lexer = Lexer()
  lexer.set_source_code(source_code=source_code)
  lexer.set_output_lexer(output_lexer=lexer_file)
  lexer.tokenize()

  with open(lexer.output_lexer, 'a', newline='') as csvfile:
    fieldnames = ['Token', 'Classificação', 'Linha']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()  # Escreva o cabeçalho do CSV
    for token in lexer.tokens:
      writer.writerow({'Token': token.value, 'Classificação': token.type, 'Linha': token.line})
      
  # TODO: incluir barra de progresso com tqdm (?)
  print(colored("✅ Análise léxica concluída","green"))

  print("\n⌛ Inicializando análise sintática...")
  lista_tokens = []
  with open(lexer_file, 'r') as csvfile:
    leitor = csv.DictReader(csvfile)
    for linha in leitor:
      # criando uma tupla com o próprio token, o seu tipo e a linha que se encontra
      lista_tokens.append(Token(linha['Classificação'], linha['Token'], int(linha['Linha'])))

  sintatico = Sintatico(lista_tokens)
  sintatico.set_input_file(lexer_file)
  sintatico.set_output_syntax(syntax_file)
  sintatico.analisar()

if __name__ == "__main__":
  print(colored("* * * Projeto de Compiladores", "cyan"))
  print()
  main()