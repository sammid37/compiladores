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
    self.posicao = 0 # ? posição do token na lista de tuplas
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
    return self.tipo_atual == tipo

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
    # TODO: self.f_declaracoes_de_subprogramas() 
    self.f_comando_composto() # TODO: está incompleto!
    # Final: verificar se há o delimitador '.', ponto final
    self.f_fim_program()
 
  # TODO: método para gerar a saída do Analisador Sintático //enthony
    # def gerar_saida(self): 
    #   with open(self.output_file, 'w') as csvfile: #fazendo a escrita do arquivo de saída
    #     writer = csv.writer(csvfile) #criando um objeto para escrita
    #     writer.writerow(['Classificação', 'Token', 'Linha']) #escrevendo o cabeçalho

    #   for token in self.tokens: #percorrendo a lista de tokens
    #     writer.writerow([token.type, token.value, token.line]) #escrevendo os tokens no arquivo de saída
  
  # ---------------------------------------------------------------------- REGRAS
  def f_program(self): 
    """Verifica se o programa começa com a palavra reservada program"""
    print(self.token_atual())
    if self.token_atual() == 'program':
      self.consumir(self.tipo_atual())
    else: 
      self.mensagem_token(f"Esperava a palavra reservada 'program', mas foi encontrado {self.token_atual()}")
      escrever_erro_sintatico(self.tokens[self.posicao])
      exit()

  def f_fim_program(self):
    """Verifica se o programa começa com o delimitador ponto final"""
    if self.token_atual() in DELIMITER and self.token_atual() == '.':
      self.consumir(self.tipo_atual())
    else: 
      self.mensagem_token(f"Esperava o delimitador '.', mas foi encontrado {self.token_atual()}")
      escrever_erro_sintatico(self.tokens[self.posicao])
      exit()

  def f_id(self): 
    # TODO: verificar se é necessário fazer um tratamento para tokens do tipo ID
    if(self.tipo_atual()) == 'Identificador':
      self.consumir(self.tipo_atual())
    else: 
      self.mensagem_token(f"Esperava um identificador, mas foi encontrado {self.token_atual()}")
      escrever_erro_sintatico(self.tokens[self.posicao])
      exit()

  def f_delimiter_program(self): 
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

  # ** Regras dependentes simples - TENTATIVAAAAAAA 
  def f_fator(self):
    if self.tipo_atual() == 'Identificador':
      self.consumir('Identificador')  # Consome o token correspondente a um identificador
      if self.token_atual() == '(':
        self.consumir('Delimitador')  # Consome o token correspondente ao parêntese aberto
        self.f_lista_de_expressoes()  # Chamada para analisar uma lista de expressões
        if self.token_atual() == ')':
          self.consumir('Delimitador')  # Consome o token correspondente ao parêntese fechado
        else:
          self.mensagem_token(f"Esperava delimitador ')', mas foi encontrado {self.token_atual()}")
          escrever_erro_sintatico(self.tokens[self.posicao])
          exit()
    elif self.tipo_atual() == 'Palavra reservada' and self.token_atual == 'integer':
      self.consumir('Palavra reservada')  # Consome o token correspondente a um número inteiro
    elif self.tipo_atual() == 'Palavra reservada' and self.token_atual() == 'real':
      self.consumir('Palavra reservada')  # Consome o token correspondente a um número real
    elif self.tipo_atual() in ['TRUE', 'FALSE']:
      self.consumir(self.tipo_atual())  # Consome o token correspondente a verdadeiro ou falso
    elif self.token_atual == '(':
      self.consumir('Delimitador')  # Consome o token correspondente ao parêntese aberto
      self.f_expressao()  # Chamada para analisar uma expressão
      if self.token_atual == ')':
        self.consumir('Delimitador')  # Consome o token correspondente ao parêntese fechado
      else:
        self.mensagem_token(f"Esperava o delimitador ')', mas foi encontrado {self.token_atual()}")
        escrever_erro_sintatico(self.tokens[self.posicao])
        exit()
    elif self.token_atual() in SINAL:
      self.consumir(self.token_atual())  # Consome o token correspondente ao sinal
      self.f_fator()  # Chamada recursiva para analisar outro fator após o sinal
    elif self.token_atual() == 'NOT':
      self.consumir('Palavra Reservada')  # Consome o token correspondente ao operador lógico NOT
      self.f_fator()  # Chamada recursiva para analisar o fator após o NOT
    else:
      self.mensagem_token(f"Esperava o delimitador '(', mas foi encontrado {self.token_atual()}")
      escrever_erro_sintatico(self.tokens[self.posicao])
      exit()

  def f_expressao_simples(self):
    self.f_termo()  # Primeiro, analisa um termo
    while self.token_atual() in SINAL:  # Enquanto encontrar operadores de adição ou subtração
      self.consumir(self.token_atual)  # Consome o operador
      self.f_termo()  # Em seguida, analisa outro termo

  def f_expressao(self):
    self.f_expressao_simples()  # Primeiro, analisa uma expressão simples
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
    while self.token_atual in OP_MULTIPLICATIVO:
      self.consumir(self.tipo_atual)  # Consome o operador multiplicativo
      self.f_fator()  # Analisa o próximo fator no termo

  def f_ativacao_procedimento(self):
    if self.tipo_atual() == 'Identificador':
      self.consumir('Identificador')  # Consome o identificador do procedimento
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
        self.mensagem_token(f"Esperava o delimitador '(', mas foi encontrado {self.token_atual()}")
        escrever_erro_sintatico(self.tokens[self.posicao])
        exit()
    else:
      self.mensagem_token(f"Esperava um identificador, mas foi encontrado {self.token_atual()}")
      escrever_erro_sintatico(self.tokens[self.posicao])
      exit()

  # *** Regras dependentes mais complexas
  def f_comando(self): 
    if self.tipo_atual() == 'Identificador':
      self.consumir('Identificador')
      if self.token_atual in ATRIBUICAO:
        self.consumir('Atribuição')
        self.f_expressao()
      else:
        self.mensagem_token(f"Esperava símbolo de atribuição, mas foi encontrado {self.token_atual()}")
        escrever_erro_sintatico(self.tokens[self.posicao])
        exit()
    elif self.tipo_atual() == 'Palavra reservada' and self.token_atual() in ['if', 'while']:
      if self.token_atual() == 'if':
        self.f_expressao()
        if self.token_atual() == 'then':
          self.consumir("Palavra reservada")
          self.f_comando()
          if self.token_atual == 'else':
            self.consumir('Palavra reservada')
            self.f_comando()
          else:
            self.mensagem_token(f"Esperava a palavra reservada 'else', mas foi encontrado {self.token_atual()}")
            escrever_erro_sintatico(self.tokens[self.posicao])
            exit()
        else:
          self.mensagem_token(f"Esperava a palavra reservada 'then', mas foi encontrado {self.token_atual()}")
          escrever_erro_sintatico(self.tokens[self.posicao])
          exit()
      elif self.token_atual() == 'while':
        self.f_iterativo()
    # elif self.tipo_atual() == 'Palavra reservada' and self.token_atual() == 'begin':
    #   self.f_comando_composto()
    # elif self.tipo_atual() == 'Identificador' or self.tipo_atual() == 'Palavra reservada' and self.token_atual() == 'write':
    #   self.ativacao_de_procedimento()  
    else: 
      self.mensagem_token(f"Comando inválido.")
      escrever_erro_sintatico(self.tokens[self.posicao])
      exit()

  def f_lista_comandos(self): 
    self.comando()
    while self.token_atual() == ';':
      self.consumir('DELIMITADOR')
      self.comando()
  # def f_comandos_opcionais(self): pass

  def f_comando_composto(self):
    if(self.token_atual()) == 'begin':
      self.consumir('Palavra reservada')
      self.f_lista_comandos()
      if(self.token_atual()) == 'end':
        self.consumir('Palavra reservada')
      else: 
        self.mensagem_token(f"Esperava a palavra reservada end, mas foi encontrado {self.token_atual()}")
        escrever_erro_sintatico(self.tokens[self.posicao])
        exit()
    else: 
      self.mensagem_token(f"Esperava a palavra reservada begin, mas foi encontrado {self.token_atual()}")
      escrever_erro_sintatico(self.tokens[self.posicao])
      exit()
  
  # ??? SEM CATEGORIA, ORGANIZAR!!
  def f_variavel(self):
    """Analisa uma variável na gramática."""
    if self.tipo_atual() == 'Identificador':
        self.consumir('Identificador')  # Consome o token correspondente a um identificador
    else:
        self.mensagem_token(f"Esperava um identificador, mas foi encontrado {self.token_atual()}")
        escrever_erro_sintatico(self.tokens[self.posicao])
        exit()

  def f_lista_de_parametros(self): pass
  def f_argumentos(self): pass
  def f_declaracao_de_subprograma(self): pass
  def f_declaracoes_de_subprogramas(self): pass
  
  def f_lista_de_identificadores(self):
    if self.tipo_atual == 'Identificador':
      self.consumir('Identificador')  # Consome o token correspondente a um identificador
      while self.token_atual == ',':
        self.consumir(',')  # Consome a vírgula
        self.consumir('Identificador')  # Consome o próximo identificador
    else:
      escrever_erro_sintatico(self.tokens[self.posicao])
      exit()
        
  def f_lista_declaracoes_variaveis(self):
    self.f_lista_de_identificadores()  # Analisa a lista de identificadores
    if self.token_atual == ';':
      self.consumir('Delitador')  # Consome o token ':' que separa a lista de identificadores do tipo
      self.f_tipo()  # Analisa o tipo das variáveis
      self.f_lista_declaracoes_variaveis_linha()  # Chama o método para l

  def f_lista_declaracoes_variaveis_linha(self):
    if self.token_atual == ';':
      self.consumir('Delimitador')  # Consome o token ';
      self.f_lista_de_identificadores()
      if self.token_atual == ':':
        self.consumir('Delimitador')
        self.f_tipo()
        self.f_lista_declaracoes_variaveis_linha()  # Chama o método recursivamente para analisar a próxima linha de declarações de variáveis
    else:
      self.mensagem_token(f"Esperava um delimitador, mas foi encontrado {self.token_atual()}")
      escrever_erro_sintatico(self.tokens[self.posicao])

  def f_declaracoes_variaveis(self):
    # Verifica se contém a palavra reservada var para prosseguir com a lista de IDs
    if self.token_atual == 'var':
      self.consumir('Palavra reservada')
      self.f_lista_de_identificadores()
      if self.token_atual in DELIMITER and self.token_atual == ':':
        self.consumir('Delimitador')
        self.f_tipo()
      self.f_lista_declaracoes_variaveis()
    else:
      escrever_erro_sintatico(self.tokens[self.posicao])
  
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

# Escreve o arquivo de saída do analisador sintático
def escrever_erro_sintatico(token):
  """Escreve o arquivo de saída do analisador sintático"""
  # Abre o arquivo de saída em modo de escrita
  with open(output_file, "a") as arquivo_saida:
    # Escreve a mensagem de erro no arquivo
    arquivo_saida.write(f"Erro sintático na linha {token.line}: '{token.erro_sintatico}'\n")

tokens = ler_tokens(source_file)

analisador = Sintatico(tokens, output_file=output_file, input_file=source_file)
analisador.analisar()