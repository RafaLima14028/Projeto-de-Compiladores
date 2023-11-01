#  Foi implementado dirigido por tabela usando diagrama de transição unificado
import re

import tabela_de_simbolos as tabela

arquivo = None
nome_id = ''
linha = 1
coluna = 1
linha_inicio_token = 0
coluna_inicio_token = 0
travar = False
tipo = ''


def abre_arquivo(caminho: str) -> None:
    global arquivo

    try:
        arquivo = open(caminho, "r")
    except FileNotFoundError:  # Arquivo não encontrado
        print(f'O arquivo {caminho} não foi encontrado.')
        raise
    except PermissionError:  # Não tem permissão para abri-lo
        print(f'Você não tem permissão para acessar esse arquivo')
        raise
    except IOError as e:  # Problemas de entrada/saida gerais
        print(f'Erro de E/S: {e}')
        raise
    except Exception as e:
        print(f'Erro desconecido: {e}')
        raise


def fecha_arquivo() -> None:
    global arquivo
    arquivo.close()
    arquivo = None


def lookhead() -> None:
    global coluna

    if coluna > 1:
        coluna -= 1

    arquivo.seek(arquivo.tell() - 1, 0)


def volta_token_anterior() -> None:
    global travar

    if travar is False:
        travar = True


def gera_erro_lexico(msg: str, linha: int, coluna: int) -> Exception:
    raise Exception(
        f'Ocorreu um erro na análise léxica: Na linha: {linha} e na coluna: {coluna}. {msg}.'
    )


def setInt() -> (str, str, (int, int)):
    global nome_id, linha_inicio_token, coluna_inicio_token

    nome_id_int = -1

    try:
        nome_id_int = int(nome_id)
    except ValueError:
        gera_erro_lexico(
            f'Ocorreu um erro na transformação para inteiro do número: {nome_id}',
            linha_inicio_token, coluna_inicio_token
        )

    if len(nome_id) > 10:
        gera_erro_lexico(
            f'O {nome_id} excedeu a quantidade de caracacteres permitidos para um inteiro, coloque até 10 digitos',
            linha_inicio_token, coluna_inicio_token
        )
    elif nome_id_int < 0 or nome_id_int > 32767:
        gera_erro_lexico(
            f'O {nome_id} excedeu o valor permitido, deve ser entre 0 e 32767 para inteiros',
            linha_inicio_token, coluna_inicio_token
        )

    item = tabela.tabela_de_simbolos.get(nome_id)

    if item is None:
        tabela.tabela_de_simbolos[nome_id] = ('numero', nome_id_int, 'int')

    return 'numero', nome_id, (linha_inicio_token, coluna_inicio_token)


def setFrac() -> (str, str, (int, int)):
    global nome_id, linha_inicio_token, coluna_inicio_token

    nome_id_float = -1.0

    try:
        nome_id_float = float(nome_id)
    except ValueError:
        gera_erro_lexico(
            f'Ocorreu um erro na transformação para número de ponto flutuante: {nome_id}',
            linha_inicio_token, coluna_inicio_token
        )

    if len(nome_id.split('.')[0]) > 10:
        gera_erro_lexico(
            f'O {nome_id_float} excedeu a quantidade de caracacteres permitidos para a parte inteira de um número '
            f'de ponto flutuante, coloque até 10 digitos na parte inteira',
            linha_inicio_token, coluna_inicio_token
        )
    elif len(nome_id.split('.')[1]) > 9:
        gera_erro_lexico(
            f'O {nome_id_float} excedeu a quantidade de caracacteres permitidos para a parte flutuante, coloque até 9 '
            f'digitos depois da vírgula',
            linha_inicio_token, coluna_inicio_token
        )
    elif nome_id_float < 0.0 or nome_id_float > 3.4E38:
        gera_erro_lexico(
            f'O {nome_id_float} excedeu o valor permitido, deve ser entre 0 e 3.4E+38 para ponto flutuante',
            linha_inicio_token, coluna_inicio_token
        )

    item = tabela.tabela_de_simbolos.get(nome_id)

    if item is None:
        tabela.tabela_de_simbolos[nome_id] = ('numero', nome_id_float, 'float')

    return 'numero', nome_id, (linha_inicio_token, coluna_inicio_token)


