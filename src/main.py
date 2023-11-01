import sintatico as sint
from lexico import abre_arquivo, fecha_arquivo

if __name__ == '__main__':
    abre_arquivo('testes/teste02.txt')

    t, arv = sint.main(
        imprimir=False,
        escrever_arvore_no_txt=True,
        nome_do_arq='testes/arvore_de_derivacao.txt'
    )

    if t is not None:
        print(f'Demorou: {t} segundos')

        for a in arv:
            print(a)

    fecha_arquivo()
