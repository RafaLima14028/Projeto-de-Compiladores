#  Implementado por descida recursiva
from lexico import getToken, volta_token_anterior, abre_arquivo, fecha_arquivo

FIRST_DAS_TRANSICOES = {
    'call': ['program'],
    'bloco': ['begin'],
    'variaveis': ['int', 'float', 'char'],
    'variaveis_linha': ['int', 'float', 'char'],
    'variavel': ['int', 'float', 'char'],
    'lista_ids': ['id'],
    'lista_ids_linha': [','],
    'cmds': ['id', 'if', 'while', 'repeat'],
    'cmds_linha': ['id', 'if', 'while', 'repeat'],
    'cmd': ['id', 'if', 'while', 'repeat'],
    'cmd_atrib': ['id'],
    'cmd_cond': ['if'],
    'cmd_rep': ['while', 'repeat'],
    'cmd_bloco': ['begin', 'id', 'if', 'while', 'repeat'],
    'cmd_else': ['else'],
    'cond': ['id', 'numero', 'caractere', '('],
    'expre': ['id', 'numero', 'caractere', '('],
    'expre_linha': ['soma_sub'],
    'expre2': ['id', 'numero', 'caractere', '('],
    'expre2_linha': ['mult_div'],
    'expre3': ['soma_sub', 'id', 'numero', 'caractere', '('],
    'expre3_linha': ['exp'],
    'unario': ['soma_sub', 'id', 'numero', 'caractere', '('],
    'term': ['id', 'numero', 'caractere', '(']
}


def gera_erro_sintatico(msg: str, linha: int, coluna: int,
                        funcao_origem_do_erro: str = None, ultima_coisa_lida: str = None) -> None:
    msg_extra = ''

    if funcao_origem_do_erro is not None:
        msg_extra = f'\nA função que originou o erro foi a: {funcao_origem_do_erro}. '
    if ultima_coisa_lida is not None:
        msg_extra += f'A última coisa lida antes de parar foi: {ultima_coisa_lida}'

    raise Exception(
        f'Ocorreu um erro na análise sintática: {msg} em {linha}:{coluna}. {msg_extra}'
    )


def procedimento_lista_ids_linha() -> None:
    print()
    print('Procedimento das lista ids linha')
    tipo, valor, linha, coluna = getToken()

    if tipo == 'pontuacao' and valor == 'VR':
        tipo = ','

        while tipo in FIRST_DAS_TRANSICOES['lista_ids_linha']:
            if tipo == ',':
                print(tipo)
                tipo, valor, linha, coluna = getToken()

                if tipo == 'id':
                    print(tipo, valor)
                    tipo, valor, linha, coluna = getToken()
                else:
                    gera_erro_sintatico('Era esperado um nome para a variável depois da ,', linha, coluna)

        volta_token_anterior()
    else:
        volta_token_anterior()


def procedimento_lista_ids() -> None:
    print()
    print('Procedimento das lista ids')
    tipo, valor, linha, coluna = getToken()

    if tipo == 'id':
        print(tipo, valor)
        procedimento_lista_ids_linha()
    else:
        gera_erro_sintatico('Era esperado um nome para a variável', linha, coluna)


def procedimento_variavel() -> None:
    print()
    print('Procedimento das variavel')
    tipo, valor, linha, coluna = getToken()

    if tipo == 'pontuacao' and valor == 'DP':
        print(':')

        procedimento_lista_ids()

        tipo, valor, linha, coluna = getToken()

        print('Procedimento das variavel')
        print(tipo, valor)
        if tipo == 'pontuacao' and valor == 'PV':
            print(';')
        else:
            gera_erro_sintatico('Era esperado o símbolo ;', linha, coluna,
                                'procedimento_variavel()',
                                f'{tipo} e {valor}')
    else:
        gera_erro_sintatico('Era esperado o símbolo :', linha, coluna)


def procedimento_variaveis_linha() -> None:
    print()
    print('-' * 3)
    print('Procedimento das variaveis linha')

    tipo, valor, linha, coluna = getToken()

    if tipo in FIRST_DAS_TRANSICOES['variaveis_linha']:
        while tipo in FIRST_DAS_TRANSICOES['variaveis_linha']:
            print(tipo)

            procedimento_variavel()

            tipo, valor, linha, coluna = getToken()

        volta_token_anterior()
    else:
        volta_token_anterior()


def procedimento_variaveis() -> None:
    print()
    print('Procedimento das variaveis')
    procedimento_variaveis_linha()


