# Construção de Compiladores
# Compilador, arquivo principal
# Enthony e Samantha

import csv
import time

from termcolor import colored

from tokens import Token
from lexico import Lexer
from sintatico import Sintatico

def main():
  # Defina o nome do arquivo de entrada (código fonte)
  source_code = "test/syntax_tests/Test4.pas"  # Ex.: 'test/syntax_tests/Test1.pas'
  print(f"📃 Analisando o arquivo: {colored(source_code, 'cyan', 'on_cyan')}\n")
  with open(source_code, 'r') as f: 
    source_code = f.read()
  # print(source_code)

  # Defina o nome do arquivo de saída para o analisador léxico
  lexer_file = "lex_output.csv"        # Ex.: 'outputs/lexer_o/result1.csv'
  open(lexer_file, 'w').close() # Limpa o conteúdo dos arquivos, se existirem

  # Realiza a análise léxica a partir de um código fonte
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

  if lexer.lexer_errors != 0:
    print(colored(f"Análise léxica finalizada com {lexer.lexer_errors} erros.","red"))
  else:
    print(colored("✅ Análise léxica concluída com sucesso.","green"))

  # Realiza a análise sintática a partir da saída do analisador léxico
  print("\n⌛ Inicializando análise sintática e semântica...")
  if (lexer.lexer_errors == 0):
    lista_tokens = []
    with open(lexer_file, 'r') as csvfile:
      leitor = csv.DictReader(csvfile)
      for linha in leitor:
        # criando uma tupla com o próprio token, o seu tipo e a linha que se encontra
        lista_tokens.append(Token(linha['Classificação'], linha['Token'], int(linha['Linha'])))

    sintatico = Sintatico(lista_tokens)
    sintatico.analisar()

  else:
    print(f"\nNão foi possível realizar a análise sintática e semântica, pois erros foram encontrados durante a análise léxica.")
    print("Encerrando.")

if __name__ == "__main__":
  print(colored("* * * Projeto de Compiladores\n", "cyan"))
  main()