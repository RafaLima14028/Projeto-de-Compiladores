#  Implementado por descida recursiva
from lexico import getToken, abre_arquivo, fecha_arquivo

FIRST_DAS_TRANSICOES = {
    'call': ['program'],
    'bloco': ['abre_bloco'],
    'variaveis': ['int', 'float', 'char'],
    'variaveis_linha': ['int', 'float', 'char'],
    'variavel': ['int', 'float', 'char'],
    'lista_ids': ['id'],
    'lista_ids_linha': [','],
    'comandos': ['id', 'if', 'while', 'repeat'],
    'comandos_linha': ['id', 'if', 'while', 'repeat'],
    'comando': ['id', 'if', 'while', 'repeat'],
    'comando_bloco': ['id', 'if', 'while', 'repeat', '{'],
    'comando_bloco_linha': ['else'],
    'cond': ['id', 'numero', 'caractere', '(', 'unario'],
    'expre': ['id', 'numero', 'caractere', '(', 'unario'],
    'expre_linha': ['+', '-', 'op'],
    'expre2': ['id', 'numero', 'caractere', '(', 'unario'],
    'expre2_linha': ['*', '/', 'op'],
    'expre3': ['+', '-', 'id', 'numero', 'caractere', '('],
    'expre3_linha': ['exp', ],
    'unario': ['soma_sub', 'id', 'numero', 'caractere', '('],
    'op': ['oprel', 'atribuicao'],
    'term': ['id', 'numero', 'caractere', '(']
}


def descompacta_tipo_token(prox_token: ((str, str), (int, int), bool)) -> (str, str, int, int):
    return prox_token[0][0], prox_token[0][1], prox_token[1][0], prox_token[1][1]


def final_do_arquivo(prox_token: ((str, str), (int, int), bool)) -> bool:
    if prox_token[2]:
        return True
    else:
        return False


def gera_erro_sintatico(msg: str, linha: int, coluna: int) -> Exception:
    raise Exception(f'Ocorreu um erro na análise sintática: {msg} em {linha}:{coluna}')


def procedimento_lista_ids_linha() -> (str, str, int, int):
    print()
    print('Procedimento das lista ids linha')
    tipo, valor, linha, coluna = descompacta_tipo_token(getToken())

    if tipo == 'pontuacao':
        if valor == 'VR':
            tipo, valor, linha, coluna = descompacta_tipo_token(getToken())

            if tipo == 'id':
                print(tipo, valor)
                return procedimento_lista_ids_linha()
            else:
                gera_erro_sintatico('Era esperado um nome para a variável depois da ,', linha, coluna)
        else:
            return tipo, valor, linha, coluna
    else:
        return tipo, valor, linha, coluna


def procedimento_lista_ids() -> (str, str, int, int):
    print()
    print('Procedimento das lista ids')
    tipo, valor, linha, coluna = descompacta_tipo_token(getToken())

    if tipo == 'id':
        print(tipo, valor)
        return procedimento_lista_ids_linha()
    else:
        gera_erro_sintatico('Era esperado um nome para a variável', linha, coluna)


def procedimento_variavel():
    print()
    print('Procedimento das variavel')
    tipo, valor, linha, coluna = descompacta_tipo_token(getToken())

    if tipo == 'pontuacao' and valor == 'DP':
        print(':')

        tipo, valor, linha, coluna = procedimento_lista_ids()
        print('Procedimento das variavel')

        if tipo is None:
            tipo, valor, linha, coluna = descompacta_tipo_token(getToken())

        print(tipo)
        if tipo == 'pontuacao' and valor == 'PV':
            print(';')
        else:
            gera_erro_sintatico('Era esperado o símbolo ;', linha, coluna)
    else:
        gera_erro_sintatico('Era esperado o símbolo :', linha, coluna)


def procedimento_variaveis_linha():
    print()
    print('-' * 3)
    print('Procedimento das variaveis linha')

    tipo, valor, linha, coluna = descompacta_tipo_token(getToken())

    if tipo in FIRST_DAS_TRANSICOES['variaveis_linha']:
        while tipo in FIRST_DAS_TRANSICOES['variaveis_linha']:
            print(tipo)

            procedimento_variavel()

            tipo, valor, linha, coluna = descompacta_tipo_token(getToken())

    return tipo, valor, linha, coluna


def procedimento_variaveis():
    print()
    print('Procedimento das variaveis')

    return procedimento_variaveis_linha()


def procedimento_term():
    tipo, valor, linha, coluna = descompacta_tipo_token(getToken())

    if tipo == 'id':
        print(tipo, valor)
    elif tipo == 'numero':
        print(tipo, valor)
    elif tipo == 'caractere':
        print(tipo, valor)
    elif tipo == 'abre_parenteses':
        procedimento_expre()
        tipo, valor, linha, coluna = descompacta_tipo_token(getToken())
        if tipo == 'fecha_parenteses':
            print(tipo)
    else:
        gera_erro_sintatico('Era esperado um id, numero, caractere ou (', linha, coluna)


def procedimento_unario(tipo, valor, linha, coluna):
    print()
    print('-' * 3)
    print('Procedimento dos unarios')

    if tipo is None:
        tipo, valor, linha, coluna = descompacta_tipo_token(getToken())

    if tipo == 'soma_sub':
        print(tipo, valor)
        procedimento_term()
    elif tipo in FIRST_DAS_TRANSICOES['unario']:
        print(tipo, valor)
    else:
        gera_erro_sintatico('Era esperado +, -, varivel, numero, caractere ou (', linha, coluna)


