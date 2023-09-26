import tabela_de_simbolos as tabela
from tabela_de_transicao import tabela_transicao, estados_finais

arquivo = None
nome_id = None


def tipo_char(char: str) -> str:
    if char.isdigit():
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
        # TODO: RETORNAR OS VALORES
    else:
        if item[0] == 'id':  # Não está reservado, mas está presente na tabela
            ...
            # TODO: RETORNAR OS VALORES
        else:  # É reservado
            ...
            # TODO: RETORNAR OS VALORES


def setChar() -> None:
    ...


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


def move(estado: int, char: str) -> str | int:
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
    if final(estado):
        tipo, valor, eh_lookhead = tabela_transicao[estado]()

        print(tipo, valor)

        if eh_lookhead:
            lookhead()


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

    if final(estado) and estado != -1:
        print('Cadeia aceita')
        acoes(estado)
    else:
        print('Cadeia rejeitada')


if __name__ == '__main__':
    abre_arquivo('testes/teste01.txt')

    getToken()

    arquivo.close()
