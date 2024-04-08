# Construção de Compiladores
# Analisador Sintático e análise Semântica
# Enthony e Samantha

from pilha import Pilha
from constantes import *
from termcolor import colored
from identificador_tipado import IdentificadorTipado     
class Sintatico:
  def __init__(self, tokens):
    self.tokens = tokens # a lista de tokens (formado por uma tupla << value, type, line >>)
    self.posicao = 0 # posição do token na lista de tuplas
    self.count_begin = 0 # indicador para pares begin e end
    self.input_file = None
    self.output_syntax = None

    # pilhas e listas aux para a análise semântica
    self.tokenBuffer = [] # auxiliar para preencher a pilha IdsTipados
    self.idsTipados = Pilha() # tupla <id, tipo>
    self.pilhaIdentificadores = Pilha() # String (id)
    self.pilhaControleTipo = Pilha() # String (tipo)

  def token_atual(self):
    return self.tokens[self.posicao].value

  def tipo_atual(self):
    return self.tokens[self.posicao].type

  def avancar(self):
    self.posicao += 1

  def verificar(self, tipo):
    return self.tipo_atual() == tipo

  def consumir(self, tipo):
    """Método responsável por consumir o tipo de um token, verificando o tipo esperado"""
    if self.tipo_atual() == tipo: 
      self.posicao += 1

  def analisar(self):
    """Realiza a análise sintática de um programa"""
    if self.token_atual() == 'program':
      self.pilhaIdentificadores.empilhar('$')
      self.idsTipados.empilhar(IdentificadorTipado('$', 'mark'))
      self.consumir('Palavra reservada')
      if self.tipo_atual() == 'Identificador':
        self.pilhaIdentificadores.empilhar(self.token_atual()) 
        self.consumir(self.tipo_atual())
        if self.token_atual() == ';':
          self.consumir(self.tipo_atual())
          self.f_declaracoes_variaveis()
          self.f_declaracoes_de_subprogramas() 
          self.f_comando_composto()
          if self.token_atual() == '.':
            return
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

  #* --------------------------------------------------- DEC VAR, LISTA ID E RECURSIVIDADE
  def f_declaracoes_variaveis(self):
    if self.token_atual() == 'var':
      self.consumir('Palavra reservada')
      self.f_lista_declaracoes_variaveis()
      self.f_declaracoes_variaveis()

  def f_lista_declaracoes_variaveis(self):
    """Obtém a lista de identificadores e o tipo, 
    em seguida empilha esses dados na pilha de IdsTipados"""
    
    self.f_lista_de_identificadores() 
    if self.token_atual() == ':':
      self.consumir('Delimitador')  
      tipo = self.f_tipo() 

      if self.token_atual() == ';':
        for identificador in self.tokenBuffer:
          self.idsTipados.empilhar(IdentificadorTipado(identificador, tipo))
        self.tokenBuffer = []  # Limpa o tokenBuffer
        self.consumir('Delimitador')
        self.f_lista_declaracoes_variaveis_linha() # Chama o método recursivamente
      else: 
        print(colored(f"Esperava um delimitador ';', mas foi encontrado {self.token_atual()}","red"))
        exit()   
    else:      
      print(colored(f"Esperava um delimitador ':', mas foi encontrado {self.token_atual()}","red"))
      exit()   

  def f_lista_declaracoes_variaveis_linha(self):
    """Obtém a lista de identificadores e o tipo, 
    em seguida empilha esses dados na pilha de IdsTipados"""
    if self.tipo_atual() == 'Identificador':
      self.f_lista_de_identificadores()
      if self.token_atual() == ':':
        self.consumir('Delimitador')
        tipo = self.f_tipo()  

        if self.token_atual() == ';':
          for identificador in self.tokenBuffer:
            self.idsTipados.empilhar(IdentificadorTipado(identificador, tipo))
          self.tokenBuffer = []  # Limpa o tokenBuffer
          self.consumir('Delimitador')
          self.f_lista_declaracoes_variaveis_linha()  # Chama o método recursivamente
        else: 
          print(colored(f"Esperava um delimitador ';', mas foi encontrado {self.token_atual()}","red"))
          exit()   
      else:      
        print(colored(f"Esperava um delimitador ':', mas foi encontrado {self.token_atual()}","red"))
        exit()   

  def f_lista_de_identificadores(self):
    """Analisa uma lista de identificadores na gramática e verifica
    se o identificador já foi declarado anteriormente."""
    if self.tipo_atual() == 'Identificador':
      declarou = False
      for identificador in self.pilhaIdentificadores:
        if identificador != "$":
          if identificador == self.token_atual():
            declarou = True
            break     
        else:
          break   
      if declarou:
        print(colored(f"O identificador '{self.token_atual()}' já foi declarado anteriormente.", "red"))
        exit()

      # Se o identificador não foi declarado anteriormente, 
      # adiciona-o à pilha de identificadores e consome o token atual
      self.pilhaIdentificadores.empilhar(self.token_atual())
      self.tokenBuffer.append(self.token_atual())
      self.consumir('Identificador')
      self.f_lista_de_identificadores_linha()  # Chama o método recursivamente
    else:
      print(colored(f"Esperava um identificador, mas foi encontrado {self.token_atual()}","red"))
      exit()
   
  def f_lista_de_identificadores_linha(self):
    """Analisa uma lista de identificadores na gramática e verifica
    se o identificador já foi declarado anteriormente."""
    if self.token_atual() == ',':
      self.consumir('Delimitador')
      if self.tipo_atual() == 'Identificador':
        declarou = False
        for identificador in self.pilhaIdentificadores:
          if identificador != "$":
            if identificador == self.token_atual():
              declarou = True
              break    
          else:
            break    
        if declarou:
          print(colored(f"O identificador '{self.token_atual()}' já foi declarado anteriormente.", "red"))
          exit()

        # Se o identificador não foi declarado anteriormente, 
        # adiciona-o à pilha de identificadores e consome o token atual
        self.pilhaIdentificadores.empilhar(self.token_atual())
        self.tokenBuffer.append(self.token_atual())
        self.consumir('Identificador')
        self.f_lista_de_identificadores_linha()  # Chama o método recursivamente
      else:
        print(colored(f"Esperava um identificador, mas foi encontrado {self.token_atual()}","red"))
        exit()

  def f_tipo(self):
    """Analisa o tipo de variável na gramática e retorna uma string correspondente."""
    if self.token_atual() in TIPO:
      tipo_variavel = self.token_atual()  # Salva o tipo atual
      self.consumir(self.tipo_atual())  # Consome o tipo
      return tipo_variavel  # Retorna o tipo como string
    else:
      print(colored(f"Esperava algum tipo de variável, mas foi encontrado {self.token_atual()}","red"))
      exit()

  #* --------------------------------------------------- DEC SUB PROG.
  def f_declaracoes_de_subprogramas(self):
    """Analisa declarações de subprogramas na gramática."""
    if self.token_atual() == 'procedure':
      self.f_declaracao_de_subprograma()
      if self.token_atual() == ';':
        # "Destrói" das pilhas as variáveis criadas após a finalização da subrotina
        for identificador in self.pilhaIdentificadores:
          if identificador != '$':
            self.pilhaIdentificadores.desempilhar()
          else: 
            self.pilhaIdentificadores.desempilhar()
            break
        for identificador in self.idsTipados:
          if identificador.identificador != '$':
            self.idsTipados.desempilhar()
          else: 
            self.idsTipados.desempilhar()
            break
        self.consumir('Delimitador') 
        self.f_declaracoes_de_subprogramas()
      else: 
        print(colored(f"Esperava o delimitador ';', mas foi encontrado {self.token_atual()}","red"))
        exit()

  def f_declaracao_de_subprograma(self):
    """Analisa uma declaração de subprograma na gramática.
    Verifica se o nome do subprograma não foi utilizado anteriormente."""
    if self.token_atual() == 'procedure':
      self.consumir('Palavra reservada') 
      if self.tipo_atual() == 'Identificador':
        declarou = False
        for identificador in self.pilhaIdentificadores:
          if(identificador != '$'):
           if(identificador == self.token_atual()):
            declarou = True
            break
          else: 
            break
        if declarou:
          print(colored(f"O identificador '{self.token_atual()}' já foi declarado anteriormente.", "red"))
          exit()
        else:
          self.pilhaIdentificadores.empilhar(self.token_atual())
          self.pilhaIdentificadores.empilhar('$') # novo escopo
          self.idsTipados.empilhar(IdentificadorTipado('$','mark')) # novo escopo
        self.consumir('Identificador')
        self.f_argumentos() # Verifica se o identificador está acompanhado de args
        if self.token_atual() == ';':
          self.consumir('Delimitador')
          self.f_declaracoes_variaveis()
          self.f_declaracoes_de_subprogramas()
          self.f_comando_composto()
        else:
          print(colored(f"Esperava o delimitador ';', mas foi encontrado {self.token_atual()}","red"))
          exit()
      else:
        print(colored(f"Esperava um identificador, mas foi encontrado {self.token_atual()}","red"))  
        exit()
    else:
      print(colored(f"Esperava a palavra reservada 'procedure', mas foi encontrado {self.token_atual()}","red"))
      exit()

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

  def f_lista_de_parametros(self):
    """Analisa uma lista de parâmetros na gramática."""
    self.f_lista_de_identificadores() 
    if self.token_atual() == ':':
      self.consumir('Delimitador')  
      tipo = self.f_tipo()  
      for identificador in self.tokenBuffer:
        self.idsTipados.empilhar(IdentificadorTipado(identificador, tipo))
      self.tokenBuffer = [] 
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
        tipo = self.f_tipo()  
        for identificador in self.tokenBuffer:
          self.idsTipados.empilhar(IdentificadorTipado(identificador, tipo))
        self.tokenBuffer = [] 
        self.f_lista_de_parametros_linha()  # Chama o método recursivamente 
      else: 
        print(colored(f"Esperava um delimitador ':', mas foi encontrado {self.token_atual()}","red"))
        exit()

