# Arvore AVL indexada pela data do post (texto AAAA-MM-DD).
# Comparar as datas como texto funciona porque o formato vai do ano pro dia.


class NoAVL:
    """No da arvore AVL. Guarda uma data e todos os posts dessa data."""

    def __init__(self, data, post):
        self.data = data
        self.posts = [post]  # varios posts podem ter a mesma data
        self.esquerda = None
        self.direita = None
        self.altura = 1


class ArvoreAVL:
    """Arvore AVL (arvore de busca balanceada) com os posts indexados por data."""

    def __init__(self):
        self.raiz = None
        self.qtd_nos = 0

    def altura(self, no):
        """Altura do no (None tem altura 0)."""
        if no is None:
            return 0
        return no.altura

    def atualizar_altura(self, no):
        """Recalcula a altura a partir dos filhos."""
        no.altura = 1 + max(self.altura(no.esquerda), self.altura(no.direita))

    def fator_balanceamento(self, no):
        """Altura da esquerda menos altura da direita. Na AVL tem que ficar entre -1 e 1."""
        return self.altura(no.esquerda) - self.altura(no.direita)

    def rotacao_direita(self, y):
        """Rotacao simples a direita. Usada quando a esquerda ficou pesada.

               y              x
              / \\            / \\
             x   C    =>    A   y
            / \\                / \\
           A   B              B   C
        """
        x = y.esquerda
        b = x.direita
        x.direita = y
        y.esquerda = b
        # y agora ta embaixo de x, entao atualiza y primeiro
        self.atualizar_altura(y)
        self.atualizar_altura(x)
        return x  # x e a nova raiz dessa subarvore

    def rotacao_esquerda(self, x):
        """Rotacao simples a esquerda (espelho da rotacao a direita).

             x                  y
            / \\                / \\
           A   y      =>      x   C
              / \\            / \\
             B   C          A   B
        """
        y = x.direita
        b = y.esquerda
        y.esquerda = x
        x.direita = b
        self.atualizar_altura(x)
        self.atualizar_altura(y)
        return y

    def inserir(self, data, post):
        """Insere um post na arvore pela data. O(log n)."""
        self.raiz = self._inserir(self.raiz, data, post)

    def _inserir(self, no, data, post):
        # insercao normal de arvore de busca
        if no is None:
            self.qtd_nos += 1
            return NoAVL(data, post)
        if data < no.data:
            no.esquerda = self._inserir(no.esquerda, data, post)
        elif data > no.data:
            no.direita = self._inserir(no.direita, data, post)
        else:
            # data repetida: nao cria no novo, so adiciona o post na lista
            no.posts.append(post)
            return no

        # na volta da recursao confere se desbalanceou
        self.atualizar_altura(no)
        fb = self.fator_balanceamento(no)

        # caso esquerda-esquerda
        if fb > 1 and data < no.esquerda.data:
            return self.rotacao_direita(no)
        # caso direita-direita
        if fb < -1 and data > no.direita.data:
            return self.rotacao_esquerda(no)
        # caso esquerda-direita: primeiro gira o filho pra virar esquerda-esquerda
        if fb > 1 and data > no.esquerda.data:
            no.esquerda = self.rotacao_esquerda(no.esquerda)
            return self.rotacao_direita(no)
        # caso direita-esquerda
        if fb < -1 and data < no.direita.data:
            no.direita = self.rotacao_direita(no.direita)
            return self.rotacao_esquerda(no)

        return no

    def buscar_intervalo(self, inicio, fim):
        """Devolve os posts com inicio <= data <= fim, em ordem de data.

        Nao percorre a arvore toda: so entra nos ramos que podem ter
        datas do intervalo. O(log n + m), m = quantidade de nos achados.
        """
        resultado = []
        self._intervalo(self.raiz, inicio, fim, resultado)
        return resultado

    def _intervalo(self, no, inicio, fim, resultado):
        if no is None:
            return
        # a esquerda so tem datas menores, entao so vale descer
        # se a data do no ainda for maior que o inicio
        if inicio < no.data:
            self._intervalo(no.esquerda, inicio, fim, resultado)
        # visita o no no meio (em ordem), por isso o resultado sai ordenado
        if inicio <= no.data <= fim:
            for p in no.posts:
                resultado.append(p)
        # mesma ideia pra direita
        if no.data < fim:
            self._intervalo(no.direita, inicio, fim, resultado)
