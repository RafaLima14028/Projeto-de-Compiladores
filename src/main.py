import sintatico as sint
from lexico import abre_arquivo, fecha_arquivo

if __name__ == '__main__':
    abre_arquivo('testes/teste01.txt')

    sint.procedimento_expre_linha()

    fecha_arquivo()