def procedimento_term() -> None:
    print()
    print('Procedimento term')

    tipo, valor, linha, coluna = getToken()

    print(f'NO TERM(DEBUG): {tipo} e {valor}')

    if tipo == 'id':
        print(tipo, valor)
    elif tipo == 'numero':
        print(tipo, valor)
    elif tipo == 'caractere':
        print(tipo, valor)
    elif tipo == '(':
        procedimento_expre()
        tipo, valor, linha, coluna = getToken()

        if tipo == ')':
            print(')')
        else:
            gera_erro_sintatico('Era esperado um )', linha, coluna,
                                'procedimento_term()',
                                f'{tipo} e {valor}')
    else:
        gera_erro_sintatico(
            'Era esperado um termo válido como: id, numero, caractere ou (', linha, coluna,
            'procedimento_term()',
            f'{tipo} e {valor}')


def procedimento_unario() -> None:
    print()
    print('Procedimento unario')

    tipo, valor, linha, coluna = getToken()
    print(f'PROCEDIMENTO UNARIO (DEBUG): {tipo} e {valor}')

    if tipo == 'soma_sub':
        print(tipo, valor)
        procedimento_term()
    else:
        volta_token_anterior()
        procedimento_term()


def procedimento_expre3_linha() -> None:
    print()
    print('Procedimento expre3_linha')

    tipo, valor, linha, coluna = getToken()

    while tipo in FIRST_DAS_TRANSICOES['expre3_linha']:
        print(tipo)
        procedimento_unario()

        tipo, valor, linha, coluna = getToken()
        print(f'DENTRO DO EXPRE3_LINHA(DEBUG): {tipo} e {valor}')

    volta_token_anterior()


def procedimento_expre3() -> None:
    print()
    print('Procedimento expre3')

    procedimento_unario()

    tipo, valor, linha, coluna = getToken()
    print(f'ANTES DO TERM(DEBUG): {tipo} e {valor}')
    volta_token_anterior()

    procedimento_expre3_linha()


def procedimento_expre2_linha() -> None:
    print()
    print('Procedimento expre2_linha')

    tipo, valor, linha, coluna = getToken()

    while tipo in FIRST_DAS_TRANSICOES['expre2_linha']:
        print(tipo)
        procedimento_expre3()

        tipo, valor, linha, coluna = getToken()

    volta_token_anterior()


def procedimento_expre2() -> None:
    print()
    print('Procedimento expre2')

    procedimento_expre3()

    tipo, valor, linha, coluna = getToken()
    print(f'ANTES DO EXPRE3(DEBUG): {tipo} e {valor}')
    volta_token_anterior()

    procedimento_expre2_linha()


def procedimento_expre_linha() -> None:
    print()
    print('Procedimento expre_linha')

    tipo, valor, linha, coluna = getToken()

    while tipo in FIRST_DAS_TRANSICOES['expre_linha']:
        print(tipo)
        procedimento_expre2()

        tipo, valor, linha, coluna = getToken()

    volta_token_anterior()


def procedimento_expre() -> None:
    print()
    print('Procedimento expre')

    procedimento_expre2()
    tipo, valor, linha, coluna = getToken()
    print(f'ANTES DO EXPRE2(DEBUG): {tipo} e {valor}')
    volta_token_anterior()
    procedimento_expre_linha()


def procedimento_cond() -> None:
    print()
    print('Procedimento cond')

    procedimento_expre()

    tipo, valor, linha, coluna = getToken()
    if tipo == 'oprel':
        print(tipo, valor)

        procedimento_expre()
    else:
        gera_erro_sintatico('Era esperado um operador relacional', linha, coluna)


def procedimento_else_cmd() -> None:
    print()
    print('Prodimento else_cmd')

    tipo, valor, linha, coluna = getToken()

    if tipo == 'else':
        print(tipo)
        procedimento_cmd_bloco()
    else:
        volta_token_anterior()


def procedimento_cmd_rep() -> None:
    print()
    print('Procedimento cmd_rep')

    tipo, valor, linha, coluna = getToken()

    if tipo == 'while':
        print(tipo)
        procedimento_cond()
        procedimento_cmd_bloco()
    elif tipo == 'repeat':
        print(tipo)
        procedimento_cmd_bloco()

        tipo, valor, linha, coluna = getToken()

        if tipo == 'until':
            print(tipo)

            procedimento_cond()

            tipo, valor, linha, coluna = getToken()

            if tipo == 'pontuacao' and valor == 'PV':
                print(';')
            else:
                gera_erro_sintatico('Era esperado um ponto e vírgula (;)', linha, coluna)
        else:
            gera_erro_sintatico('Era esperado um until', linha, coluna)
    else:
        gera_erro_sintatico('Era esperado um while ou repeat', linha, coluna)


