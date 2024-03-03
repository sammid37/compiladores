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

  # Defina o nome do arquivo de entrada
  # Ex.: 'test/syntax_tests/Test1.pas'
  source_code = "test/lexer_tests/exemplo1.txt"
  with open(source_code, 'r') as f: 
    source_code = f.read()
  # print(source_code)

  # Defina o nome do arquivo de saída para o analisador léxico
  # Ex.: 'outputs/lexer_o/result1.csv'
  lexico_file = "lex_output.csv"

  # Defina o nome do arquivo de saída para o analisador sintático
  # Ex.: 'outputs/syntax_o/result1.csv'
  sintatico_file = "sint_output.csv"

  # Realize a análise léxica a partir de um código fonte
  print("Inicializando análise léxica...")
  lexer = Lexer()
  lexer.set_source_code(source_code=source_code)
  lexer.set_output_lexer(output_lexer=lexico_file)
  lexer.tokenize()
  # total_tokens = len(lexer.tokens)
  # print(len(source_code))
  # print(total_tokens)

  with open(lexer.output_lexer, 'a', newline='') as csvfile:
    fieldnames = ['Token', 'Classificação', 'Linha']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()  # Escreva o cabeçalho do CSV
    for token in lexer.tokens:
      writer.writerow({'Token': token.value, 'Classificação': token.type, 'Linha': token.line})
    # with tqdm(total=total_tokens, desc="Escrevendo no arquivo CSV") as pbar:

    #     # Escreva cada token no arquivo CSV
    #     time.sleep(0.05)
    #     pbar.update(1)  # Atualize a barra de progresso
      
  # TODO: incluir barra de progresso com tqdm
  print("[Léxico] Arquivo .csv gerado!")


  print("Inicializando análise sintática...")
  lista_tokens = []
  with open(lexico_file, 'r') as csvfile:
    leitor = csv.DictReader(csvfile)
    for linha in leitor:
      # criando uma tupla com o próprio token, o seu tipo e a linha que se encontra
      lista_tokens.append(Token(linha['Classificação'], linha['Token'], int(linha['Linha'])))

# try:
# except Exception as e:
#   print(colored(f"Erro ocorrido durante a análise léxica: {e}", "red"))
#   tqdm.close()

  # Inicializando análise sintática
  # Armazena tokens em tuplas

  sintatico = Sintatico(lista_tokens)
  sintatico.set_input_file(lexico_file)
  sintatico.set_output_syntax(sintatico_file)
  sintatico.analisar()
  print(lista_tokens)

if __name__ == "__main__":
  print(colored("* * * Projeto de Compiladores", "cyan"))
  print()
  main()