def setExp() -> (str, str, (int, int)):
    global nome_id, linha_inicio_token, coluna_inicio_token

    numero = -1.0

    try:
        numero = nome_id.split('E')
        print(numero[0], numero[1])
        numero = float(numero[0]) * pow(10, float(numero[1]))
    except ValueError:
        gera_erro_lexico(
            f'Ocorreu um erro na transformação para exponenciação: {nome_id}',
            linha_inicio_token, coluna_inicio_token
        )

    try:
        numero_antes_do_e = nome_id.split('E')[0]
        numero_antes_do_e = numero_antes_do_e.split('.')

        if len(numero_antes_do_e) == 2:  # Ex: 10.2E+3
            if len(nome_id.split('E')[0]) > 10:  # Numero de casas inteiras
                gera_erro_lexico(
                    f'O {numero} excedeu a quantidade de caracacteres permitidos para a parte inteira de um número de '
                    f'ponto flutuante, coloque até 10 digitos na parte inteira',
                    linha_inicio_token, coluna_inicio_token
                )
            elif len(numero_antes_do_e[1]) > 9:  # Numero de casas decimais
                gera_erro_lexico(
                    f'O {numero} excedeu a quantidade de caracacteres permitidos para a parte flutuante, coloque até 9 '
                    f'digitos depois da vírgula',
                    linha_inicio_token, coluna_inicio_token
                )
        else:  # Ex: 10E+3
            if len(nome_id.split('E')[0]) > 10:  # Numero de casas inteiras
                gera_erro_lexico(
                    f'O {numero} excedeu a quantidade de caracacteres permitidos para a parte inteira de um número de '
                    f'ponto flutuante, coloque até 10 digitos na parte inteira',
                    linha_inicio_token, coluna_inicio_token
                )
    except ValueError:
        pass

    if numero < 0.0 or numero > 3.4E38:
        gera_erro_lexico(
            f'O {numero} excedeu o valor permitido, deve ser entre 0 e 3.4E+38 para ponto flutuante',
            linha_inicio_token, coluna_inicio_token
        )

    item = tabela.tabela_de_simbolos.get(nome_id)

    if item is None:
        tabela.tabela_de_simbolos[nome_id] = ('numero', numero, 'float')

    return 'numero', nome_id, (linha_inicio_token, coluna_inicio_token)


def setId() -> (str, str, (int, int)):
    global nome_id, linha_inicio_token, coluna_inicio_token

    if len(nome_id) > 30:
        gera_erro_lexico(
            f'O nome da sua variável {nome_id} excedeu o limite de 30 caracteres',
            linha_inicio_token, coluna_inicio_token
        )

    item = tabela.tabela_de_simbolos.get(nome_id)

    if item is None:
        tabela.tabela_de_simbolos[item] = ('id', '', '')
        return 'id', nome_id, (linha_inicio_token, coluna_inicio_token)
    else:
        if item[0] == 'id':  # Não está reservado, mas está presente na tabela
            return 'id', nome_id, (linha_inicio_token, coluna_inicio_token)
        else:  # É reservado
            return nome_id, '-', (linha_inicio_token, coluna_inicio_token)


def setChar() -> (str, str, (int, int)):
    global nome_id, linha_inicio_token, coluna_inicio_token

    item = tabela.tabela_de_simbolos.get(nome_id)

    if item is None:
        tabela.tabela_de_simbolos[nome_id] = ('caractere', nome_id, 'char')

    return 'caractere', nome_id, (linha_inicio_token, coluna_inicio_token)


estados_finais = [2, 4, 5, 7, 8, 10, 11, 12, 13, 14, 15, 17, 20, 22, 24, 27, 31, 32, 33, 35, 36, 37, 38, 40]

