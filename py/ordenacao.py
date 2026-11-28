# Merge Sort feito na mao (nao pode usar sorted nem list.sort)


def merge_sort(lista, vem_antes):
    """Ordena a lista com Merge Sort e devolve uma lista nova. O(n log n).

    vem_antes(a, b) retorna True se 'a' tem que aparecer antes de 'b'.
    """
    if len(lista) <= 1:
        return lista
    meio = len(lista) // 2
    esquerda = merge_sort(lista[:meio], vem_antes)
    direita = merge_sort(lista[meio:], vem_antes)
    return intercalar(esquerda, direita, vem_antes)


def intercalar(esquerda, direita, vem_antes):
    """Junta duas listas ja ordenadas em uma so, tambem ordenada. O(n)."""
    resultado = []
    i = 0
    j = 0
    while i < len(esquerda) and j < len(direita):
        # o 'not' deixa o merge estavel: no empate pega o da esquerda
        if not vem_antes(direita[j], esquerda[i]):
            resultado.append(esquerda[i])
            i += 1
        else:
            resultado.append(direita[j])
            j += 1
    # sobrou alguma coisa em uma das duas
    while i < len(esquerda):
        resultado.append(esquerda[i])
        i += 1
    while j < len(direita):
        resultado.append(direita[j])
        j += 1
    return resultado