#* --------------------------------------------------- CMD COMPOSTO, OP, CMD E ETC       
  def f_comando(self): 
    """Analisa possibilidades de comando, como atribuição, 
    ativações de procedimentos e outros"""
    if self.tipo_atual() == 'Identificador' and self.tokens[self.posicao + 1].type == 'Atribuição':
      self.f_variavel()
      if self.tipo_atual() == 'Atribuição':
        self.consumir('Atribuição')
        self.f_expressao()
      self.f_verificar_atribuicao()
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
        self.f_comando()
      else: 
        print(colored(f"Esperava um a palavra reservada do, mas foi encontrado {self.token_atual()}","red"))
        exit()   
    elif self.token_atual() == 'for':
      self.consumir('Palavra reservada')
      self.f_variavel()
      if self.tipo_atual() == 'Atribuição':
        self.consumir('Atribuição')
        self.f_expressao()
        self.f_verificar_atribuicao()
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

  def f_comandos_opcionais(self):
    while self.token_atual() in ['begin', 'if', 'while', 'for'] or self.tipo_atual() == 'Identificador':
      self.f_lista_comandos()

  def f_lista_comandos(self): 
    self.f_comando()
    self.f_lista_comandos_linha() # Chama o método recursivamente
  
  def f_lista_comandos_linha(self):
    """Verifica se ao final de um comando há um delimitador ';' e se há mais comandos em linha"""
    if self.token_atual() == ';':
      self.consumir('Delimitador')
      self.f_comando()
      self.f_lista_comandos_linha() # Chama o método recursivamente

  def f_parte_else(self):
    if self.token_atual() == 'else':
      self.consumir(self.tipo_atual())
      self.f_comando()

  #* ----------------------------------->>> Vars, sinais e operações
  def f_variavel(self):
    """Analisa uma variável na gramática."""
    if self.tipo_atual() == 'Identificador':
      if self.token_atual() not in self.pilhaIdentificadores:
        print(colored(f"O identificador {self.token_atual()} não foi declarado anteriormente.","red"))
        exit()
      # Se o identificador tiver sido declarado, ele obtem o tipo a partir da pilha idsTipados para incluir na pilha de controle
      for identificador in self.idsTipados:
        if identificador.identificador == self.token_atual():
          self.pilhaControleTipo.empilhar(identificador.tipo)
          break
      self.consumir('Identificador') 
    else:
      print(colored(f"Esperava uma variável, mas foi encontrado {self.token_atual()}","red"))
      exit()
  
  def f_op_aditivo(self):
    if self.token_atual() in OP_ADITIVO:
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

  #* ----------------------------------->>> Fator
  def f_fator(self):
    if self.tipo_atual() == 'Identificador':
      self.f_ativacao_procedimento()
    elif self.tipo_atual() == 'Número inteiro':
      self.consumir(self.tipo_atual())
      self.pilhaControleTipo.empilhar('integer')
    elif self.tipo_atual() == 'Número real':
      self.consumir(self.tipo_atual())
      self.pilhaControleTipo.empilhar('real')
    elif self.tipo_atual() in BOOLEAN_VALUES:
      self.consumir(self.tipo_atual())
      self.pilhaControleTipo.empilhar('boolean')
    elif self.token_atual() == '(':
      self.consumir('Delimitador')
      self.f_expressao()
      if self.token_atual() == ')':
        self.consumir('Delimitador')
      else:
        print(colored(f"Esperava o delimitador ')', mas foi encontrado {self.token_atual()}","red"))  
        exit()     
    elif self.token_atual() == 'not':
      self.pilhaControleTipo.empilhar('boolean')
      self.consumir('Palavra reservada')
      self.f_fator()
      self.f_verificar_logica()
    else:
      print(colored(f"Esperava um fator, mas foi encontrado {self.token_atual()}","red"))   
      exit()
          
  #* ----------------------------------->>> Expressão
  def f_expressao(self):
    self.f_expressao_simples() 
    self.f_expressao_linha() # Chama o método recursivamente
 
  def f_expressao_linha(self):
    if self.token_atual() in OP_RELACIONAL: 
      self.f_op_relacional()
      self.f_expressao_simples()
      self.f_expressao_linha() # Chama o método recursivamente
      self.f_verificar_relacional()
  
  def f_expressao_simples(self):
    if self.token_atual() in SINAL:
      self.consumir(self.tipo_atual())
      self.f_termo()
      self.f_expressao_simples_linha() # Chama o método recursivamente
    else:
      self.f_termo()
      self.f_expressao_simples_linha() # Chama o método recursivamente
 
  def f_expressao_simples_linha(self):
    if self.tipo_atual() == 'Operador aditivo':
      if self.token_atual() in SINAL:
        self.f_op_aditivo()
        self.f_termo()
        self.f_expressao_simples_linha() # Chama o método recursivamente
        self.f_verificar_aritmetica()
      #  verificar se é 'or'
      elif self.token_atual() == 'or':
        self.f_op_aditivo()
        self.f_termo()
        self.f_expressao_simples_linha()
        self.f_verificar_logica()

  def f_lista_de_expressao(self):
    self.f_expressao()  # Analisa a primeira expressão da lista
    while self.token_atual() == ',':
      self.consumir('Delimitador')  
      self.f_expressao()  

  #* ----------------------------------->>> Termo
  def f_termo(self):
    self.f_fator() 
    self.f_termo_linha() # Chama o método recursivamente
    
  def f_termo_linha(self):
    if self.tipo_atual() == 'Operador multiplicativo':
      if self.token_atual() == '*' or self.token_atual() == '/':
        self.f_op_multiplicativo()
        self.f_fator()
        self.f_termo_linha() # Chama o método recursivamente
        self.f_verificar_aritmetica()
      elif self.token_atual() == 'and':
        self.f_op_multiplicativo()
        self.f_fator()
        self.f_termo_linha() # Chama o método recursivamente
        self.f_verificar_logica()

  #* ----------------------------------->>> Ativação de Procedimento
  def f_ativacao_procedimento(self):
    if self.tipo_atual() == 'Identificador':
      if self.token_atual() not in self.pilhaIdentificadores:
        print(colored(f"O identificador {self.token_atual()} não foi declarado anteriormente.","red"))
        exit()
      # Se o identificador tiver sido declarado, ele obtem o tipo a partir da pilha idsTipados para incluir na pilha de controle
      for identificador in self.idsTipados:
        if identificador.identificador == self.token_atual():
          self.pilhaControleTipo.empilhar(identificador.tipo)
          break

      self.consumir('Identificador')  # Consome o identificador do procedimento
      self.f_ativacao_procedimento_linha() # Chama o método recursivamente
    else:
      print(colored(f"Esperava um identificador, mas foi encontrado {self.token_atual()}","red"))    
      exit()     
  
  def f_ativacao_procedimento_linha(self):
    if self.token_atual() == '(':
      self.consumir('Delimitador')  
      self.f_lista_de_expressao()  
      if self.token_atual() == ')':
        self.consumir('Delimitador')
      else:
        print(colored(f"Esperava o delimitador ')', mas foi encontrado {self.token_atual()}","red"))
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

  #* --------------------------------------------------- Métodos da Pilha Controle de Tipo
  def f_verificar_atribuicao(self):
    """Realiza a verificação de tipos para operações de atribuição."""
    top = self.pilhaControleTipo.desempilhar()

    if self.pilhaControleTipo.topo() == "real" and top == "integer":
      self.pilhaControleTipo.desempilhar()
    elif self.pilhaControleTipo.topo() == top:
      self.pilhaControleTipo.desempilhar()
    else:
      if self.token_atual() == "end":
        print(colored(f"Erro: tipos incompatíveis em operação de atribuição na linha {self.tokens[self.posicao - 1].line}", "red"))
      else:
        print(colored(f"Erro: tipos incompatíveis em operação de atribuição na linha {self.tokens[self.posicao].line}", "red"))
      exit()

  def f_verificar_logica(self):
    """Realiza a verificação de tipos para operações lógicas."""
    top = self.pilhaControleTipo.desempilhar()
    subtop = self.pilhaControleTipo.desempilhar()

    if top == subtop:
      self.pilhaControleTipo.empilhar("boolean")
    else:
      if self.token_atual() == "end":
        print(colored(f"Erro: tipos incompatíveis em operação lógica na linha {self.tokens[self.posicao - 1].line}", "red"))
      else:
        print(colored(f"Erro: tipos incompatíveis em operação lógica na linha {self.tokens[self.posicao].line}", "red"))
      exit()

  def f_verificar_relacional(self):
    """Realiza a verificação de tipos para operações relacionais."""
    top = self.pilhaControleTipo.desempilhar()
    subtop = self.pilhaControleTipo.desempilhar()

    if top == "integer" and subtop == "integer":
      self.pilhaControleTipo.empilhar("boolean")
    elif top == "real" and subtop == "real":
      self.pilhaControleTipo.empilhar("boolean")
    elif top == "integer" and subtop == "real":
      self.pilhaControleTipo.empilhar("boolean")
    elif top == "real" and subtop == "integer":
      self.pilhaControleTipo.empilhar("boolean")
    else:
        if self.token_atual() == "end":
          print(colored(f"Erro: tipos incompatíveis em operação relacional na linha {self.tokens[self.posicao - 1].linha}", "red"))
        else:
          print(colored(f"Erro: tipos incompatíveis em operação relacional na linha {self.tokens[self.posicao].linha}", "red"))
        exit()

  def f_verificar_aritmetica(self):
    """Realiza a verificação de tipos para operações aritméticas."""
    top = self.pilhaControleTipo.desempilhar()
    subtop = self.pilhaControleTipo.desempilhar()
    if top == "integer" and subtop == "integer":
      self.pilhaControleTipo.empilhar("integer")
    elif top == "real" and subtop == "real":
      self.pilhaControleTipo.empilhar("real")
    elif top == "integer" and subtop == "real":
      self.pilhaControleTipo.empilhar("real")
    elif top == "real" and subtop == "integer":
      self.pilhaControleTipo.empilhar("real")
    else:
      if self.token_atual() == "end":
        print(colored(f"Erro: tipos incompatíveis em operação aritmética na linha {self.tokens[self.posicao - 1].line}", "red"))
      else:
        print(colored(f"Erro: tipos incompatíveis em operação aritmética na linha {self.tokens[self.posicao].line}", "red"))
      exit()