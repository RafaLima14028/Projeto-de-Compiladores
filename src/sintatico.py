#  Implementado por descida recursiva
from time import time
import os
from anytree import Node, RenderTree

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


def procedimento_lista_ids_linha(raiz: Node) -> None:
    no_pai = Node("lista_ids'", raiz)

    tipo, valor, linha, coluna = getToken()

    if tipo == 'pontuacao' and valor == 'VR':
        tipo = ','

        while tipo in FIRST_DAS_TRANSICOES['lista_ids_linha']:
            if tipo == ',':
                Node(',', no_pai)

                tipo, valor, linha, coluna = getToken()

                if tipo == 'id':
                    Node(tipo, no_pai)

                    tipo, valor, linha, coluna = getToken()

                    if tipo == 'pontuacao' and valor == 'VR':
                        tipo = ','
                else:
                    gera_erro_sintatico('Era esperado um nome para a variável depois da ,', linha, coluna)

    volta_token_anterior()


def procedimento_lista_ids(raiz: Node) -> None:
    no_pai = Node('lista_ids', raiz)

    tipo, valor, linha, coluna = getToken()

    if tipo == 'id':
        Node(tipo, parent=no_pai)

        procedimento_lista_ids_linha(no_pai)
    else:
        gera_erro_sintatico('Era esperado um nome para a variável', linha, coluna)


def procedimento_variavel(raiz: Node) -> None:
    no_pai = Node('variavel', raiz)

    tipo, valor, linha, coluna = getToken()

    if tipo == 'int' or tipo == 'float' or tipo == 'char':
        Node(tipo, no_pai)

        tipo, valor, linha, coluna = getToken()

        if tipo == 'pontuacao' and valor == 'DP':
            Node(':', parent=no_pai)

            procedimento_lista_ids(no_pai)

            tipo, valor, linha, coluna = getToken()

            if tipo == 'pontuacao' and valor == 'PV':
                Node(';', parent=no_pai)
            else:
                gera_erro_sintatico('Era esperado o símbolo ;', linha, coluna,
                                    'procedimento_variavel()',
                                    f'{tipo} e {valor}')
        else:
            gera_erro_sintatico('Era esperado o símbolo :', linha, coluna)
    else:
        gera_erro_sintatico('Era esperado o tipo da variável', linha, coluna)


def procedimento_variaveis_linha(raiz: Node) -> None:
    tipo, valor, linha, coluna = getToken()

    if tipo in FIRST_DAS_TRANSICOES['variaveis_linha']:
        while tipo in FIRST_DAS_TRANSICOES['variaveis_linha']:
            no_pai = Node("variaveis'", raiz)

            volta_token_anterior()

            procedimento_variavel(no_pai)

            tipo, valor, linha, coluna = getToken()

    volta_token_anterior()


def procedimento_variaveis(no_pai_anterior: Node) -> None:
    pai = Node('variaveis', no_pai_anterior)

    procedimento_variaveis_linha(pai)


def procedimento_term(raiz: Node) -> None:
    no_pai = Node('term', raiz)

    tipo, valor, linha, coluna = getToken()

    if tipo == 'id':
        Node(tipo, no_pai)
    elif tipo == 'numero':
        Node(tipo, no_pai)
    elif tipo == 'caractere':
        Node(tipo, no_pai)
    elif tipo == '(':
        Node(tipo, no_pai)

        procedimento_expre(no_pai)

        tipo, valor, linha, coluna = getToken()

        if tipo == ')':
            Node(')', no_pai)
        else:
            gera_erro_sintatico('Era esperado um )', linha, coluna,
                                'procedimento_term()',
                                f'{tipo} e {valor}')
    else:
        gera_erro_sintatico(
            'Era esperado um termo válido como: id, numero, caractere ou (', linha, coluna,
            'procedimento_term()',
            f'{tipo} e {valor}')


def procedimento_unario(raiz: Node) -> None:
    no_pai = Node('unario', raiz)

    tipo, valor, linha, coluna = getToken()

    if tipo == 'soma_sub':
        Node(tipo, no_pai)

        procedimento_term(no_pai)
    else:
        volta_token_anterior()

        procedimento_term(no_pai)


def procedimento_expre3_linha(raiz: Node) -> None:
    no_pai = Node("expre3'", raiz)

    tipo, valor, linha, coluna = getToken()

    while tipo in FIRST_DAS_TRANSICOES['expre3_linha']:
        Node(tipo, no_pai)

        procedimento_unario(no_pai)

        tipo, valor, linha, coluna = getToken()

    volta_token_anterior()


