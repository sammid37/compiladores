# Construção de Compiladores
# Analisador Sintático
# Enthony e Samantha

import re
import csv

from tokens import Token

from constantes import *
from termcolor import colored

# Definição de um Token: tipo, valor e linha onde se localiza
       
# Definição de um Analisador Sintático
class Sintatico:
  def __init__(self, tokens):
    self.tokens = tokens # a lista de tokens (formado por uma tupla << type, value, line >>)
    self.posicao = 0 # posição do token na lista de tuplas
    self.count_begin = 0 # indicador para pares begin e end
    self.input_file = None
    self.output_syntax = None

  def set_input_file(self, input_file):
    self.input_file = input_file

  def set_output_syntax(self, output_syntax):
    self.output_syntax = output_syntax

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
    print(colored("-----"*8,'green'))
    print(colored("Análise sintática concluída com sucesso.", 'green'))
    print(colored("-----"*8,'green'))

  def programa(self):
    """Contém regras (subregras) de um programa em Pascal"""
    print("teste")
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

  #* <<REVISAR>> -> não-determinismo, p/ ID (lista_expressao) vira ID com Argumentos (GPT)
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
        if self.tipo_atual() == 'Delimitador':
          self.consumir('Delimitador')  # Consome o token correspondente ao parêntese fechado
        #? gambiarra de última hora, deveria trazer um erro de sintax
        else: pass 
        # self.consumir(self.tipo_atual())
    elif self.token_atual() == 'not':
      self.consumir('Palavra Reservada')  # Consome o token correspondente ao operador lógico NOT
      self.f_fator()  # Chamada recursiva para analisar o fator após o NOT
    # TODO: pensar em outra estratégia para tratar erros de fator
    # else:
    #   self.mensagem_token(f"Esperava um fator, mas foi encontrado {self.token_atual()}")
    #   escrever_erro_sintatico(self.tokens[self.posicao])
    #   exit()
  #* <<REVISAR>>
  def f_expressao_simples(self):
    if self.token_atual() in SINAL:
      self.consumir(self.tipo_atual())
      self.f_termo()
      self.f_expressao_simples_linha()
    else:
      self.f_termo()
      self.f_expressao_simples_linha()
 
  def f_expressao_simples_linha(self):
    if self.token_atual() in OP_ADITIVO:
      self.consumir(self.tipo_atual())
      self.f_termo()
      self.f_expressao_simples_linha()
  #* <<REVISAR>> pq ela chama expressão simples em 2 casos
  def f_expressao(self):
    self.f_expressao_simples()  # Primeiro, analisa uma expressão simples
    self.f_expressao_linha()
  #* <<REVISAR>>
  def f_expressao_linha(self):
    if self.token_atual() in OP_RELACIONAL:  # Se encontrar um operador relacional
      self.consumir(self.tipo_atual())  # Consome o operador relacional
      self.f_expressao_simples()  # Em seguida, analisa outra expressão simples
  #* <<REVISAR>>
  def f_lista_de_expressao(self):
    self.f_expressao()  # Analisa a primeira expressão da lista
    while self.token_atual() == ',':
      self.consumir('Delimitador')  # Consome a vírgula
      self.f_expressao()  # Analisa a próxima expressão na lista
  #* <<REVISAR>>
  def f_termo(self):
    self.f_fator()  # Analisa o primeiro fator do termo
    self.f_termo_linha()
    
  def f_termo_linha(self):
    if self.token_atual() in OP_MULTIPLICATIVO:
      self.consumir('Operador multiplicativo')  # Consome o operador multiplicativo
      self.f_fator()  # Analisa o próximo fator no termo
      self.f_termo_linha()
  #* <<REVISAR>> não-determinismo!! (vai tratar o problema do fator())
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
    if self.tipo_atual() == 'Identificador' and self.tokens[self.posicao + 1].type == 'Atribuição':
      self.f_variavel();
      if self.tipo_atual() == 'Atribuição':
        self.consumir('Atribuição')
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
      if self.token_atual() == 'do':
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
        if self.token_atual() == 'to':
          self.consumir('Palavra reservada')
          self.f_expressao()
          if self.token_atual() == 'do':
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
      # self.mensagem_token(f"Comando inválido. Recebido: {self.token_atual()} de tipo {self.tipo_atual()}")
      # escrever_erro_sintatico(self.tokens[self.posicao])
      # exit()
  #? <<OK>>
  def f_lista_comandos(self): 
    self.f_comando()
    self.f_lista_comandos_linha()
  
  def f_lista_comandos_linha(self):
    """Verifica se ao final de um comando há um delimitador ';' e se há mais comandos em linha"""
    if self.token_atual() == ';':
      self.consumir('Delimitador')
      self.f_comando()
      self.f_lista_comandos_linha()

  def f_comandos_opcionais(self):
    while self.token_atual() in ['begin', 'if', 'while', 'for'] or self.tipo_atual() == 'Identificador':
      self.f_lista_comandos()
      # GAMBIARRA
      # print(f"iiiiiiiii{self.token_atual()}")
      if (self.token_atual() == 'end' and self.tokens[self.posicao -1].value == ';') or self.tokens[self.posicao -1].value == 'end':
        break # Se chegar o end do bloco, não tentará processar mais nada
      else: 
        self.mensagem_token("Esperava um delimitador ';' antes do end.")
        escrever_erro_sintatico(self.tokens[self.posicao])
        exit()
  def f_comando_composto(self):
    if self.token_atual() == 'begin':
      self.count_begin += 1
      self.consumir('Palavra reservada')
      self.f_comandos_opcionais()
      if self.token_atual() == 'end' and self.tokens[self.posicao + 1].value == '.' and self.count_begin == 1:
        return "Programa finalizado com sucesso."
      elif self.token_atual() == 'end':
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
  #? <<OK>>
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
  #* <<REVISAR>>
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
  #?? <<OK>>  
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
  #?? <<OK>>      
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
  
  #????? entender pq que não tá funcionando
  def f_parte_else(self):
    if self.token_atual() == 'else':
      self.consumir(self.tipo_atual())
      self.f_comando()


# Escreve o arquivo de saída do analisador sintático
def escrever_erro_sintatico(token):
  pass
  # """Escreve o arquivo de saída do analisador sintático"""
  # # Abre o arquivo de saída em modo de escrita
  # with open(output_file1, "a") as arquivo_saida:
  #   # Escreve a mensagem de erro no arquivo
  #   arquivo_saida.write(f"Erro sintático na linha {token.line}: '{token.erro_sintatico}'\n")
  # print(colored("-----"*8,'red'))
  # print(colored("Erro sintático encontrado. Verifique o arquivo gerado.",'red'))
  # print(colored("-----"*8,'red'))

