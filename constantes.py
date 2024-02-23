# Constantes para Compilador Pascal 
# Utilitário para os analisadores Léxico, Sintático e Semântico
# Enthony Miguel e Samantha Dantas

OP_ADITIVO = ['+','-','or']
OP_MULTIPLICATIVO = ['*','/','and']
OP_RELACIONAL = ['=','<','>','<=','>=','<>']
SINAL = ['+','-']
TIPO = ['interger','real','boolean']
ATRIBUICAO = [':=']
DELIMITER = [';', '.', ':', '(', ')', ',']
BOOLEAN_VALUES = ['true', 'false']

# TODO: Fragmentar ou deixar inteiro?
PALAVRAS_RESERVADAS = ['program', 'var', 'integer', 'real', 'boolean', 'procedure', 'begin','end', 'if', 'then', 'else', 'while', 'do', 'not']