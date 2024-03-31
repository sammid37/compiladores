# Construção de Compiladores
# Analisador Sintático
# Enthony e Samantha

from constantes import *
from termcolor import colored
from collections import deque
       
# Definição de um Analisador Sintático
class Sintatico:
  def __init__(self, tokens):
    self.tokens = tokens # a lista de tokens (formado por uma tupla << value, type, line >>)
    self.posicao = 0 # posição do token na lista de tuplas
    self.count_begin = 0 # indicador para pares begin e end
    self.input_file = None
    self.output_syntax = None

    # pilhas e listas aux para a análise semântica
    self.tokenBuffer = [] # auxiliar para preencher a pilha IdsTipados
    self.idsTipados = deque() # tupla <id, tipo>
    self.pilhaIdentificadores = [] # String (id)
    self.pilhaControleTipo = deque() # String (tipo)

  def token_atual(self):
    return self.tokens[self.posicao].value;

  def tipo_atual(self):
    return self.tokens[self.posicao].type;

  def avancar(self):
    self.posicao += 1

  def verificar(self, tipo):
    return self.tipo_atual() == tipo

  def consumir(self, tipo):
    """Método responsável por consumir o tipo de um token, verificando o tipo esperado"""
    if self.verificar(tipo): 
      self.avancar()

  def analisar(self):
    """Realiza a análise sintática de um programa"""
    if self.token_atual() == 'program':
      self.pilhaIdentificadores.append('$')
      self.idsTipados.append(('$', 'mark'))
      self.consumir('Palavra reservada')
      if self.tipo_atual() == 'Identificador':
        self.pilhaIdentificadores.append(self.token_atual()) 
        self.consumir(self.tipo_atual())
        if self.token_atual() == ';':
          self.consumir(self.tipo_atual())
          self.f_declaracoes_variaveis()
          self.f_declaracoes_de_subprogramas() 
          self.f_comando_composto()
          if self.token_atual() == '.':
            print(colored("✅ Análise sintática concluída com sucesso.", 'green'))
          else:
            print(colored(f"\tEsperava o delimitador '.', mas foi encontrado {self.token_atual()}","red"))
            exit()
        else:
          print(colored(f"Esperava o delimitador ';', mas foi encontrado {self.token_atual()}", "red"))
          exit()
      else: 
        print(colored(f"Esperava um identificador, mas foi encontrado {self.token_atual()}","red"))
        exit()
    else:
      print(colored(f"Esperava a palavra reservada 'program', mas foi encontrado {self.token_atual()}","red"))
      exit()

  def f_op_aditivo(self):
    if self.self.token_atual() in OP_ADITIVO:
      self.consumir(self.tipo_atual())
    else:
      print(colored(f"Esperava algum operador aditivo, mas foi encontrado {self.token_atual()}","red"))  
      exit() 

  def f_op_multiplicativo(self):  
    if self.token_atual() in OP_MULTIPLICATIVO:
      self.consumir(self.tipo_atual())
    else:
      print(colored(f"Esperava algum operador multiplicativo, mas foi encontrado {self.token_atual()}","red"))
      exit()
      
  def f_op_relacional(self):
    if self.token_atual() in OP_RELACIONAL:
      self.consumir(self.tipo_atual())
    else:
      print(colored(f"Esperava algum operador relacional, mas foi encontrado {self.token_atual()}","red"))
      exit()  

  def f_sinal(self):
    if self.token_atual() in SINAL:
      self.consumir(self.tipo_atual())
    else:
      print(colored(f"Esperava algum sinal, mas foi encontrado {self.token_atual()}","red"))
      exit()
    
  def f_tipo(self):
    if self.token_atual() in TIPO:
      self.consumir(self.tipo_atual())
    else:
      print(colored(f"Esperava algum tipo tipo de variável, mas foi encontrado {self.token_atual()}","red"))
      exit()

  def f_fator(self):
    if self.tipo_atual() == 'Identificador':
      if self.token_atual() == '(':
        self.f_id_com_argumentos()
      else:
        self.consumir('Identificador')
    elif self.tipo_atual() == 'Número inteiro' or self.tipo_atual() == 'Número real' or self.tipo_atual() in BOOLEAN_VALUES:
      self.consumir(self.tipo_atual())
    elif self.token_atual() == '(':
      self.consumir('Delimitador')
      self.f_expressao()
      if self.token_atual() == ')':
        self.consumir('Delimitador')
      else:
        print(colored(f"Esperava o delimitador ')', mas foi encontrado {self.token_atual()}","red"))  
        exit()     
    elif self.token_atual() == 'not':
      self.consumir('Palavra Reservada')
      self.f_fator()
    else:
      print(colored(f"Esperava um fator, mas foi encontrado {self.token_atual()}","red"))   
      exit()
        
  def f_id_com_argumentos(self):
    self.consumir('Identificador')
    if self.token_atual() == '(':
      self.consumir('Delimitador')
      self.f_lista_de_expressao()
      if self.token_atual() == ')':
        self.consumir('Delimitador')
      else:
        print(colored(f"Esperava o delimitador ')', mas foi encontrado {self.token_atual()}","red"))   
        exit()       
    else:
      print(colored(f"Esperava o delimitador '(', mas foi encontrado {self.token_atual()}","red"))
      exit()            
  
  def f_expressao_simples(self):
    if self.token_atual() in SINAL:
      self.consumir(self.tipo_atual())
      self.f_termo()
      self.f_expressao_simples_linha() # Chama o método recursivamente
    else:
      self.f_termo()
      self.f_expressao_simples_linha() # Chama o método recursivamente
 
  def f_expressao_simples_linha(self):
    if self.token_atual() in OP_ADITIVO:
      self.consumir(self.tipo_atual())
      self.f_termo()
      self.f_expressao_simples_linha() # Chama o método recursivamente

  def f_expressao(self):
    self.f_expressao_simples() 
    self.f_expressao_linha() # Chama o método recursivamente
 
  def f_expressao_linha(self):
    if self.token_atual() in OP_RELACIONAL: 
      self.consumir(self.tipo_atual()) 
      self.f_expressao_simples() # Chama o método recursivamente
 
  def f_lista_de_expressao(self):
    self.f_expressao()  # Analisa a primeira expressão da lista
    while self.token_atual() == ',':
      self.consumir('Delimitador')  
      self.f_expressao()  

  def f_termo(self):
    self.f_fator() 
    self.f_termo_linha() # Chama o método recursivamente
    
  def f_termo_linha(self):
    if self.token_atual() in OP_MULTIPLICATIVO:
      self.consumir('Operador multiplicativo')  
      self.f_fator()
      self.f_termo_linha() # Chama o método recursivamente
      
  def f_ativacao_procedimento(self):
    if self.tipo_atual() == 'Identificador':
      self.consumir('Identificador')  # Consome o identificador do procedimento
      self.f_ativacao_procedimento_linha() # Chama o método recursivamente
    else:
      print(colored(f"Esperava um identificador, mas foi encontrado {self.token_atual()}","red"))    
      exit()     
  
  def f_ativacao_procedimento_linha(self):
    if self.token_atual() == '(':
      self.consumir('Delimitador')  
      self.f_lista_de_expressoes()  
      if self.token_atual() == ')':
        self.consumir('Delimitador')
      else:
        print(colored(f"Esperava o delimitador ')', mas foi encontrado {self.token_atual()}","red"))
        exit()   
                  
  def f_comando(self): 
    """Analisa possibilidades de comando, como atribuição, ativações de procedimentos e outros"""
    if self.tipo_atual() == 'Identificador' and self.tokens[self.posicao + 1].type == 'Atribuição':
      self.f_variavel();
      if self.tipo_atual() == 'Atribuição':
        self.consumir('Atribuição')
        self.f_expressao()
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
        print(colored(f"Esperava um a palavra reservada then, mas foi encontrado {self.token_atual()}","red"))
        exit()     
    elif self.token_atual() == 'while':
      self.consumir('Palavra reservada')
      self.f_expressao()
      if self.token_atual() == 'do':
        self.consumir('Palavra reservada')
        self.f_comando_composto()
      else: 
        print(colored(f"Esperava um a palavra reservada do, mas foi encontrado {self.token_atual()}","red"))
        exit()   
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
            print(colored(f"Esperava um a palavra reservada do, mas foi encontrado {self.token_atual()}","red"))
            exit()   
        else:
          print(colored(f"Esperava um a palavra reservada to, mas foi encontrado {self.token_atual()}","red"))
          exit()   
      else:
        print(colored(f"Esperava símbolo de atribuição :=, mas foi encontrado {self.token_atual()}","red"))
        exit()   
    else:
      print(colored(f"Comando inválido. Recebido: {self.token_atual()} de tipo '{self.tipo_atual()}'.", "red"))
      exit()
  
  def f_lista_comandos(self): 
    self.f_comando()
    self.f_lista_comandos_linha() # Chama o método recursivamente
  
  def f_lista_comandos_linha(self):
    """Verifica se ao final de um comando há um delimitador ';' e se há mais comandos em linha"""
    if self.token_atual() == ';':
      self.consumir('Delimitador')
      self.f_comando()
      self.f_lista_comandos_linha() # Chama o método recursivamente

  def f_comandos_opcionais(self):
    while self.token_atual() in ['begin', 'if', 'while', 'for'] or self.tipo_atual() == 'Identificador':
      self.f_lista_comandos()
        
  def f_comando_composto(self):
    if self.token_atual() == 'begin':
      self.consumir('Palavra reservada')
      self.f_comandos_opcionais()
      if(self.token_atual() != 'end'):
        print(colored(f"Esperava a palavra reservada end, mas foi encontrado {self.token_atual()}","red"))
        exit()
      else:
        self.consumir('Palavra reservada')
    else: 
      print(colored(f"Esperava a palavra reservada begin, mas foi encontrado {self.token_atual()}","red"))
      exit()
     
  def f_variavel(self):
    """Analisa uma variável na gramática."""
    if self.tipo_atual() == 'Identificador':
      self.consumir('Identificador') 
    else:
      print(colored(f"Esperava um identificador, mas foi encontrado {self.token_atual()}","red"))
      exit()
      
  def f_lista_de_parametros(self):
    """Analisa uma lista de parâmetros na gramática."""
    self.f_lista_de_identificadores() 

    if self.token_atual() == ':':
      self.consumir('Delimitador')  
      self.f_tipo()  
      self.f_lista_de_parametros_linha()  # Chama o método recursivamente 
    else: 
      print(colored(f"Esperava um delimitador ':', mas foi encontrado {self.token_atual()}","red"))
      exit()
      
  def f_lista_de_parametros_linha(self):
    """Analisa uma linha de parâmetros na gramática."""
    if self.token_atual() == ';':
      self.consumir('Delimitador')  
      self.f_lista_de_identificadores() 
      if self.token_atual() == ':':
        self.consumir('Delimitador') 
        self.f_tipo()  
        self.f_lista_de_parametros_linha()  # Chama o método recursivamente 
    if self.token_atual() == ',':
      self.consumir('Delimitador') 
      self.f_lista_de_identificadores() 
      if self.token_atual() == ':':
        self.consumir('Delimitador')  
        self.f_tipo()  
        self.f_lista_de_parametros_linha() # Chama o método recursivamente

  def f_argumentos(self):
    """Analisa os argumentos na gramática."""
    if self.token_atual() == '(':
      self.consumir('Delimitador') 
      self.f_lista_de_parametros()
      if self.token_atual() == ')':
        self.consumir('Delimitador') 
      else:
        print(colored(f"Esperava um delimitador ')', mas foi encontrado {self.token_atual()}","red"))
        exit()
        
  def f_declaracao_de_subprograma(self):
    """Analisa uma declaração de subprograma na gramática."""
    if self.token_atual() == 'procedure':
      self.consumir('Palavra reservada') 
      self.f_id()
      self.f_argumentos()
      if self.token_atual() == ';':
        self.consumir('Delimitador')
        self.f_declaracoes_variaveis()
        self.f_declaracoes_de_subprogramas()
        self.f_comando_composto()
      else:
        print(colored(f"Esperava o delimitador ';', mas foi encontrado {self.token_atual()}","red"))  
    else:
      print(colored(f"Esperava a palavra reservada 'procedure', mas foi encontrado {self.token_atual()}","red"))
      exit()
        
  def f_declaracoes_de_subprogramas(self):
    """Analisa declarações de subprogramas na gramática."""
    if self.token_atual() == 'procedure':
      self.f_declaracao_de_subprograma()
      if self.token_atual() == ';':
        self.consumir('Delimitador') 
        self.f_declaracoes_de_subprogramas()
      else: 
        print(colored(f"Esperava o delimitador ';', mas foi encontrado {self.token_atual()}","red"))
        exit()
           
  def f_lista_de_identificadores(self):
    """Analisa uma lista de identificadores na gramática."""
    if self.tipo_atual() == 'Identificador':
      self.consumir('Identificador')  # Consome o primeiro identificador
      self.f_lista_de_identificadores_linha()  # Chama o método recursivamente 
    else:
      print(colored(f"Esperava um identificador, mas foi encontrado {self.token_atual()}","red"))
      exit()
      
  def f_lista_de_identificadores_linha(self):
    """Analisa o restante da lista de identificadores na gramática ou vazio caso não haja mais identificadores após a vírgula."""
    if self.token_atual() == ',':
      self.consumir('Delimitador')
      if self.tipo_atual() == 'Identificador':
        self.consumir('Identificador')
        self.f_lista_de_identificadores_linha() # Chama o método recursivamente 
      else:
        print(colored(f"Esperava um identificador após a vírgula, mas foi encontrado {self.token_atual()}","red"))
        exit()
        
  def f_lista_declaracoes_variaveis(self):
    self.f_lista_de_identificadores() 
    if self.token_atual() == ':':
      self.consumir('Delimitador')  
      self.f_tipo() 
      self.f_lista_declaracoes_variaveis_linha() # Chama o método recursivamente

  def f_lista_declaracoes_variaveis_linha(self):
    if self.token_atual() == ';':
      self.consumir('Delimitador') 
      self.f_lista_de_identificadores()
      if self.token_atual() == ':':
        self.consumir('Delimitador')
        self.f_tipo()
        self.f_lista_declaracoes_variaveis_linha()  # Chama o método recursivamente
    else:
      print(colored(f"Esperava um delimitador ';', mas foi encontrado {self.token_atual()}","red"))
      exit()

  # TODO: correções em declarações de variáveis, de forma que f_tipo() retorne uma string correspondente ao tipo da variável declarada (e que possivelmente será utilizada em outras partes da análise sintática e semântica)
  def f_declaracoes_variaveis(self):
    if self.token_atual() == 'var':
      self.consumir('Palavra reservada')
      self.f_lista_de_identificadores()
      if self.token_atual() == ':':
        self.consumir('Delimitador')
        self.f_tipo()
        if self.token_atual() == ';':
          self.consumir('Delimitador')
          self.f_declaracoes_variaveis() # Chama o método recursivamente
  
  def f_parte_else(self):
    if self.token_atual() == 'else':
      self.consumir(self.tipo_atual())
      self.f_comando()