def procedimento_expre3_linha():
    print()
    print('Procedimento do expre3 linha')

    tipo, valor, linha, coluna = descompacta_tipo_token(getToken())

    if tipo == 'exp':
        print('^')
        procedimento_unario(None, None, None, None)
        return procedimento_expre3_linha()
    else:
        return tipo, valor, linha, coluna


def procedimento_expre3():
    print()
    print('Procedimento do expre3')

    tipo, valor, linha, coluna = descompacta_tipo_token(getToken())

    print(tipo, valor)

    if tipo in FIRST_DAS_TRANSICOES['unario']:
        procedimento_unario(tipo, valor, linha, coluna)
        procedimento_expre3_linha()
    else:
        gera_erro_sintatico('Era esperado +, -, variavel, numero, caractere, (, operador relacional ou atribuicao',
                            linha, coluna)


def procedimento_expre2_linha():
    tipo, valor, linha, coluna = descompacta_tipo_token(getToken())

    if tipo == 'mult_div':
        procedimento_expre3()
        procedimento_expre2_linha()


def procedimento_expre2():
    procedimento_expre3()
    procedimento_expre2_linha()


def procedimento_expre_linha():
    tipo, valor, linha, coluna = descompacta_tipo_token(getToken())

    if tipo == 'soma_sub':
        procedimento_expre2()
        procedimento_expre_linha()


def procedimento_expre():
    procedimento_expre2()
    procedimento_expre_linha()


def procedimento_cond():
    print()
    print('-' * 4)
    print('Procedimento do cond')
    procedimento_expre()

    tipo, valor, linha, coluna = descompacta_tipo_token(getToken())

    if tipo == 'oprel':
        procedimento_expre()
    else:
        gera_erro_sintatico('Era esperado um operador relacional', linha, coluna)


def procedimento_comandos_linha(tipo, valor, linha, coluna):
    print()
    print('Procedimento do comando linha')

    if tipo in FIRST_DAS_TRANSICOES['comandos_linha']:
        while tipo in FIRST_DAS_TRANSICOES['comandos_linha']:
            if tipo == 'id':
                print(tipo, valor)
                tipo, valor, linha, coluna = descompacta_tipo_token(getToken())

                if tipo == 'atribuicao':
                    print(':=')

                    procedimento_expre()
            elif tipo == 'if':
                print('if')
                procedimento_cond()

                tipo, valor, linha, coluna = descompacta_tipo_token(getToken())
                if tipo == 'then':
                    ...
                else:
                    raise Exception(
                        f'Ocorreu um erro na análise sintática: Era esperado um then para concluir o if '
                        f'em {linha}:{coluna}')
            elif tipo == 'while':
                ...
            elif tipo == 'repeat':
                ...
            else:
                raise Exception(
                    f'Ocorreu um erro na análise sintática: Era esperado uma atribuição (:=) depois da variavel '
                    f'em {linha}:{coluna}')

            tipo, valor, linha, coluna = descompacta_tipo_token(getToken())
    else:
        raise Exception(
            f'Ocorreu um erro na análise sintática: Era esperado uma variável, if, while ou repeat '
            f'em {linha}:{coluna}')


def procedimento_comandos(tipo, valor, linha, coluna):
    print()
    print('-' * 3)
    print('Procedimento do comando')
    procedimento_comandos_linha(tipo, valor, linha, coluna)


def procedimento_bloco():
    print()
    print('Procedimento do bloco')
    tipo, valor, linha, coluna = descompacta_tipo_token(getToken())

    if tipo == 'begin':
        print(tipo)
        resultado_variaveis = procedimento_variaveis()

        if resultado_variaveis is None:
            tipo, valor, linha, coluna = descompacta_tipo_token(getToken())
            procedimento_comandos(tipo, valor, linha, coluna)
        else:
            tipo, valor, linha, coluna = resultado_variaveis
            procedimento_comandos(tipo, valor, linha, coluna)

        # tipo, valor, linha, coluna = descompacta_tipo_token(getToken())
        # if tipo == 'end':
        #     return
        # else:
        #     raise Exception(
        #         f'Ocorreu um erro na análise sintática: Era esperado fechamento de bloco (end) em '
        #         f'{linha}:{coluna}')
    else:
        raise Exception(
            f'Ocorreu um erro na análise sintática: Era esperado abertura de bloco (begin) em '
            f'{linha}:{coluna}')


def procedimento_call() -> None:
    print()
    print('Procedimento do call')
    tipo, valor, linha, coluna = descompacta_tipo_token(getToken())

    if tipo == 'program':
        print(tipo)
        tipo, valor, linha, coluna = descompacta_tipo_token(getToken())

        if tipo == 'id':
            print(tipo)
            tipo, valor, linha, coluna = descompacta_tipo_token(getToken())

            if tipo == 'abre_parenteses':
                print(tipo)
                tipo, valor, linha, coluna = descompacta_tipo_token(getToken())

                if tipo == 'fecha_parenteses':
                    print(tipo)
                    procedimento_bloco()
                else:
                    raise Exception(f'Ocorreu um erro na análise sintática: Era esperado fechamento de parenteses em '
                                    f'{linha}:{coluna}')
            else:
                raise Exception(f'Ocorreu um erro na análise sintática: Era esperado abertura de parenteses em '
                                f'{linha}:{coluna}')
        else:
            raise Exception(f'Ocorreu um erro na análise sintática: Era esperado um nome para o program em '
                            f'{linha}:{coluna}')
    else:
        raise Exception(f'Ocorreu um erro na análise sintática: Era esperado a palavra reservada program em '
                        f'{linha}:{coluna}')


if __name__ == '__main__':
    abre_arquivo('testes/teste02.txt')

    procedimento_call()

    fecha_arquivo()
