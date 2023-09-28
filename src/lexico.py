import tabela_de_simbolos as tabela

arquivo = None
nome_id = None


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


def lookhead() -> None:
    arquivo.seek(arquivo.tell() - 1, 0)


def setInt() -> None:
    global nome_id

    item = tabela.tabela_de_simbolos.get(nome_id)

    if item is None:
        tabela.tabela_de_simbolos[nome_id] = ('numero', int(nome_id), 'int')

    # TODO: RETORNAR OS VALORES


def setFrac() -> None:
    global nome_id

    item = tabela.tabela_de_simbolos.get(nome_id)

    if item is None:
        tabela.tabela_de_simbolos[nome_id] = ('numero', float(nome_id), 'float')

    # TODO: RETORNAR OS VALORES


def setExp() -> None:
    global nome_id

    item = tabela.tabela_de_simbolos.get(nome_id)

    if item is None:
        ...

    # TODO: RETORNAR OS VALORES


def setId() -> None:
    global nome_id

    item = tabela.tabela_de_simbolos.get(nome_id)

    if item is None:
        tabela.tabela_de_simbolos[item] = ('id', '', '')
        ...
        # TODO: RETORNAR OS VALORES
    else:
        if item[0] == 'id':  # Não está reservado, mas está presente na tabela
            ...
            # TODO: RETORNAR OS VALORES
        else:  # É reservado
            ...
            # TODO: RETORNAR OS VALORES


def setChar() -> None:
    global nome_id


estados_finais = [
    2, 4, 5, 7, 8, 10, 11, 12, 13, 14, 15,
    17, 20, 22, 24, 27, 31, 32, 33, 35, 36,
    37, 38, 40
]

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
    # TODO: IMPLEMENTAR O NÓ 18
    # 18: {
    #     '\\': 18,
    #     'outros': 19
    # },
    19: {
        "'": 20
    },
    20: [setChar],
    21: {
        'letra_': 21,
        'digito': 21,
        'ex': 21,
        'ws': 22
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
    32: ('fecha_parenteses', '', False),
    33: ('abre_parenteses', '', False),
    34: {
        '=': 36,
        'outros': 35
    },
    35: ('pontucao', 'DP', True),
    36: ('atribuicao', '', False),
    37: ('pontuacao', 'PV', False),
    38: ('pontuacao', 'VR', False),
    39: {
        'ws': 39,
        'outros': 40
    },
    40: ('', '', True)
}


def acoes(estado: int) -> None:
    retorno_estado_final = tabela_transicao[estado]

    if type(retorno_estado_final) is tuple:
        tipo, valor, faz_lookhead = retorno_estado_final

        if tipo == '':
            tipo = None
        if valor == '':
            valor = None
        print(tipo, valor, faz_lookhead)

        if faz_lookhead:
            lookhead()
    else:
        for func in retorno_estado_final:
            # func()
            print(func)


def prox_char() -> str:
    global arquivo

    try:
        return arquivo.read(1)
    except StopIteration:
        return 'EOF'


def final(estado: int) -> bool:
    if estado in estados_finais:
        return True
    else:
        return False


def tipo_char(char: str) -> str:
    if char == 'EOF':
        return char
    elif char.isdigit():
        return 'digito'
    elif char.isalpha() or char == '_':
        if char == 'E':
            return 'ex'

        return 'letra_'
    elif char == ' ' or char == '\t' or char == '\n':
        return 'ws'
    else:
        return char


def move(estado: int, char: str) -> int:
    tipo_do_char = tipo_char(char)

    print(tipo_do_char)

    outros = 'outros'

    if estado in tabela_transicao and tipo_do_char in tabela_transicao[estado]:
        return tabela_transicao[estado][tipo_do_char]
    elif estado in tabela_transicao and outros in tabela_transicao[estado]:
        return tabela_transicao[estado][outros]
    else:
        return -1


def estado_inicial() -> int:
    return 1


def getToken() -> None:
    global nome_id

    nome_id = ''

    print_estado = True
    estado = estado_inicial()
    char = prox_char()

    while char != 'EOF' and estado != -1:
        if print_estado:
            print(f'O estado atual é: {estado}')
            print(f'O caractere atual é: {char}')
            print()

        estado = move(estado, char)

        if not final(estado):
            nome_id += char
            # print(f'Nome_id atual: {nome_id}')

        if final(estado):
            break

        char = prox_char()

    if print_estado:
        print(f'O estado atual é: {estado}')
        print(f'O caractere atual é: {char}')
    # print()
    # print()

    if final(estado):
        print('Cadeia aceita')
        acoes(estado)
    else:
        print('Cadeia rejeitada')

    print(nome_id)


if __name__ == '__main__':
    # abre_arquivo('testes/teste01.txt')
    abre_arquivo('testes/teste02.txt')

    # for i in range(25):
    getToken()
    # print()

    arquivo.close()
