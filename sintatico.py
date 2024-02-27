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
    print(self.token_atual())
    if self.token_atual() == 'program':
      self.consumir('Palavra reservada')
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
    print(TIPO)
    print(self.token_atual())
    print(self.tipo_atual())

    if self.token_atual() in TIPO:
      self.consumir(self.tipo_atual())
    else:
      self.mensagem_token(f"Esperava algum tipo tipo de variável, mas foi encontrado {self.token_atual()}")
      escrever_erro_sintatico(self.tokens[self.posicao])
      exit()

  # ** Regras dependentes simples
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
    elif self.tipo_atual() == 'Número inteiro':
      self.consumir('Número inteiro')  # Consome o token correspondente a um número inteiro
    elif self.tipo_atual() == 'Número real':
      self.consumir('Número real')  # Consome o token correspondente a um número real
    elif self.tipo_atual() in BOOLEAN_VALUES:
      self.consumir(self.tipo_atual())  # Consome o token correspondente a verdadeiro ou falso
    elif self.token_atual() == '(':
      self.consumir('Delimitador')  # Consome o token correspondente ao parêntese aberto
      self.f_expressao()  # Chamada para analisar uma expressão
      if self.token_atual() == ')':
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
    """Analisa possibilidades de comando, como atrobuição, ativações de procedimentos e outros"""
    if self.tipo_atual() == 'Identificador' and self.tokens[self.posicao + 1].type == 'Atribuição':
      self.f_variavel();
      if self.tipo_atual() == 'Atribuição':
        self.consumir('Atribuição')
        self.f_expressao()
    elif self.tipo_atual == 'Identificador':
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
      self.mensagem_token(f"Comando inválido")
      escrever_erro_sintatico(self.tokens[self.posicao])
      exit()

  def f_lista_comandos(self): 
    self.f_comando()
    while self.token_atual() == ';':
      self.consumir('DELIMITADOR')
      self.f_comando()
  
  def f_comandos_opcionais(self):
    while self.token_atual() in ['begin', 'if', 'while', 'for'] or self.tipo_atual() == 'Identificador':
      self.f_lista_comandos()
      if self.token_atual() == 'end':
        break # Se chegar o end do bloco, não tentará processar mais nada

  def f_comando_composto(self):
    if self.token_atual() == 'begin':
      self.count_begin += 1
      print("[DEBUG] Begins encontrados: " + str(self.count_begin))
      self.consumir('Palavra reservada')
      self.f_comandos_opcionais()
      if(self.token_atual()) == 'end' and self.tokens[self.posicao + 1].value == '.' and self.count_begin == 1:
        return "Programa finalizado com sucesso."
      elif self.token_atual == 'end':
        self.count_begin -= 1 # desempilha, pois encontrou o seu par
        print("[DEBUG] Begins encontrados: " + str(self.count_begin))
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

  def f_lista_de_parametros_linha(self):
    """Analisa uma linha de parâmetros na gramática."""
    if self.token_atual() == ';':
      self.consumir('Delimitador')  # Consome o token ';'
      self.f_lista_de_identificadores()  # Analisa a lista de identificadores
      if self.token_atual() == ':':
        self.consumir('Delimitador')  # Consome o token ':' que separa a lista de identificadores do tipo
        self.f_tipo()  # Analisa o tipo dos parâmetros
        self.f_lista_de_parametros_linha()  # Chama o método recursivamente para analisar a próxima linha de parâmetros
    else:
      self.mensagem_token(f"Esperava um delimitador ';', mas foi encontrado {self.token_atual()}")
      escrever_erro_sintatico(self.tokens[self.posicao])

  def f_argumentos(self):
    """Analisa os argumentos na gramática."""
    if self.token_atual() == '(':
      self.consumir('Delimitador')  # Consome o '('
      if self.token_atual() != ')':
        self.f_lista_de_parametros()  # Analisa a lista de parâmetros
      if self.token_atual() == ')':
        self.consumir('Delimitador')  # Consome o ')'
    # Se não houver argumentos, não há necessidade de consumir tokens

  def f_declaracao_de_subprograma(self):
    """Analisa uma declaração de subprograma na gramática."""
    if self.token_atual() == 'procedure':
      self.consumir('Palavra reservada')  # Consome a palavra reservada 'procedure'
      self.f_id()  # Analisa o identificador do subprograma
      self.f_argumentos()  # Analisa os argumentos do subprograma
      self.f_delimiter_program()  # Verifica o delimitador ':'
      self.f_declaracoes_variaveis()  # Analisa as declarações de variáveis
      self.f_declaracoes_de_subprogramas()  # Analisa as declarações de subprogramas
      self.f_comando_composto()  # Analisa o comando composto
    else:
      self.mensagem_token(f"Esperava a palavra reservada 'procedure', mas foi encontrado {self.token_atual()}")
      escrever_erro_sintatico(self.tokens[self.posicao])

  def f_declaracoes_de_subprogramas(self):
    """Analisa declarações de subprogramas na gramática."""
    self.f_declaracao_de_subprograma()
    self.f_declaracoes_de_subprogramas_linha()

  def f_declaracoes_de_subprogramas_linha(self):
    """Analisa a linha de declarações de subprogramas na gramática."""
    if self.token_atual() == ';':
      self.consumir('Delimitador')  # Consome o ponto e vírgula
      self.f_declaracao_de_subprograma()
      self.f_declaracoes_de_subprogramas_linha()
    else:
      # ε - Não faz nada, pois é uma produção vazia
      pass
  
  def f_lista_de_identificadores(self):
    """Analisa uma lista de identificadores na gramática."""
    print("Estou consumindo a lista de identificadores!")
    if self.tipo_atual() == 'Identificador':
        self.consumir('Identificador')  # Consome o primeiro identificador
        self.f_lista_de_identificadores_linha()  # Chama o método para analisar o restante da lista de identificadores
    else:
        self.mensagem_token(f"Esperava um identificador, mas foi encontrado {self.token_atual()}")
        escrever_erro_sintatico(self.tokens[self.posicao])
        exit()  # Encerra o programa em caso de erro grave

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
      print("Verificando o tipo das variaveis declaradas!")
      self.f_tipo()  # Analisa o tipo das variáveis
      print("Consumi o tipo, vou pra próxima!")
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