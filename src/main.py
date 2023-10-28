import sintatico as sint
from lexico import abre_arquivo, fecha_arquivo
from time import time

# from treelib import Tree

if __name__ == '__main__':
    inicio = time()

    abre_arquivo('testes/teste02.txt')

    sint.procedimento_call()

    fecha_arquivo()

    print(f'Demorou: {time() - inicio}')

    # tree = Tree()
    # tree.create_node('Raiz', "root")
    # tree.create_node("Filho 1", "child1", parent="root")
    # tree.create_node("Filho 2", "child2", parent="root")
    # tree.create_node("Neto", "grandchild", parent="child1")
    #
    # for node in tree.expand_tree(mode=Tree.WIDTH):
    #     print(node)
    #
    # print()
    # print(tree.show(stdout=False))