def procedimento_cmd_bloco() -> None:
    tipo, valor, linha, coluna = getToken()

    if tipo == 'begin':
        volta_token_anterior()
        procedimento_bloco()
    elif tipo in FIRST_DAS_TRANSICOES['cmd']:
        volta_token_anterior()
        procedimento_cmd()
    else:
        gera_erro_sintatico(
            'Era esperado um comando válido', linha, coluna,
            'procedimento_cmd_bloco()', f'{tipo} e {valor}'
        )


def procedimento_cmd_cond() -> None:
    print()
    print('Procedimento cmd_cond')

    tipo, valor, linha, coluna = getToken()

    if tipo == 'if':
        print(tipo)
        procedimento_cond()

        tipo, valor, linha, coluna = getToken()

        if tipo == 'then':
            print(tipo)
            procedimento_cmd_bloco()
            procedimento_else_cmd()
        else:
            gera_erro_sintatico('Era esperado um then', linha, coluna)
    else:
        gera_erro_sintatico('Era esperado um if', linha, coluna)


def procedimento_cmd_atrib() -> None:
    print()
    print('Procedimento cmd_atrib')

    tipo, valor, linha, coluna = getToken()

    if tipo == 'id':
        print(tipo, valor)
        tipo, valor, linha, coluna = getToken()

        if tipo == 'atribuicao':
            print(':=')

            procedimento_expre()  # Está retornando 2

            tipo, valor, linha, coluna = getToken()

            if tipo == 'pontuacao' and valor == 'PV':
                print(';')
            else:
                gera_erro_sintatico('Era esperado ponto e vírugula (;)', linha, coluna,
                                    'procedimento_cmd_atrib()',
                                    f'{tipo} e {valor}')
        else:
            gera_erro_sintatico('Era esprado um atribuição (:=)', linha, coluna)
    else:
        gera_erro_sintatico('Era esperado um variável', linha, coluna)


def procedimento_cmd() -> None:
    print()
    print('Procedimento cmd')

    tipo, valor, linha, coluna = getToken()

    while tipo in FIRST_DAS_TRANSICOES['cmd']:
        if tipo == 'id':
            volta_token_anterior()
            procedimento_cmd_atrib()
        elif tipo == 'if':
            volta_token_anterior()
            procedimento_cmd_cond()
        elif tipo == 'while' or tipo == 'repeat':
            volta_token_anterior()
            procedimento_cmd_rep()

        tipo, valor, linha, coluna = getToken()

    volta_token_anterior()


def procedimento_cmds() -> None:
    print()
    print('Procedimento cmds')

    tipo, valor, linha, coluna = getToken()

    if tipo in FIRST_DAS_TRANSICOES['cmd']:
        volta_token_anterior()
        procedimento_cmd()
    else:
        gera_erro_sintatico('Era esperado um comando válido', linha, coluna)


def procedimento_bloco() -> None:
    print()
    print('Procedimento do bloco')
    tipo, valor, linha, coluna = getToken()
    print(f'Imprimi algo 1: {tipo, valor}')

    if tipo == 'begin':
        print(tipo)
        print('#' * 30)
        procedimento_variaveis()

        print('#' * 30)
        procedimento_cmds()

        tipo, valor, linha, coluna = getToken()
        print(f'Imprimi algo 2: {tipo, valor}')
        if tipo == 'end':
            print('end')
            print('CHEGOU NO FINAL DO PROGRAMA')
        else:
            gera_erro_sintatico(
                'Era esperado fechamento de bloco (end)', linha, coluna,
                'procedimento_bloco()', f'{tipo} e {valor}'
            )
    else:
        gera_erro_sintatico('Era esperado abertura de bloco (begin)', linha, coluna)


def procedimento_call() -> None:
    print()
    print('Procedimento do call')
    tipo, valor, linha, coluna = getToken()

    if tipo == 'program':
        print(tipo)
        tipo, valor, linha, coluna = getToken()

        if tipo == 'id':
            print(tipo)
            tipo, valor, linha, coluna = getToken()

            if tipo == '(':
                print(tipo)
                tipo, valor, linha, coluna = getToken()

                if tipo == ')':
                    print(tipo)
                    procedimento_bloco()
                else:
                    gera_erro_sintatico('Era esperado fechamento de parenteses', linha, coluna)
            else:
                gera_erro_sintatico('Era esperado abertura de parenteses', linha, coluna)
        else:
            gera_erro_sintatico('Era esperado um nome para o program', linha, coluna)
    else:
        gera_erro_sintatico('Era esperado a palavra reservada program', linha, coluna)


if __name__ == '__main__':
    abre_arquivo('testes/teste02.txt')

    procedimento_call()

    fecha_arquivo()
