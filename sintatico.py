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

# Definição de um Analisador Sintático
class Sintatico:
  def __init__(self, tokens, output_file, input_file):
    self.tokens = tokens # a lista de tokens (formado por uma tupla << type, value, line >>)
    self.posicao = 0 # ? posição do token na lista de tuplas
    self.input_file = input_file
    self.output_file = output_file

  # Avança na leitura de tokens
  def avancar(self):
    self.posicao += 1

  # Verifica se um tipo corresponde ao esperado
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

  def programa(self):
    # Inicial: verificar se o arquivo começa com: << program id ; >>
    # Está funcional, mas talvez precise melhorar
    self.f_program()
    self.f_id() 
    self.f_delimiter()
    
    # TODO: chamada de 
    # -[] declarações_variáveis
    # -[] declarações_de_subprogramas
    # -[] comando_composto

    self.f_comando_composto() # TODO: está incompleto!
    
    self.f_delimiter()
 
  # TODO: método para gerar a saída do Analisador Sintático //enthony
    def gerar_saida(self): 
      with open(self.output_file, 'w') as csvfile: #fazendo a escrita do arquivo de saída
        writer = csv.writer(csvfile) #criando um objeto para escrita
        writer.writerow(['Classificação', 'Token', 'Linha']) #escrevendo o cabeçalho

      for token in self.tokens: #percorrendo a lista de tokens
        writer.writerow([token.type, token.value, token.line]) #escrevendo os tokens no arquivo de saída
    

  # ---------------------------------------------------------------------- REGRAS
  def f_program(self): 
    if(self.tokens[self.posicao].value) == 'program':
      self.consumir(self.tokens[self.posicao].type)
    else: 
      # TODO: chamada de função para escrever em documento de saída



      raise SyntaxError(f"Esperava palavra reservada program, mas foi encontrado {self.tokens[self.posicao].value}")

  def f_id(self): 
    # TODO: verificar se é necessário fazer um tratamento para tokens do tipo ID

    #if(self.tokens[self.posicao].type) == 'ID':
      


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

  # ** Regras dependentes simples - TENTATIVAAAAAAA 
    
  def f_fator(self):
    if self.tokens[self.posicao].type == 'ID':
        self.consumir('ID')  # Consome o token correspondente a um identificador
        if self.tokens[self.posicao].value == '(':
            self.consumir('(')  # Consome o token correspondente ao parêntese aberto
            self.f_lista_de_expressoes()  # Chamada para analisar uma lista de expressões
            if self.tokens[self.posicao].value == ')':
                self.consumir(')')  # Consome o token correspondente ao parêntese fechado
            else:
                raise SyntaxError("Erro de sintaxe: esperado ')' após a lista de expressões.")
    elif self.tokens[self.posicao].type == 'NUM_INT':
        self.consumir('NUM_INT')  # Consome o token correspondente a um número inteiro
    elif self.tokens[self.posicao].type == 'NUM_REAL':
        self.consumir('NUM_REAL')  # Consome o token correspondente a um número real
    elif self.tokens[self.posicao].type in ['TRUE', 'FALSE']:
        self.consumir(self.tokens[self.posicao].type)  # Consome o token correspondente a verdadeiro ou falso
    elif self.tokens[self.posicao].value == '(':
        self.consumir('(')  # Consome o token correspondente ao parêntese aberto
        self.f_expressao()  # Chamada para analisar uma expressão
        if self.tokens[self.posicao].value == ')':
            self.consumir(')')  # Consome o token correspondente ao parêntese fechado
        else:
            raise SyntaxError("Erro de sintaxe: esperado ')' após a expressão entre parênteses.")
    elif self.tokens[self.posicao].value in ['+', '-']:
        self.consumir(self.tokens[self.posicao].value)  # Consome o token correspondente ao sinal
        self.f_fator()  # Chamada recursiva para analisar outro fator após o sinal
    elif self.tokens[self.posicao].type == 'NOT':
        self.consumir('NOT')  # Consome o token correspondente ao operador lógico NOT
        self.f_fator()  # Chamada recursiva para analisar o fator após o NOT
    else:
        raise SyntaxError("Erro de sintaxe: fator inválido.")

  def f_expressao_simples(self):
    self.f_termo()  # Primeiro, analisa um termo
    while self.tokens[self.posicao].value in ['+', '-']:  # Enquanto encontrar operadores de adição ou subtração
        self.consumir(self.tokens[self.posicao].value)  # Consome o operador
        self.f_termo()  # Em seguida, analisa outro termo

  def f_expressao(self):
    self.f_expressao_simples()  # Primeiro, analisa uma expressão simples
    if self.tokens[self.posicao].value in OP_RELACIONAL:  # Se encontrar um operador relacional
        self.consumir(self.tokens[self.posicao].value)  # Consome o operador relacional
        self.f_expressao_simples()  # Em seguida, analisa outra expressão simples

  def f_lista_de_expressao(self):
    self.f_expressao()  # Analisa a primeira expressão da lista
    while self.tokens[self.posicao].value == ',':
        self.consumir(',')  # Consome a vírgula
        self.f_expressao()  # Analisa a próxima expressão na lista

  def f_termo(self):
    self.f_fator()  # Analisa o primeiro fator do termo
    while self.tokens[self.posicao].value in OP_MULTIPLICATIVO:
        self.consumir(self.tokens[self.posicao].type)  # Consome o operador multiplicativo
        self.f_fator()  # Analisa o próximo fator no termo

  def f_ativacao_procedimento(self):
    if self.tokens[self.posicao].type == 'ID':
        self.consumir('ID')  # Consome o identificador do procedimento
        if self.tokens[self.posicao].value == '(':
            self.consumir('(')  # Consome o '('
            self.f_lista_de_expressoes()  # Analisa a lista de expressões
            if self.tokens[self.posicao].value == ')':
                self.consumir(')')  # Consome o ')'
            else:
                raise SyntaxError(f"Esperava ')' para finalizar a chamada de procedimento, mas foi encontrado {self.tokens[self.posicao].value}")
    else:
        raise SyntaxError(f"Esperava um identificador de procedimento, mas foi encontrado {self.tokens[self.posicao].value}")


  # *** Regras dependentes mais complexas
  def f_comando(self): pass
  def f_lista_comandos(self): pass
  def f_comandos_opcionais(self): pass

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

  # ??? SEM CATEGORIA, ORGANIZAR!!
  def f_variavel(self): pass
  def f_lista_de_parametros(self): pass
  def f_argumentos(self): pass
  def f_declaracao_de_subprograma(self): pass
  def f_declaracoes_de_subprogramas(self): pass
  def f_lista_de_identificadores(self): pass
  def f_lista_declaracoes_variaveis(self): pass
  def f_declaracoes_variaveis(self): pass
  
# -------------------------------------------------------- Main do Analisador Sintático
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

analisador = Sintatico(tokens, output_file=output_file, input_file=source_file)
analisador.analisar()