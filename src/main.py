import sintatico as sint
from lexico import abre_arquivo, fecha_arquivo

if __name__ == '__main__':
    abre_arquivo('testes/teste02.txt')

    sint.procedimento_call()
    # sint.procedimento_lista_ids_linha()

    fecha_arquivo()
