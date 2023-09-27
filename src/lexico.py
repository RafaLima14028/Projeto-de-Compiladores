import tabela_de_simbolos as tabela
import tabela_de_simbolos_metodos as funcs

arquivo = None
nome_id = None


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
        return None, None, None
        # TODO: RETORNAR OS VALORES
    else:
        if item[0] == 'id':  # Não está reservado, mas está presente na tabela
            return None, None, None
            # TODO: RETORNAR OS VALORES
        else:  # É reservado
            return None, None, None
            # TODO: RETORNAR OS VALORES


def setChar() -> None:
    ...


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
        'digito': 23,
        ')': 32,
        '(': 33,
        ':': 34,
        ';': 37,
        ',': 38,
        'ws': 39
    },
    2: funcs.return_oprel_eq,
    3: {
        '=': 4,
        'outros': 5
    },
    4: setId,
    5: setId,
    6: {
        '=': 7,
        'outros': 8
    },
    7: setId,
    8: setId,
    21: {
        'letra_': 21,
        'digito': 21,
        'outros': 22
    },
    22: setId
}


def tipo_char(char: str) -> str:
    if char == 'EOF':
        return char
    elif char.isdigit():
        return 'digito'
    elif char.isalpha() or char == '_':
        return 'letra_'
    elif char == ' ' or char == '\t' or char == '\n':
        return 'ws'
    else:
        return char


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


def prox_char() -> str:
    global arquivo

    char = arquivo.read(1)

    if char != '':
        return char
    else:
        return 'EOF'


def final(estado: int) -> bool:
    if estado in estados_finais:
        return True
    else:
        return False


def move(estado: int, char: str) -> int:
    tipo_do_char = tipo_char(char)

    outros = 'outros'

    if estado in tabela_transicao and tipo_do_char in tabela_transicao[estado]:
        return tabela_transicao[estado][tipo_do_char]
    elif estado in tabela_transicao and outros in tabela_transicao[estado]:
        return tabela_transicao[estado][outros]
    else:
        return -1


def estado_inicial() -> int:
    return 1


def acoes(estado: int) -> None:
    print(tabela_transicao[estado]())


def getToken() -> None:
    global nome_id

    print_estado = True
    estado = estado_inicial()
    char = prox_char()

    if print_estado:
        print(f'O estado atual é: {estado}')
        print(f'O caractere atual é: {char}')
        print()

    while char != 'EOF' and not final(estado) and estado != -1:
        estado = move(estado, char)
        char = prox_char()

        if print_estado:
            print(f'O estado atual é: {estado}')
            print(f'O caractere atual é: {char}')
            print()

    # if char == 'EOF':
    #     estado = move(estado, char)

    if final(estado):
        print('Cadeia aceita')
        acoes(estado)
    else:
        print('Cadeia rejeitada')


if __name__ == '__main__':
    abre_arquivo('testes/teste01.txt')

    getToken()

    arquivo.close()
