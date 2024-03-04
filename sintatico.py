# Construção de Compiladores
# Analisador Sintático
# Enthony e Samantha

from tokens import Token

from constantes import *
from termcolor import colored
       
# Definição de um Analisador Sintático
class Sintatico:
  def __init__(self, tokens):
    self.tokens = tokens # a lista de tokens (formado por uma tupla << value, type, line >>)
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

  def avancar(self):
    """Avança para a próxima posição que possa conter um token"""
    self.posicao += 1

  def verificar(self, tipo):
    """Retorna se o tipo do token atual corresponde ao tipo esperado"""
    return self.tipo_atual() == tipo

  def consumir(self, tipo):
    """Método responsável por consumir o tipo de um token, verificando o tipo esperado"""
    if self.verificar(tipo): 
      self.avancar()
    else:
      self.tokens[self.posicao].erro_sintatico = f"esperado {tipo}, encontrado {self.tipo_atual()}"
    
  def analisar(self):
    """Realiza a análise sintática de um programa"""
    self.programa()
    print(colored("✅ Análise sintática concluída com sucesso.", 'green'))

  def programa(self):
    """Contém regras (e subregras) de um programa em Pascal"""
    self.f_program()
    self.f_id() 
    self.f_delimiter_program()
    self.f_declaracoes_variaveis()
    self.f_declaracoes_de_subprogramas() 
    self.f_comando_composto()
  
  def f_program(self): 
    if self.token_atual() == 'program':
      self.consumir('Palavra reservada')
    else: 
      self.mensagem_token(f"Esperava a palavra reservada 'program', mas foi encontrado {self.token_atual()}")
      self.escrever_erro_sintatico(self.tokens[self.posicao])

  def f_id(self): 
    if(self.tipo_atual()) == 'Identificador':
      self.consumir(self.tipo_atual())
    else: 
      self.mensagem_token(f"Esperava um identificador, mas foi encontrado {self.token_atual()}")
      self.escrever_erro_sintatico(self.tokens[self.posicao])

  def f_delimiter_program(self): 
    if self.token_atual() in DELIMITER and self.token_atual() == ';':
      self.consumir(self.tipo_atual())
    else:
      self.mensagem_token(f"Esperava o delimitador ';', mas foi encontrado {self.token_atual()}")
      self.escrever_erro_sintatico(self.tokens[self.posicao])

  def f_delimiter(self): 
    if self.token_atual() in DELIMITER:
      self.consumir(self.tipo_atual())
    else:
      self.mensagem_token(f"Esperava algum delimitado, mas foi encontrado {self.token_atual()}")
      self.escrever_erro_sintatico(self.tokens[self.posicao])

  def f_op_aditivo(self):
    if self.self.token_atual() in OP_ADITIVO:
      self.consumir(self.tipo_atual())
    else:
      self.mensagem_token(f"Esperava algum operador aditivo, mas foi encontrado {self.token_atual()}")
      self.escrever_erro_sintatico(self.tokens[self.posicao])

  def f_op_multiplicativo(self):  
    if self.token_atual() in OP_MULTIPLICATIVO:
      self.consumir(self.tipo_atual())
    else:
      self.mensagem_token(f"Esperava algum operador multiplicativo, mas foi encontrado {self.token_atual()}")
      self.escrever_erro_sintatico(self.tokens[self.posicao])

  def f_op_relacional(self):
    if self.token_atual() in OP_RELACIONAL:
      self.consumir(self.tipo_atual())
    else:
      self.mensagem_token(f"Esperava algum operador relacional, mas foi encontrado {self.token_atual()}")
      self.escrever_erro_sintatico(self.tokens[self.posicao])

  def f_sinal(self):
    if self.token_atual() in SINAL:
      self.consumir(self.tipo_atual())
    else:
      self.mensagem_token(f"Esperava algum sinal, mas foi encontrado {self.token_atual()}")
      self.escrever_erro_sintatico(self.tokens[self.posicao])
    
  def f_tipo(self):
    if self.token_atual() in TIPO:
      self.consumir(self.tipo_atual())
    else:
      self.mensagem_token(f"Esperava algum tipo tipo de variável, mas foi encontrado {self.token_atual()}")
      self.escrever_erro_sintatico(self.tokens[self.posicao])

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
        self.mensagem_token(f"Esperava o delimitador ')', mas foi encontrado {self.token_atual()}")
        self.escrever_erro_sintatico(self.tokens[self.posicao]) 
    elif self.token_atual() == 'not':
      self.consumir('Palavra Reservada')
      self.f_fator()
    else:
      self.mensagem_token(f"Esperava um fator, mas foi encontrado {self.token_atual()}")
      self.escrever_erro_sintatico(self.tokens[self.posicao])
        
  def f_id_com_argumentos(self):
    self.consumir('Identificador')
    if self.token_atual() == '(':
      self.consumir('Delimitador')
      self.f_lista_de_expressao()
      if self.token_atual() == ')':
        self.consumir('Delimitador')
      else:
        self.mensagem_token(f"Esperava o delimitador ')', mas foi encontrado {self.token_atual()}")
        self.escrever_erro_sintatico(self.tokens[self.posicao])
    else:
      self.mensagem_token(f"Esperava o delimitador '(', mas foi encontrado {self.token_atual()}")
      self.escrever_erro_sintatico(self.tokens[self.posicao])   
  
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
      self.mensagem_token(f"Esperava um identificador, mas foi encontrado {self.token_atual()}")
      self.escrever_erro_sintatico(self.tokens[self.posicao])
  
  def f_ativacao_procedimento_linha(self):
    if self.token_atual() == '(':
      self.consumir('Delimitador')  
      self.f_lista_de_expressoes()  
      if self.token_atual() == ')':
        self.consumir('Delimitador')
      else:
        self.mensagem_token(f"Esperava o delimitador ')', mas foi encontrado {self.token_atual()}")
        self.escrever_erro_sintatico(self.tokens[self.posicao])          
  
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
        self.mensagem_token(f"Esperava um a palavra reservada then, mas foi encontrado {self.token_atual()}")
        self.escrever_erro_sintatico(self.tokens[self.posicao])
    elif self.token_atual() == 'while':
      self.consumir('Palavra reservada')
      self.f_expressao()
      if self.token_atual() == 'do':
        self.consumir('Palavra reservada')
        self.f_comando_composto()
      else: 
        self.mensagem_token(f"Esperava um a palavra reservada do, mas foi encontrado {self.token_atual()}")
        self.escrever_erro_sintatico(self.tokens[self.posicao])
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
            self.escrever_erro_sintatico(self.tokens[self.posicao])
        else:
          self.mensagem_token(f"Esperava um a palavra reservada to, mas foi encontrado {self.token_atual()}")
          self.escrever_erro_sintatico(self.tokens[self.posicao])
      else:
        self.mensagem_token(f"Esperava símbolo de atribuição :=, mas foi encontrado {self.token_atual()}")
        self.escrever_erro_sintatico(self.tokens[self.posicao])
    else:
      if self.token_atual() == 'end' and self.tokens[self.posicao + 1].value == '.':
        return "Comando avaliado com sucesso"
      # * Ainda com erro!
      # self.mensagem_token(f"Comando inválido. Recebido: {self.token_atual()} de tipo '{self.tipo_atual()}'.")
      # self.escrever_erro_sintatico(self.tokens[self.posicao])
  
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
      # GAMBIARRA
      if (self.token_atual() == 'end' and self.tokens[self.posicao -1].value == ';') or self.tokens[self.posicao -1].value == 'end':
        break # Se chegar o end do bloco, não tentará processar mais nada
      else: 
        self.mensagem_token("Esperava um delimitador ';' antes do end.")
        self.escrever_erro_sintatico(self.tokens[self.posicao])

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
          self.escrever_erro_sintatico(self.tokens[self.posicao]) 
    else: 
      self.mensagem_token(f"Esperava a palavra reservada begin, mas foi encontrado {self.token_atual()}")
      self.escrever_erro_sintatico(self.tokens[self.posicao])
     
  def f_variavel(self):
    """Analisa uma variável na gramática."""
    if self.tipo_atual() == 'Identificador':
      self.consumir('Identificador') 
    else:
      self.mensagem_token(f"Esperava um identificador, mas foi encontrado {self.token_atual()}")
      self.escrever_erro_sintatico(self.tokens[self.posicao])
     
  def f_lista_de_parametros(self):
    """Analisa uma lista de parâmetros na gramática."""
    self.f_lista_de_identificadores() 

    if self.token_atual() == ':':
      self.consumir('Delimitador')  
      self.f_tipo()  
      self.f_lista_de_parametros_linha()  # Chama o método recursivamente 
    else: 
      self.mensagem_token(f"Esperava um delimitador ':', mas foi encontrado {self.token_atual()}")
      self.escrever_erro_sintatico(self.tokens[self.posicao])

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
        self.mensagem_token(f"Esperava um delimitador ')', mas foi encontrado {self.token_atual()}")
        self.escrever_erro_sintatico(self.tokens[self.posicao])

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
        self.mensagem_token(f"Esperava o delimitador ';', mas foi encontrado {self.token_atual()}")
        self.escrever_erro_sintatico(self.tokens[self.posicao])
    else:
      self.mensagem_token(f"Esperava a palavra reservada 'procedure', mas foi encontrado {self.token_atual()}")
      self.escrever_erro_sintatico(self.tokens[self.posicao])
     
  def f_declaracoes_de_subprogramas(self):
    """Analisa declarações de subprogramas na gramática."""
    if self.token_atual() == 'procedure':
      self.f_declaracao_de_subprograma()
      if self.token_atual() == ';':
        self.consumir('Delimitador') 
        self.f_declaracoes_de_subprogramas()
      else: 
        self.mensagem_token(f"Esperava o delimitador ';', mas foi encontrado {self.token_atual()}")
        self.escrever_erro_sintatico(self.tokens[self.posicao])
       
  def f_lista_de_identificadores(self):
    """Analisa uma lista de identificadores na gramática."""
    if self.tipo_atual() == 'Identificador':
      self.consumir('Identificador')  # Consome o primeiro identificador
      self.f_lista_de_identificadores_linha()  # Chama o método recursivamente 
    else:
      self.mensagem_token(f"Esperava um identificador, mas foi encontrado {self.token_atual()}")
      self.escrever_erro_sintatico(self.tokens[self.posicao])

  def f_lista_de_identificadores_linha(self):
    """Analisa o restante da lista de identificadores na gramática ou vazio caso não haja mais identificadores após a vírgula."""
    if self.token_atual() == ',':
      self.consumir('Delimitador')
      if self.tipo_atual() == 'Identificador':
        self.consumir('Identificador')
        self.f_lista_de_identificadores_linha() # Chama o método recursivamente 
      else:
        self.mensagem_token(f"Esperava um identificador após a vírgula, mas foi encontrado {self.token_atual()}")
        self.escrever_erro_sintatico(self.tokens[self.posicao])
 
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
      self.mensagem_token(f"Esperava um delimitador ';', mas foi encontrado {self.token_atual()}")
      self.escrever_erro_sintatico(self.tokens[self.posicao])

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
          self.f_declaracoes_variaveis() # Chama o método recursivamente
  
  def f_parte_else(self):
    if self.token_atual() == 'else':
      self.consumir(self.tipo_atual())
      self.f_comando()

# Escreve o arquivo de saída do analisador sintático
  def escrever_erro_sintatico(self, token):
    """Escreve o arquivo de saída do analisador sintático e encerra a execução do sintático"""
    # Abre o arquivo de saída em modo de escrita
    with open(self.output_syntax, "a") as arquivo_saida:
      # Escreve a mensagem de erro no arquivo
      arquivo_saida.write(f"Erro sintático na linha {token.line}: '{token.erro_sintatico}'\n")
    print(colored("🟥 Erro sintático encontrado. Verifique o arquivo gerado.",'red'))
    exit()