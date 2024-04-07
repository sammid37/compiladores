# Construção de Compiladores
# Analisador Léxico implementado com AFD
# Enthony e Samantha

# FIXME: precisa de ajustes para operar como a versão feita com regex!

import csv

class ComentarioNaoFechadoErro(Exception):
    def __init__(self, linha, posicao):
        self.linha = linha
        super().__init__(f"Comentario aberto e nao fechado encontrado na linha {linha}.")

class AnalisadorLexico:
    def __init__(self):
        self.tabela_simbolos = []
        self.estado = 0
        self.buffer = ''
        self.comentario_aberto = False
        self.numero_da_linha = 0  

    def adicionar_a_tabela_de_simbolos(self, token, tipo_do_token):
        self.tabela_simbolos.append({'Token': token, 'Tipo do Token': tipo_do_token, 'Linha': self.numero_da_linha})

    def analisar_codigo(self, codigo):
        linhas = codigo.split('\n')
        for linha in linhas:  # Processa todas as linhas
            self.numero_da_linha += 1  # Incremento do contador de linha
            self.analisar_linha(linha)

        # Verifica se há um comentário aberto no final do arquivo
        if self.comentario_aberto:
            raise ComentarioNaoFechadoErro(self.numero_da_linha, len(codigo) + 1)

    def analisar_linha(self, linha):
        # Verifica se a linha contém apenas palavras-chave
        if linha.strip() and all(word.strip() in ['program', 'var', 'integer', 'real', 'boolean', 'procedure', 'begin', 'end', 'if', 'then', 'else', 'while', 'do', 'not', 'or', 'and'] for word in linha.split()):
            self.adicionar_a_tabela_de_simbolos(linha.strip(), 'Palavra-chave')
            return  # Não processa caracteres individuais se toda a linha é uma palavra-chave

        for posicao, char in enumerate(linha, start=1):
            self.processar_char(char, posicao)

        # Verifica se o comentário está aberto no final da linha
        if self.comentario_aberto:
            raise ComentarioNaoFechadoErro(self.numero_da_linha, len(linha) + 1)

    def processar_char(self, char, posicao):
        if char == '{':
            if self.comentario_aberto:
                raise ComentarioNaoFechadoErro(self.numero_da_linha, posicao)
            self.comentario_aberto = True
        elif char == '}':
            if not self.comentario_aberto:
                raise ComentarioNaoFechadoErro(self.numero_da_linha, posicao)
            self.comentario_aberto = False
        elif self.comentario_aberto:
            pass
        elif self.estado == 0:  # Estado inicial
            if char.isalpha() or char == '_':
                self.buffer += char
                self.estado = 1
            elif char.isdigit():
                self.buffer += char
                self.estado = 2
            elif char.isspace():
                pass
            elif char == ':':
                self.buffer += char
                self.estado = 5
            elif char == ';':
                self.adicionar_a_tabela_de_simbolos(char, 'Delimitador')
            elif char in ['.', '(', ')', ',']:
                self.adicionar_a_tabela_de_simbolos(char, 'Delimitador')
            elif char in ['+', '-']:
                self.adicionar_a_tabela_de_simbolos(char, 'Operador Aditivo')
            elif char in ['*', '/']:
                self.adicionar_a_tabela_de_simbolos(char, 'Operador Multiplicativo')
            elif char in ['<', '>']:
                self.buffer += char
                self.estado = 6
            elif char == '=':
                self.adicionar_a_tabela_de_simbolos(char, 'Operador Relacional')
            else:
                self.adicionar_a_tabela_de_simbolos(char, 'Erro - Símbolo não pertencente à linguagem')

        elif self.estado == 1:  # Identificador ou Palavra-chave
            if char.isalnum() or char == '_':
                self.buffer += char
            else:
                self.adicionar_identificador_ou_palavra_chave()
                self.processar_char(char, posicao)
        elif self.estado == 2:  # Número Inteiro
            if char.isdigit():
                self.buffer += char
            elif char == '.':
                self.buffer += char
                self.estado = 3
            elif char.isalpha() or char == '_':
                self.adicionar_a_tabela_de_simbolos(self.buffer, 'Erro - Identificador inválido')
                self.reset_buffer_and_estado()
                self.processar_char(char, posicao)
            else:
                self.adicionar_a_tabela_de_simbolos(self.buffer, 'Numero Inteiro')
                self.reset_buffer_and_estado()
                self.processar_char(char, posicao)

        elif self.estado == 3:  # Parte Decimal de Número Real
            if char.isdigit():
                self.buffer += char
                self.estado = 4
            else:
                self.adicionar_a_tabela_de_simbolos(self.buffer, 'Erro - Numero Real inválido')
                self.reset_buffer_and_estado()
                self.processar_char(char, posicao)

        elif self.estado == 4:  # Número Real
            if char.isdigit():
                self.buffer += char
            elif char.isalpha() or char == '_':
                self.adicionar_a_tabela_de_simbolos(self.buffer, 'Erro - Identificador inválido')
                self.reset_buffer_and_estado()
                self.processar_char(char, posicao)
            else:
                self.adicionar_a_tabela_de_simbolos(self.buffer, 'Número Real')
                self.reset_buffer_and_estado()
                self.processar_char(char, posicao)

        elif self.estado == 5:  # Comando de atribuição :=
            if char == '=':
                self.buffer += char
                self.adicionar_a_tabela_de_simbolos(self.buffer, 'Atribuicao')
                self.reset_buffer_and_estado()
            else:
                self.adicionar_a_tabela_de_simbolos(self.buffer, 'Delimitador')
                self.reset_buffer_and_estado()
                self.processar_char(char, posicao)

        elif self.estado == 6:  # Operadores relacionais
            if char == '=' or char == '>':
                self.buffer += char
                self.adicionar_a_tabela_de_simbolos(self.buffer, 'Operador Relacional')
                self.reset_buffer_and_estado()
            elif char == '<':
                self.buffer += char
                self.estado = 7
            else:
                self.adicionar_a_tabela_de_simbolos(self.buffer, 'Erro - Símbolo não pertencente à linguagem')
                self.reset_buffer_and_estado()
                self.processar_char(char, posicao)

        elif self.estado == 7:  # Operador Relacional '<>'
            if char == '>':
                self.buffer += char
                self.adicionar_a_tabela_de_simbolos(self.buffer, 'Operador Relacional')
                self.reset_buffer_and_estado()
            else:
                self.adicionar_a_tabela_de_simbolos(self.buffer, 'Erro - Símbolo não pertencente à linguagem')
                self.reset_buffer_and_estado()
                self.processar_char(char, posicao)

        elif self.estado == 8:  # Operador Relacional '<'
            if char == '=':
                self.buffer += char
                self.adicionar_a_tabela_de_simbolos(self.buffer, 'Operador Relacional')
                self.reset_buffer_and_estado()
            else:
                self.adicionar_a_tabela_de_simbolos(self.buffer, 'Erro - Símbolo não pertencente à linguagem')
                self.reset_buffer_and_estado()
                self.processar_char(char, posicao)

    def adicionar_identificador_ou_palavra_chave(self):
        if self.buffer.lower() in ['program', 'var', 'integer', 'real', 'boolean', 'procedure', 'begin', 'end', 'if', 'then', 'else', 'while', 'do', 'not', 'or', 'and']:
            self.adicionar_a_tabela_de_simbolos(self.buffer, 'Palavra reservada')
        else:
            self.adicionar_a_tabela_de_simbolos(self.buffer, 'Identificador')
        self.reset_buffer_and_estado()

    def reset_buffer_and_estado(self):
        self.buffer = ''
        self.estado = 0

    def salvar_em_csv(self, nome_do_arquivo='tabela_de_simbolos.csv'):
        with open(nome_do_arquivo, 'w', newline='') as csvfile:
            nomes_dos_campos = ['Token', 'Tipo do Token', 'Linha']
            escritor = csv.DictWriter(csvfile, fieldnames=nomes_dos_campos)

            escritor.writeheader()
            for entrada in self.tabela_simbolos:
                escritor.writerow(entrada)

# Leitura do arquivo de entrada
source_file = 'entrada.txt'

with open(source_file, 'r') as f:
    source_code = f.read()

# Exemplo de uso
analisador = AnalisadorLexico()
analisador.analisar_codigo(source_code)
analisador.salvar_em_csv()