tabela_transicao = {
    1: {
        '=': 2,
        '>': 3,
        '<': 6,
        '!': 9,
        '+': 11,
        '-': 12,
        '*': 13,
        '/': 14,
        '^': 15,
        '{': 16,
        "'": 18,
        'letra': 21,
        'letra_': 21,
        'ex': 21,
        'digito': 23,
        ')': 32,
        '(': 33,
        ':': 34,
        ';': 37,
        ',': 38,
        'ws': 39
    },
    2: ('oprel', 'EQ', False),
    3: {
        '=': 4,
        'outros': 5
    },
    4: ('oprel', 'GE', False),
    5: ('oprel', 'GT', True),
    6: {
        '=': 7,
        'outros': 8
    },
    7: ('oprel', 'LE', False),
    8: ('oprel', 'LT', True),
    9: {
        '=': 10
    },
    10: ('oprel', 'NE', False),
    11: ('soma_sub', 'soma', False),
    12: ('soma_sub', 'sub', False),
    13: ('mult_div', 'mult', False),
    14: ('mult_div', 'div', False),
    15: ('exp', '', False),
    16: {
        '}': 17,
        'outros': 16
    },
    17: ('', '', False),
    -18: {  # Nó extra
        'letra': 19
    },
    18: {
        '\\': -18,
        'digito': 19,
        'letra': 19,
        'letra_': 19,
        'ws': 19
    },
    19: {
        "'": 20
    },
    20: [setChar],
    21: {
        'letra': 21,
        'letra_': 21,
        'digito': 21,
        'ex': 21,
        'outros': 22
    },
    22: [setId, lookhead],
    23: {
        'digito': 23,
        '.': 25,
        'ex': 28,
        'outros': 24
    },
    24: [setInt, lookhead],
    25: {
        'digito': 26
    },
    26: {
        'digito': 26,
        'ex': 28,
        'outros': 27
    },
    27: [setFrac, lookhead],
    28: {
        'digito': 30,
        '+': 29,
        '-': 29
    },
    29: {
        'digito': 30
    },
    30: {
        'digito': 30,
        'outros': 31
    },
    31: [setExp, lookhead],
    32: (')', '', False),
    33: ('(', '', False),
    34: {
        '=': 36,
        'outros': 35
    },
    35: ('pontuacao', 'DP', True),
    36: ('atribuicao', '', False),
    37: ('pontuacao', 'PV', False),
    38: ('pontuacao', 'VR', False),
    39: {
        'ws': 39,
        'outros': 40
    },
    40: ('', '', True)
}


def acoes(estado: int) -> (str, str):
    retorno_estado_final = tabela_transicao[estado]

    if type(retorno_estado_final) is tuple:
        tipo_do_retorno, valor, faz_lookhead = retorno_estado_final

        if faz_lookhead:
            lookhead()

        return tipo_do_retorno, valor
    else:
        retorno1 = None
        retorno2 = None

        for func in retorno_estado_final:
            resp = func()

            if resp is not None:
                #  Remove a linha e coluna
                retorno1 = resp[0]
                retorno2 = resp[1]

        return retorno1, retorno2


def prox_char() -> str:
    global arquivo

    char = arquivo.read(1)

    if char == '':
        return 'EOF'
    else:
        return char


def final(estado: int) -> bool:
    return estado in estados_finais


def tipo_char(char: str) -> str:
    if char == 'EOF':
        return char
    elif char.isdigit():
        return 'digito'
    elif char.isalpha():
        if char == 'E':
            return 'ex'

        return 'letra'
    elif char == '_':
        return 'letra_'
    elif char == ' ' or char == '\t':
        return 'ws'
    elif char == '\n':
        global linha, coluna
        linha += 1
        coluna = 1

        return 'ws'
    else:
        return char


def move(estado: int, char: str) -> int:
    tipo_do_char = tipo_char(char)

    if estado in tabela_transicao:
        if tipo_do_char in tabela_transicao[estado]:
            global nome_id
            nome_id += char

            return tabela_transicao[estado][tipo_do_char]
        elif 'outros' in tabela_transicao[estado] or tipo_do_char == 'EOF':
            valor = tabela_transicao[estado]['outros']

            if final(valor) and char == '\n':
                global linha
                linha -= 1

            return valor
    else:
        return -1


def estado_inicial() -> int:
    return 1


def getToken() -> (str, str, int, int):
    global linha_inicio_token, coluna_inicio_token, travar, tipo

    if travar is True:
        travar = False
        return tipo[0], tipo[1], linha_inicio_token, coluna_inicio_token

    global nome_id, linha, coluna

    nome_id = ''
    coluna_inicio_token = coluna
    linha_inicio_token = linha

    estado = estado_inicial()
    char = prox_char()

    while char != 'EOF' and estado != -1:
        coluna += 1

        estado = move(estado, char)

        if final(estado):
            break

        char = prox_char()

    if char == 'EOF':
        if not final(estado):
            estado = move(estado, char)

    if final(estado):
        tipo = acoes(estado)

        if (tipo[0] == '' and tipo[1] == '') or re.match(r'^[\s\t\n]*$', nome_id):
            return getToken()
        else:
            return tipo[0], tipo[1], linha_inicio_token, coluna_inicio_token
    else:
        msg_add = ''

        if not final(estado):
            msg_add = 'Não é um token válido.'

        gera_erro_lexico(f'{msg_add}', linha_inicio_token, coluna_inicio_token)


if __name__ == '__main__':
    abre_arquivo('testes/teste01.txt')

    for _ in range(100):
        tipo0, tipo1, linha, coluna = getToken()
        print(tipo0)

    fecha_arquivo()
