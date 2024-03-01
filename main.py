# Construção de Compiladores
# Compilador, arquivo principal
# Enthony e Samantha

from lexico import Lexer
from sintatico import Sintatico

# TODO: criar classe Token separadamente e importar ou definí-la no arquivo main.py
# TODO: [Lexico] acrescentar aceitação de aspas simples e duplas 

from termcolor import colored

def main():
  # Defina o nome do arquivo de entrada
  # Ex.: 'test/syntax_tests/Test1.pas'
  source_code = "input_code.txt"
  
  # Defina o nome do arquivo de saída para o analisador léxico
  # Ex.: 'outputs/lexer_o/result1.csv'
  lexico_file = "lex_output.csv"
  
  # Defina o nome do arquivo de saída para o analisador sintático
  # Ex.: 'outputs/syntax_o/result1.csv'
  sintatico_file = "sint_output.csv"

  # Realize a análise léxica a partir de um código fonte
  # TODO: modificar a classe de forma que ele tbm receba um atributo arquivo de saída (semelhante ao que o sintático faz, pois o sintático receber 2 arquivos: entrada e saída)
  lexer = Lexer(source_code)
  tokens = lexer.tokenize() # armazena os tokens, talvez renomear apaenas para << t >>

  # TODO: seguir o padrão que está no analisador léxico
  # Escreva os resultados da análise léxica no arquivo de saída
  with open(lexico_file, "w") as f:
    for token in tokens:
      f.write(f"{token}\n")

  # TODO: Realizar alguma verificação de que o arquivo de saída do Léxico foi gerado para então o Sintático começar a operar.

  # TODO: Verificar se precisa de ajustes
  # -[] Armazenar tokens em tuplas (criar variável nova) -> semelhante ao que é feito em ler_tokens(nome_arq=<saida_CSV_lexico>) do Analisador SIntático
  # Realize a análise sintática    
  sintatico = Sintatico(tokens, sintatico_file, lexico_file)
  sintatico.analisar()

  print("Análise léxica e sintática concluídas.")
  print(colored("Hello world","cyan"))