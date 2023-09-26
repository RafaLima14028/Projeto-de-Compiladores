# Paramentros de retorno: (tipo, valor, se_faz_overhead)
def return_oprel_ge() -> (str, str, bool):
    return 'oprel', 'GE', False


def return_oprel_eq() -> (str, str, bool):
    return 'oprel', 'EQ', False


def return_oprel_gt() -> (str, str, bool):
    return 'oprel', 'GT', True


def return_oprel_le() -> (str, str, bool):
    return 'oprel', 'LE', False


def return_oprel_lt() -> (str, str, bool):
    return 'oprel', 'LT', True


estados_finais = [
    -1, 2, 4, 5, 7, 8, 10, 11, 12, 13, 14, 15,
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
    2: return_oprel_eq,
    3: {
        '=': 4,
        'outros': 5
    },
    4: return_oprel_ge,
    5: return_oprel_gt,
    6: {
        '=': 7,
        'outros': 8
    },
    7: return_oprel_le,
    8: return_oprel_lt
}
