# Construção de Compiladores
# Analisador Sintático
# Enthony e Samantha

import re
import csv

from constantes import *

# Definição de um Token: tipo, valor e linha onde se localiza
class Token:
  def __init__(self, token_type, value, line, erro_sintatico=None):
    self.type = token_type
    self.value = value
    self.line = line
    self.erro_sintatico = erro_sintatico

  def __str__(self):
    if(self.erro_sintatico): 
      return f"({self.value}, {self.type}, linha {self.line}, erro sintático: '{self.erro_sintatico}')"
    else:
      return f"({self.value}, {self.type}, linha {self.line})"
       
# Definição de um Analisador Sintático
class Sintatico:
  def __init__(self, tokens, output_file, input_file):
    self.tokens = tokens # a lista de tokens (formado por uma tupla << type, value, line >>)
    self.posicao = 0 # posição do token na lista de tuplas
    self.count_begin = 0 # indicador para pares begin e end
    self.input_file = input_file
    self.output_file = output_file

  def token_atual(self):
    """Obtém o valor do token atual"""
    return self.tokens[self.posicao].value;

  def tipo_atual(self):
    """Obtém o tipo do token atual"""
    return self.tokens[self.posicao].type;

  def mensagem_token(self, mensagem):
    """Atribui uma mensagem de erro pro token lido"""
    self.tokens[self.posicao].erro_sintatico = mensagem
    return self.tokens[self.posicao].erro_sintatico

  # Avança na leitura de tokens
  def avancar(self):
    """Avança para a próxima posição que possa conter um token"""
    self.posicao += 1

  # Verifica se um tipo corresponde ao esperado
  def verificar(self, tipo):
    """Retorna se o tipo do token atual corresponde ao tipo esperado"""
    return self.tipo_atual() == tipo

  def consumir(self, tipo):
    """Método responsável por consumir o tipo de um token e verificar sintaxe"""
    # Se o tipo for correspondente ao esperado da regra, avança
    if self.verificar(tipo):
      self.avancar()
    # Se não, exibe erro de sintaxe
    else:
      self.tokens[self.posicao].erro_sintatico = f"esperado {tipo}, encontrado {self.tipo_atual()}"
    
  # A análise sintática é concluída ao passar por todas as regras gramaticias da linguagem
  def analisar(self):
    """Realiza a análise sintática de um programa"""
    self.programa()
    print("Análise sintática concluída com sucesso.")

  def programa(self):
    """Contém regras (subregras) de um programa em Pascal"""
    # Inicial: verificar se o arquivo começa com: << program id ; >>
    self.f_program()
    self.f_id() 
    self.f_delimiter_program()
    # Verificação de declarações de variaveis, declarações de subprograma e comandos compostos
    self.f_declaracoes_variaveis()
    self.f_declaracoes_de_subprogramas() 
    self.f_comando_composto()
  
  # ---------------------------------------------------------------------- REGRAS
  def f_program(self): 
    """Verifica se o programa começa com a palavra reservada program"""
    if self.token_atual() == 'program':
      self.consumir('Palavra reservada')
    else: 
      self.mensagem_token(f"Esperava a palavra reservada 'program', mas foi encontrado {self.token_atual()}")
      escrever_erro_sintatico(self.tokens[self.posicao])
      exit()

  def f_id(self): 
    if(self.tipo_atual()) == 'Identificador':
      self.consumir(self.tipo_atual())
    else: 
      self.mensagem_token(f"Esperava um identificador, mas foi encontrado {self.token_atual()}")
      escrever_erro_sintatico(self.tokens[self.posicao])
      exit()

  def f_delimiter_program(self): 
    """Delimitador do nome de um programa: << program id ; >>"""
    if self.token_atual() in DELIMITER and self.token_atual() == ';':
      self.consumir(self.tipo_atual())
    else:
      self.mensagem_token(f"Esperava o delimitador ';', mas foi encontrado {self.token_atual()}")
      escrever_erro_sintatico(self.tokens[self.posicao])
      exit()

  def f_delimiter(self): 
    if self.token_atual() in DELIMITER:
      self.consumir(self.tipo_atual())
    else:
      self.mensagem_token(f"Esperava algum delimitado, mas foi encontrado {self.token_atual()}")
      escrever_erro_sintatico(self.tokens[self.posicao])
      exit()

  # * Regras não dependentes
  def f_op_aditivo(self):
    if self.self.token_atual() in OP_ADITIVO:
      self.consumir(self.tipo_atual())
    else:
      self.mensagem_token(f"Esperava algum operador aditivo, mas foi encontrado {self.token_atual()}")
      escrever_erro_sintatico(self.tokens[self.posicao])
      exit()

  def f_op_multiplicativo(self):  
    if self.token_atual() in OP_MULTIPLICATIVO:
      self.consumir(self.tipo_atual())
    else:
      self.mensagem_token(f"Esperava algum operador multiplicativo, mas foi encontrado {self.token_atual()}")
      escrever_erro_sintatico(self.tokens[self.posicao])
      exit()

  def f_op_relacional(self):
    if self.token_atual() in OP_RELACIONAL:
      self.consumir(self.tipo_atual())
    else:
      self.mensagem_token(f"Esperava algum operador relacional, mas foi encontrado {self.token_atual()}")
      escrever_erro_sintatico(self.tokens[self.posicao])
      exit()

  def f_sinal(self):
    if self.token_atual() in SINAL:
      self.consumir(self.tipo_atual())
    else:
      self.mensagem_token(f"Esperava algum sinal, mas foi encontrado {self.token_atual()}")
      escrever_erro_sintatico(self.tokens[self.posicao])
      exit()
    
  def f_tipo(self):
    if self.token_atual() in TIPO:
      self.consumir(self.tipo_atual())
    else:
      self.mensagem_token(f"Esperava algum tipo tipo de variável, mas foi encontrado {self.token_atual()}")
      escrever_erro_sintatico(self.tokens[self.posicao])
      exit()

  # ** Regras dependentes simples
  def f_fator(self):
    if self.tipo_atual() == 'Identificador':
      self.f_ativacao_procedimento()
    elif self.tipo_atual() == 'Número inteiro' or  self.tipo_atual() == 'Número real':
      self.consumir(self.tipo_atual())  # Consome o token correspondente a um número inteiro
    elif self.tipo_atual() in BOOLEAN_VALUES:
      self.consumir(self.tipo_atual())  # Consome o token correspondente a verdadeiro ou falso
    elif self.token_atual() == '(':
      self.consumir('Delimitador')  # Consome o token correspondente ao parêntese aberto
      self.f_expressao()  # Chamada para analisar uma expressão
      if self.token_atual() != ')':
        self.mensagem_token(f"Esperava o delimitador ')', mas foi encontrado {self.token_atual()}")
        escrever_erro_sintatico(self.tokens[self.posicao])
        exit()
      else:
        self.consumir('Delimitador')  # Consome o token correspondente ao parêntese fechado
        print(f"[DEBUG] consumindo {self.tipo_atual()} de valor {self.token_atual()}")
        self.consumir(self.tipo_atual())
    elif self.token_atual() == 'not':
      self.consumir('Palavra Reservada')  # Consome o token correspondente ao operador lógico NOT
      self.f_fator()  # Chamada recursiva para analisar o fator após o NOT
    else:
      self.mensagem_token(f"Esperava um fator, mas foi encontrado {self.token_atual()}")
      escrever_erro_sintatico(self.tokens[self.posicao])
      exit()

  def f_expressao_simples(self):
    print(f"[DEBUG] #D {self.token_atual()} {self.tipo_atual()}")
    if self.token_atual() in SINAL:
      self.consumir(self.tipo_atual())
      self.f_termo()
      self.f_expressao_simples_linha()
    else:
      self.f_termo()
      self.f_expressao_simples_linha()
 
  def f_expressao_simples_linha(self):
    if self.token_atual() in OP_ADITIVO:
      self.consumir(self.token_atual())
      self.f_termo()
      self.f_expressao_simples_linha()

  def f_expressao(self):
    self.f_expressao_simples()  # Primeiro, analisa uma expressão simples
    self.f_expressao_linha()

  def f_expressao_linha(self):
    if self.token_atual() in OP_RELACIONAL:  # Se encontrar um operador relacional
      self.consumir(self.tipo_atual)  # Consome o operador relacional
      self.f_expressao_simples()  # Em seguida, analisa outra expressão simples

  def f_lista_de_expressao(self):
    self.f_expressao()  # Analisa a primeira expressão da lista
    while self.token_atual() == ',':
      self.consumir('Delimitador')  # Consome a vírgula
      self.f_expressao()  # Analisa a próxima expressão na lista

  def f_termo(self):
    self.f_fator()  # Analisa o primeiro fator do termo
    self.f_termo_linha()
    
  def f_termo_linha(self):
    if self.token_atual in OP_MULTIPLICATIVO:
      self.consumir(self.tipo_atual)  # Consome o operador multiplicativo
      self.f_fator()  # Analisa o próximo fator no termo
      self.f_termo_linha()

  def f_ativacao_procedimento(self):
    print(f"[DEBUG] #E1 {self.token_atual()} {self.tipo_atual()}")
    if self.tipo_atual() == 'Identificador':
      self.consumir('Identificador')  # Consome o identificador do procedimento
      print(f"[DEBUG] #E2 {self.token_atual()} {self.tipo_atual()}")
      if self.token_atual() == '(':
        self.consumir('Delimitador')  # Consome o '('
        self.f_lista_de_expressoes()  # Analisa a lista de expressões
        if self.token_atual() == ')':
          self.consumir('Delimitador')  # Consome o ')'
        else:
          self.mensagem_token(f"Esperava o delimitador ')', mas foi encontrado {self.token_atual()}")
          escrever_erro_sintatico(self.tokens[self.posicao])
          exit()
      else:
        self.f_expressao_simples()
        # self.mensagem_token(f"Esperava o delimitador '(', mas foi encontrado {self.token_atual()}")
        # escrever_erro_sintatico(self.tokens[self.posicao])
        # exit()
    else:
      self.mensagem_token(f"Esperava um identificador, mas foi encontrado {self.token_atual()}")
      escrever_erro_sintatico(self.tokens[self.posicao])
      exit()

  # def f_ativacao_procedimento_linha():

  # *** Regras dependentes mais complexas
  def f_comando(self): 
    """Analisa possibilidades de comando, como atrobuição, ativações de procedimentos e outros"""
    print(f"[DEBUG] #C {self.token_atual()} {self.tipo_atual()}")
    if self.tipo_atual() == 'Identificador' and self.tokens[self.posicao + 1].type == 'Atribuição':
      self.f_variavel();
      if self.tipo_atual() == 'Atribuição':
        print(f"[DEBUG] #A {self.token_atual()} {self.tipo_atual()}")
        self.consumir('Atribuição')
        print(f"[DEBUG] #B {self.token_atual()} {self.tipo_atual()}")
        self.f_expressao()
    # elif self.tipo_atual() == 'Identificador' and (self.tokens[self.posicao + 1].value in OP_ADITIVO):
    #   print("É aqui!")
    elif self.tipo_atual() == 'Identificador':
      self.f_ativacao_procedimento()
    elif self.token_atual() == 'begin':
      self.f_comando_composto()
    elif self.token_atual() == 'if':
      self.consumir('Palavra reservada')
      self.f_expressao()
      if self.token_atual() == 'then':
        self.consumir("Palavra reservada")
        self.f_comando()
        self.f_parte_else()
      else:
        self.mensagem_token(f"Esperava um a palavra reservada then, mas foi encontrado {self.token_atual()}")
        escrever_erro_sintatico(self.tokens[self.posicao])
        exit()
    elif self.token_atual() == 'while':
      self.consumir('Palavra reservada')
      self.f_expressao()
      if self.token_atual == 'do':
        self.consumir('Palavra reservada')
        self.f_comando_composto()
      else: 
        self.mensagem_token(f"Esperava um a palavra reservada do, mas foi encontrado {self.token_atual()}")
        escrever_erro_sintatico(self.tokens[self.posicao])
        exit()
    # Caso extra não informado pelo professor, mas implementado
    elif self.token_atual() == 'for':
      self.consumir('Palavra reservada')
      self.f_variavel()
      if self.tipo_atual() == 'Atribuição':
        self.consumir('Atribuição')
        self.f_expressao()
        if self.token_atual == 'to':
          self.consumir('Palavra reservada')
          self.f_expressao()
          if self.token_atual == 'do':
            self.consumir('Palavra reservada')
            self.f_comando_composto()
          else:
            self.mensagem_token(f"Esperava um a palavra reservada do, mas foi encontrado {self.token_atual()}")
            escrever_erro_sintatico(self.tokens[self.posicao])
            exit()
        else:
          self.mensagem_token(f"Esperava um a palavra reservada to, mas foi encontrado {self.token_atual()}")
          escrever_erro_sintatico(self.tokens[self.posicao])
          exit()
      else:
        self.mensagem_token(f"Esperava símbolo de atribuição :=, mas foi encontrado {self.token_atual()}")
        escrever_erro_sintatico(self.tokens[self.posicao])
        exit()
    else:
      if self.token_atual() == 'end' and self.tokens[self.posicao + 1].value == '.':
        return "Comando avaliado com sucesso"
      print(f"[DEBUG] {self.token_atual()} {self.tipo_atual()}")
      self.mensagem_token(f"Comando inválido. Recebido: {self.token_atual()} de tipo {self.tipo_atual()}")
      escrever_erro_sintatico(self.tokens[self.posicao])
      exit()

  def f_lista_comandos(self): 
    self.f_comando()
    self.f_lista_comandos_linha()
  
  def f_lista_comandos_linha(self):
    if self.token_atual() == ';':
      self.consumir('Delimitador')
      self.f_comando()
      self.f_lista_comandos_linha()

  def f_comandos_opcionais(self):
    while self.token_atual() in ['begin', 'if', 'while', 'for'] or self.tipo_atual() == 'Identificador':
      self.f_lista_comandos()
      if self.token_atual() == 'end':
        break # Se chegar o end do bloco, não tentará processar mais nada

  def f_comando_composto(self):
    if self.token_atual() == 'begin':
      self.count_begin += 1
      self.consumir('Palavra reservada')
      self.f_comandos_opcionais()
      if(self.token_atual()) == 'end' and self.tokens[self.posicao + 1].value == '.' and self.count_begin == 1:
        return "Programa finalizado com sucesso."
      elif self.token_atual == 'end':
        self.count_begin -= 1 # desempilha, pois encontrou o seu par
        self.consumir('Palavra reservada')
      else: 
        self.f_lista_comandos()
        if(self.token_atual()) == 'end' and self.tokens[self.posicao + 1].value == '.' and self.count_begin == 1:
          return "Programa finalizado com sucesso."
        else:
          self.mensagem_token(f"Esperava a palavra reservada end, mas foi encontrado {self.token_atual()}")
          escrever_erro_sintatico(self.tokens[self.posicao])
          exit()
    else: 
      self.mensagem_token(f"Esperava a palavra reservada begin, mas foi encontrado {self.token_atual()}")
      escrever_erro_sintatico(self.tokens[self.posicao])
      exit()

  def f_variavel(self):
    """Analisa uma variável na gramática."""
    if self.tipo_atual() == 'Identificador':
        self.consumir('Identificador')  # Consome o token correspondente a um identificador
    else:
        self.mensagem_token(f"Esperava um identificador, mas foi encontrado {self.token_atual()}")
        escrever_erro_sintatico(self.tokens[self.posicao])
        exit()

  def f_lista_de_parametros(self):
    """Analisa uma lista de parâmetros na gramática."""
    self.f_lista_de_identificadores()  # Analisa a lista de identificadores
    if self.token_atual() == ':':
      self.consumir('Delimitador')  # Consome o token ':' que separa a lista de identificadores do tipo
      self.f_tipo()  # Analisa o tipo dos parâmetros
      self.f_lista_de_parametros_linha()  # Chama o método para analisar a próxima linha de parâmetros
    else: 
      self.mensagem_token(f"Esperava um delimitador ':', mas foi encontrado {self.token_atual()}")
      escrever_erro_sintatico(self.tokens[self.posicao])

  def f_lista_de_parametros_linha(self):
    """Analisa uma linha de parâmetros na gramática."""
    if self.token_atual() == ';':
      self.consumir('Delimitador')  # Consome o token ';'
      self.f_lista_de_identificadores()  # Analisa a lista de identificadores
      if self.token_atual() == ':':
        self.consumir('Delimitador')  # Consome o token ':' que separa a lista de identificadores do tipo
        self.f_tipo()  # Analisa o tipo dos parâmetros
        self.f_lista_de_parametros_linha()  # Chama o método recursivamente para analisar a próxima linha de parâmetros
    elif self.token_atual() == ',':
      self.consumir('Delimitador')  # Consome o token ':' que separa a lista de identificadores do tipo
      self.f_lista_de_identificadores()  # Analisa a lista de identificadores
      if self.token_atual() == ':':
        self.consumir('Delimitador')  # Consome o token ':' que separa a lista de identificadores do tipo
        self.f_tipo()  # Analisa o tipo dos parâmetros
        self.f_lista_de_parametros_linha() # chamada recursiva
    else:
      self.mensagem_token(f"Esperava um delimitador ';', mas foi encontrado {self.token_atual()}")
      escrever_erro_sintatico(self.tokens[self.posicao])

  def f_argumentos(self):
    """Analisa os argumentos na gramática."""
    if self.token_atual() == '(':
      self.consumir('Delimitador')  # Consome o '('
      self.f_lista_de_parametros()
      if self.token_atual() == ')':
        self.consumir('Delimitador')  # Consome o ')'
      else:
        self.mensagem_token(f"Esperava um delimitador ')', mas foi encontrado {self.token_atual()}")
        escrever_erro_sintatico(self.tokens[self.posicao])

  def f_declaracao_de_subprograma(self):
    """Analisa uma declaração de subprograma na gramática."""
    if self.token_atual() == 'procedure':
      self.consumir('Palavra reservada')  # Consome a palavra reservada 'procedure'
      self.f_id()
      self.f_argumentos()
      if self.token_atual() == ';':
        self.consumir('Delimitador')
        self.f_declaracoes_variaveis()
        self.f_declaracoes_de_subprogramas()
        self.f_comando_composto()
      else:
        self.mensagem_token(f"Esperava o delimitador ';', mas foi encontrado {self.token_atual()}")
        escrever_erro_sintatico(self.tokens[self.posicao])
        exit()
    else:
      self.mensagem_token(f"Esperava a palavra reservada 'procedure', mas foi encontrado {self.token_atual()}")
      escrever_erro_sintatico(self.tokens[self.posicao])
      exit()

  def f_declaracoes_de_subprogramas(self):
    """Analisa declarações de subprogramas na gramática."""
    if self.token_atual() == 'procedure':
      self.f_declaracao_de_subprograma()
      if self.token_atual() == ';':
        self.consumir('Delimitador') 
        self.f_declaracoes_de_subprogramas()
      else: 
        self.mensagem_token(f"Esperava o delimitador ';', mas foi encontrado {self.token_atual()}")
        escrever_erro_sintatico(self.tokens[self.posicao])
        exit()
  
  def f_lista_de_identificadores(self):
    """Analisa uma lista de identificadores na gramática."""
    if self.tipo_atual() == 'Identificador':
        self.consumir('Identificador')  # Consome o primeiro identificador
        self.f_lista_de_identificadores_linha()  # Chama o método para analisar o restante da lista de identificadores
    else:
        self.mensagem_token(f"Esperava um identificador, mas foi encontrado {self.token_atual()}")
        escrever_erro_sintatico(self.tokens[self.posicao])
        exit() 

  def f_lista_de_identificadores_linha(self):
    """Analisa o restante da lista de identificadores na gramática."""
    if self.token_atual() == ',':
      self.consumir('Delimitador')  # Consome a vírgula
      # Após consumir um Delimitador, busca por consumir um Identificador
      if self.tipo_atual() == 'Identificador':
        self.consumir('Identificador')  # Consome o próximo identificador
        self.f_lista_de_identificadores_linha()  # Chama recursivamente o método para analisar mais identificadores
      else:
        self.mensagem_token(f"Esperava um identificador após a vírgula, mas foi encontrado {self.token_atual()}")
        escrever_erro_sintatico(self.tokens[self.posicao])
        exit()  # Encerra o programa em caso de erro grave
    # Caso não haja mais identificadores após a vírgula, a produção é epsilon (vazio)
    # Não é necessário fazer nada nesse caso, pois a lista pode terminar aqui
        
  def f_lista_declaracoes_variaveis(self):
    self.f_lista_de_identificadores()  # Analisa a lista de identificadores
    if self.token_atual() == ':':
      self.consumir('Delimitador')  # Consome o token ':' que separa a lista de identificadores do tipo
      self.f_tipo()  # Analisa o tipo das variáveis
      self.f_lista_declaracoes_variaveis_linha()  # Chama o método para l

  def f_lista_declaracoes_variaveis_linha(self):
    if self.token_atual() == ';':
      self.consumir('Delimitador')  # Consome o token ';
      self.f_lista_de_identificadores()
      if self.token_atual() == ':':
        self.consumir('Delimitador')
        self.f_tipo()
        self.f_lista_declaracoes_variaveis_linha()  # Chama o método recursivamente para analisar a próxima linha de declarações de variáveis
    else:
      self.mensagem_token(f"Esperava um delimitador ';', mas foi encontrado {self.token_atual()}")
      escrever_erro_sintatico(self.tokens[self.posicao])

  def f_declaracoes_variaveis(self):
    """Verifica se há declarações de variáveis, consome a palavra reservada 'var' e verifica a lista de identificadores"""
    if self.token_atual() == 'var':
      self.consumir('Palavra reservada')
      self.f_lista_de_identificadores()
      if self.token_atual() == ':':
        self.consumir('Delimitador')
        self.f_tipo()
        if self.token_atual() == ';':
          self.consumir('Delimitador')
          self.f_declaracoes_variaveis()  # Chamada recursiva para analisar mais declarações de variáveis
    # else:
    #   self.mensagem_token(f"Esperava a palavra reservada var, mas foi encontrado {self.token_atual()}")
    #   escrever_erro_sintatico(self.tokens[self.posicao])    
  
  def f_parte_else(self):
    if self.token_atual() == 'else':
      self.consumir('Palavra reservada')
      self.f_comando()

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

source_file1 = 'lexico1.csv'
source_file2 = 'lexico2.csv'
source_file3 = 'lexico3.csv'
source_file4 = 'lexico4.csv'
source_file5 = 'lexico5.csv'

# output_file = 'sintatico.csv'  # Nome do arquivo de saída
output_file1 = 'sintatico1.csv' 
output_file2 = 'sintatico2.csv' 
output_file3 = 'sintatico3.csv' 
output_file4 = 'sintatico4.csv' 
output_file5 = 'sintatico5.csv' 

# Escreve o arquivo de saída do analisador sintático
def escrever_erro_sintatico(token):
  """Escreve o arquivo de saída do analisador sintático"""
  # Abre o arquivo de saída em modo de escrita
  with open(output_file5, "a") as arquivo_saida:
    # Escreve a mensagem de erro no arquivo
    arquivo_saida.write(f"Erro sintático na linha {token.line}: '{token.erro_sintatico}'\n")

tokens = ler_tokens(source_file5)

analisador = Sintatico(tokens, output_file=output_file5, input_file=source_file5)
analisador.analisar()