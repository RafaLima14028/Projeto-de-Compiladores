#  Implementado por descida recursiva
from lexico import getToken, abre_arquivo

FIRST_DAS_TRANSICOES = {
    'call': ['program'],
    'bloco': ['abre_bloco'],
    'variaveis': ['int', 'float', 'char'],
    'variaveis_linha': ['int', 'float', 'char', 'vazio'],
    'variavel': ['int', 'float', 'char'],
    'lista_ids': ['id'],
    'lista_ids_linha': [',', 'vazio'],
    'comandos': ['id', 'if', 'while', 'repeat'],
    'comandos_linha': ['id', 'if', 'while', 'repeat', 'vazio'],
    'comando': ['id', 'if', 'while', 'repeat'],
    'comando_bloco': ['id', 'if', 'while', 'repeat', '{'],
    'comando_bloco_linha': ['else', 'vazio'],
    'cond': ['id', 'numero', 'caractere', '(', 'unario'],
    'expre': ['id', 'numero', 'caractere', '(', 'unario'],
    'expre_linha': ['+', '-', 'op', 'vazio'],
    'expre2': ['id', 'numero', 'caractere', '(', 'unario'],
    'expre2_linha': ['*', '/', 'op', 'vazio'],
    'expre3': ['+', '-', 'id', 'numero', 'caractere', '('],
    'expre3_linha': ['exp', 'vazio'],
    'unario': ['+', '-', 'id', 'numero', 'caractere', '('],
    'term': ['id', 'numero', 'caractere', '('],
    'op': ['oprel', 'atribuicao'],
    'string': ['caractere', 'vazio'],
    'string_linha': ['caractere', 'vazio'],
    'coment': ['abre_comentario']
}

if __name__ == '__main__':
    prox_token = getToken()