def procedimento_expre3(raiz: Node) -> None:
    no_pai = Node('expre3', raiz)

    procedimento_unario(no_pai)
    procedimento_expre3_linha(no_pai)


def procedimento_expre2_linha(raiz: Node) -> None:
    no_pai = Node("expre2'", raiz)

    tipo, valor, linha, coluna = getToken()

    while tipo in FIRST_DAS_TRANSICOES['expre2_linha']:
        Node(tipo, no_pai)

        procedimento_expre3(no_pai)

        tipo, valor, linha, coluna = getToken()

    volta_token_anterior()


def procedimento_expre2(raiz: Node) -> None:
    no_pai = Node('expre2', raiz)

    procedimento_expre3(no_pai)
    procedimento_expre2_linha(no_pai)


def procedimento_expre_linha(raiz: Node) -> None:
    no_pai = Node("expre'", raiz)

    tipo, valor, linha, coluna = getToken()

    while tipo in FIRST_DAS_TRANSICOES['expre_linha']:
        Node(tipo, no_pai)

        procedimento_expre2(no_pai)

        tipo, valor, linha, coluna = getToken()

    volta_token_anterior()


def procedimento_expre(raiz: Node) -> None:
    no_pai = Node('expre', raiz)

    procedimento_expre2(no_pai)
    procedimento_expre_linha(no_pai)


def procedimento_cond(raiz: Node) -> None:
    no_pai = Node('cond', raiz)

    procedimento_expre(no_pai)

    tipo, valor, linha, coluna = getToken()

    if tipo == 'oprel':
        Node(tipo, no_pai)

        procedimento_expre(no_pai)
    else:
        gera_erro_sintatico('Era esperado um operador relacional', linha, coluna)


def procedimento_else_cmd(raiz: Node) -> None:
    no_pai = Node('else_cmd', raiz)

    tipo, valor, linha, coluna = getToken()

    if tipo == 'else':
        procedimento_cmd_bloco(no_pai)
    else:
        volta_token_anterior()


def procedimento_cmd_rep(raiz: Node) -> None:
    no_pai = Node('cmd_rep', raiz)

    tipo, valor, linha, coluna = getToken()

    if tipo == 'while':
        Node(tipo, no_pai)

        procedimento_cond(no_pai)
        procedimento_cmd_bloco(no_pai)
    elif tipo == 'repeat':
        Node(tipo, no_pai)

        procedimento_cmd_bloco(no_pai)

        tipo, valor, linha, coluna = getToken()

        if tipo == 'until':
            Node(tipo, no_pai)

            procedimento_cond(no_pai)

            tipo, valor, linha, coluna = getToken()

            if tipo == 'pontuacao' and valor == 'PV':
                Node(';', no_pai)
            else:
                gera_erro_sintatico('Era esperado um ponto e vírgula (;)', linha, coluna)
        else:
            gera_erro_sintatico('Era esperado um until', linha, coluna)
    else:
        gera_erro_sintatico('Era esperado um while ou repeat', linha, coluna)


def procedimento_cmd_bloco(raiz: Node) -> None:
    tipo, valor, linha, coluna = getToken()

    no_pai = Node('cmd_bloco', raiz)

    if tipo == 'begin':
        volta_token_anterior()

        procedimento_bloco(no_pai)
    elif tipo in FIRST_DAS_TRANSICOES['cmd']:
        volta_token_anterior()

        procedimento_cmd(no_pai)
    else:
        gera_erro_sintatico(
            'Era esperado um comando válido', linha, coluna,
            'procedimento_cmd_bloco()', f'{tipo} e {valor}'
        )


def procedimento_cmd_cond(raiz: Node) -> None:
    no_pai = Node('cmd_cond', raiz)

    tipo, valor, linha, coluna = getToken()

    if tipo == 'if':
        Node(tipo, no_pai)

        procedimento_cond(no_pai)

        tipo, valor, linha, coluna = getToken()

        if tipo == 'then':
            Node(tipo, no_pai)

            procedimento_cmd_bloco(no_pai)
            procedimento_else_cmd(no_pai)
        else:
            gera_erro_sintatico('Era esperado um then', linha, coluna)
    else:
        gera_erro_sintatico('Era esperado um if', linha, coluna)


def procedimento_cmd_atrib(raiz: Node) -> None:
    no_pai = Node('cmd_atrib', raiz)

    tipo, valor, linha, coluna = getToken()

    if tipo == 'id':
        Node(tipo, no_pai)

        tipo, valor, linha, coluna = getToken()

        if tipo == 'atribuicao':
            Node(':=', no_pai)

            procedimento_expre(no_pai)

            tipo, valor, linha, coluna = getToken()

            if tipo == 'pontuacao' and valor == 'PV':
                Node(';', no_pai)
            else:
                gera_erro_sintatico('Era esperado ponto e vírugula (;)', linha, coluna,
                                    'procedimento_cmd_atrib()',
                                    f'{tipo} e {valor}')
        else:
            gera_erro_sintatico('Era esprado um atribuição (:=)', linha, coluna)
    else:
        gera_erro_sintatico('Era esperado um variável', linha, coluna)


