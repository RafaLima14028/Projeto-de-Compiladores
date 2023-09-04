arquivo = None


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


def lookhead() -> None:
    arquivo.seek(arquivo.tell() - 1, 0)


# Retorna um token por vez
def getToken():
    ...


if __name__ == '__main__':
    abre_arquivo('testes/teste01.txt')

    arquivo.close()
