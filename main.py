# Construção de Compiladores
# Compilador, arquivo principal
# Enthony e Samantha

import os
import csv

from termcolor import colored

from tokens import Token
from lexico import Lexer
from sintatico import Sintatico

def main(file_name):
  # Defina o nome do arquivo de entrada (código fonte)
  source_code = file_name
  display_file_name = os.path.basename(file_name)
  print(f"📃 Analisando o arquivo: {colored(display_file_name, 'light_grey')}")
  with open(source_code, 'r') as f: 
    source_code = f.read()
  # print(source_code)

  # Defina o nome do arquivo de saída para o analisador léxico
  lexer_file = "lex_output.csv"        # Ex.: 'outputs/lexer_o/result1.csv'
  open(lexer_file, 'w').close() # Limpa o conteúdo dos arquivos, se existirem

  # Realiza a análise léxica a partir de um código fonte
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

  if lexer.lexer_errors != 0:
    print(colored(f"Análise léxica finalizada com {lexer.lexer_errors} erros.","red"))
  else:
    print(colored("✅ Análise léxica concluída com sucesso.","green"))

  # Realiza a análise sintática a partir da saída do analisador léxico
  if (lexer.lexer_errors == 0):
    lista_tokens = []
    with open(lexer_file, 'r') as csvfile:
      leitor = csv.DictReader(csvfile)
      for linha in leitor:
        # criando uma tupla com o próprio token, o seu tipo e a linha que se encontra
        lista_tokens.append(Token(linha['Classificação'], linha['Token'], int(linha['Linha'])))

    sintatico = Sintatico(lista_tokens)
    sintatico.analisar()
    print(colored("✅ Análise sintática e semântica concluída com sucesso.\n", 'green'))

  else:
    print(f"\nNão foi possível realizar a análise sintática e semântica, pois erros foram encontrados durante a análise léxica.")
    print("Encerrando.")

if __name__ == "__main__":
  print(colored("* * * Projeto de Compiladores", "cyan"))
  test_files_directory = "test/syntax_tests/"
  # Realizando a execução dos 5 arquivos de teste
  # Se um deles falhar, o próximo não poderá ser testado
  for i in range(1, 6):
    file_name = os.path.join(test_files_directory, f"Test{i}.pas")
    main(file_name)