def procedimento_cmd(raiz: Node) -> None:
    no_pai = Node('cmd', raiz)

    tipo, valor, linha, coluna = getToken()

    if tipo in FIRST_DAS_TRANSICOES['cmd']:
        volta_token_anterior()

        if tipo == 'id':
            procedimento_cmd_atrib(no_pai)
        elif tipo == 'if':
            procedimento_cmd_cond(no_pai)
        elif tipo == 'while' or tipo == 'repeat':
            procedimento_cmd_rep(no_pai)

        tipo, valor, linha, coluna = getToken()

    volta_token_anterior()


def procedimento_cmds_linha(raiz: Node) -> None:
    no_pai = Node("cmds'", raiz)

    tipo, valor, linha, coluna = getToken()

    if tipo in FIRST_DAS_TRANSICOES['cmds']:
        volta_token_anterior()

        procedimento_cmds(no_pai)
    else:
        volta_token_anterior()


def procedimento_cmds(raiz: Node) -> None:
    tipo, valor, linha, coluna = getToken()

    if tipo in FIRST_DAS_TRANSICOES['cmd']:
        volta_token_anterior()
        no_pai = Node('cmds', raiz)

        procedimento_cmd(no_pai)
        procedimento_cmds_linha(no_pai)
    else:
        gera_erro_sintatico('Era esperado um comando válido', linha, coluna)


def procedimento_bloco(raiz: Node) -> None:
    raiz = Node('bloco', parent=raiz)

    tipo, valor, linha, coluna = getToken()

    if tipo == 'begin':
        Node(tipo, parent=raiz)

        procedimento_variaveis(raiz)
        procedimento_cmds(raiz)

        tipo, valor, linha, coluna = getToken()

        if tipo == 'end':
            Node(tipo, raiz)
        else:
            gera_erro_sintatico(
                'Era esperado fechamento de bloco (end)', linha, coluna,
                'procedimento_bloco()', f'{tipo} e {valor}'
            )
    else:
        gera_erro_sintatico('Era esperado abertura de bloco (begin)', linha, coluna)


def procedimento_call() -> Node:
    raiz = Node('call')

    tipo, valor, linha, coluna = getToken()

    if tipo == 'program':
        Node('program', parent=raiz)

        tipo, valor, linha, coluna = getToken()

        if tipo == 'id':
            Node(tipo, parent=raiz, data=valor)

            tipo, valor, linha, coluna = getToken()

            if tipo == '(':
                Node(tipo, parent=raiz)

                tipo, valor, linha, coluna = getToken()

                if tipo == ')':
                    Node(tipo, parent=raiz)

                    procedimento_bloco(raiz)

                    return raiz
                else:
                    gera_erro_sintatico('Era esperado fechamento de parenteses', linha, coluna)
            else:
                gera_erro_sintatico('Era esperado abertura de parenteses', linha, coluna)
        else:
            gera_erro_sintatico('Era esperado um nome para o program', linha, coluna)
    else:
        gera_erro_sintatico('Era esperado a palavra reservada program', linha, coluna)


def main(imprimir: bool = True, escrever_arvore_no_txt: bool = False, nome_do_arq: str = None) -> (float, [str]):
    inicio = time()

    raiz = procedimento_call()

    demorou = time() - inicio

    if escrever_arvore_no_txt:
        if nome_do_arq is not None:
            nome_base, extensao = os.path.splitext(nome_do_arq)

            if extensao.lower() == '.txt':
                with open(nome_do_arq, 'w', encoding='utf-8') as arq:
                    for pre, _, node in RenderTree(raiz):
                        arq.writelines(f'{pre}{node.name}\n')
            else:
                print('Erro: Precisa ser um arquivo com final .txt')
        else:
            print('Erro: Nome inválido')

    if imprimir:
        print('Código aceito')
        print(f'Demorou: {demorou}')

        print('Árvore de derivação:')
        print()
        for pre, _, node in RenderTree(raiz):
            print(f'{pre}{node.name}')
    else:
        arvore = []

        for pre, _, node in RenderTree(raiz):
            arvore.append(f'{pre}{node.name}')

        return demorou, arvore


if __name__ == '__main__':
    abre_arquivo('testes/teste02.txt')

    main()

    fecha_arquivo()
