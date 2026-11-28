# Heap binaria guardada num vetor (lista do python).
# Para o no na posicao i: pai = (i-1)//2, filho esq = 2i+1, filho dir = 2i+2


class Heap:
    """Heap binaria generica.

    Quem fica no topo e decidido pela funcao vem_antes(a, b), que retorna
    True se 'a' tem que ficar acima de 'b'. No projeto eu passo uma funcao
    que compara "quem e maior", entao funciona como heap de maximo.
    """

    def __init__(self, vem_antes):
        """Cria a heap vazia. vem_antes e a funcao de comparacao."""
        self.dados = []
        self.vem_antes = vem_antes

    def tamanho(self):
        """Quantidade de elementos na heap."""
        return len(self.dados)

    def vazia(self):
        """True se nao tem nenhum elemento."""
        return len(self.dados) == 0

    def inserir(self, item):
        """Coloca o item no final e sobe ele ate o lugar certo. O(log n)."""
        self.dados.append(item)
        self.subir(len(self.dados) - 1)

    def remover_topo(self):
        """Tira e devolve o elemento do topo (o maior). O(log n).

        O ultimo elemento vai pro lugar do topo e depois desce.
        """
        if len(self.dados) == 0:
            return None
        topo = self.dados[0]
        ultimo = self.dados.pop()
        if len(self.dados) > 0:
            self.dados[0] = ultimo
            self.descer(0)
        return topo

    def subir(self, i):
        """Sift-up: enquanto o item for 'maior' que o pai, troca com o pai."""
        while i > 0:
            pai = (i - 1) // 2
            if self.vem_antes(self.dados[i], self.dados[pai]):
                aux = self.dados[i]
                self.dados[i] = self.dados[pai]
                self.dados[pai] = aux
                i = pai
            else:
                break  # ja ta no lugar certo

    def descer(self, i):
        """Sift-down: troca o item com o maior dos filhos ate nenhum filho ser maior."""
        n = len(self.dados)
        while True:
            esq = 2 * i + 1
            dir = 2 * i + 2
            melhor = i
            if esq < n and self.vem_antes(self.dados[esq], self.dados[melhor]):
                melhor = esq
            if dir < n and self.vem_antes(self.dados[dir], self.dados[melhor]):
                melhor = dir
            if melhor == i:
                break  # os dois filhos sao menores, parou
            aux = self.dados[i]
            self.dados[i] = self.dados[melhor]
            self.dados[melhor] = aux
            i = melhor
