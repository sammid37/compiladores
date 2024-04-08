# Constantes para Compilador Pascal 
# Utilitário para os analisadores Léxico, Sintático e Semântico
# Enthony e Samantha

OP_ADITIVO = ['+','-','or']
OP_MULTIPLICATIVO = ['*','/','and']
OP_RELACIONAL = ['=','<','>','<=','>=','<>']
SINAL = ['+','-']
TIPO = ['integer','real','boolean']
ATRIBUICAO = [':=']
DELIMITER = [';', '.', ':', '(', ')', ',']
BOOLEAN_VALUES = ['true', 'false']
NUMERICOS = ['Número inteiro', 'Número real']
PALAVRAS_RESERVADAS = ['program', 'var', 'integer', 'real', 'boolean', 'procedure', 'begin','end', 'if', 'then', 'else', 'while', 'do', 'not']

# Classificações
# TODO: utilizar essas constantes no sintático
PALAVRA_RESERVADA = 'Palavra reservada'
INTEIRO = 'integer'
IDENTIFICADOR = 'Identificador'
OPM = 'Operador multiplicativo'
OPA = 'Operador aditivo'
OPR = 'Operador relacional'
NINT = 'Número inteiro'
NREAL = 'Número real'