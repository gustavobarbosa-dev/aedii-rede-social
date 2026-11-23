# Grafo da rede social com lista de adjacencia.
# Os vertices sao os ids dos usuarios, entao uso o proprio id como indice da lista.


class Grafo:
    """Grafo dirigido: uma aresta a -> b quer dizer que a segue b.

    Guardo duas listas de adjacencia: quem cada um segue e quem segue cada um.
    A segunda ajuda a contar seguidores e a fazer a BFS sem direcao.
    """

    def __init__(self, n):
        """Cria o grafo para ids de 1 ate n (a posicao 0 nao e usada)."""
        self.n = n
        self.seguindo = []
        self.seguidores = []
        for i in range(n + 1):
            self.seguindo.append([])
            self.seguidores.append([])

    def adicionar_aresta(self, a, b):
        """a passa a seguir b. O(1)."""
        self.seguindo[a].append(b)
        self.seguidores[b].append(a)

    def qtd_seguindo(self, v):
        return len(self.seguindo[v])

    def qtd_seguidores(self, v):
        return len(self.seguidores[v])

    def amigos_de_amigos(self, u):
        """Candidatos a distancia 2 de u e quantas conexoes em comum cada um tem.

        Devolve lista de [id_candidato, em_comum]. Fica de fora o proprio u
        e quem u ja segue. O(soma dos graus de quem u segue).
        """
        # marca quem u ja segue pra nao sugerir de novo
        ja_segue = [False] * (self.n + 1)
        for v in self.seguindo[u]:
            ja_segue[v] = True

        em_comum = [0] * (self.n + 1)
        candidatos = []
        for amigo in self.seguindo[u]:
            for c in self.seguindo[amigo]:
                if c == u or ja_segue[c]:
                    continue
                if em_comum[c] == 0:
                    candidatos.append(c)  # primeira vez que aparece
                em_comum[c] += 1  # mais um amigo de u que segue c

        resultado = []
        for c in candidatos:
            resultado.append([c, em_comum[c]])
        return resultado

    def componentes(self):
        """Acha os componentes conexos com BFS, ignorando a direcao das arestas.

        Devolve uma lista com o tamanho de cada componente. O(V + E).
        """
        visitado = [False] * (self.n + 1)
        tamanhos = []
        for inicio in range(1, self.n + 1):
            if visitado[inicio]:
                continue
            # BFS: a lista funciona como fila, 'frente' aponta quem sai
            fila = [inicio]
            visitado[inicio] = True
            frente = 0
            while frente < len(fila):
                v = fila[frente]
                frente += 1
                # vizinhos nas duas direcoes (quem v segue e quem segue v)
                for w in self.seguindo[v]:
                    if not visitado[w]:
                        visitado[w] = True
                        fila.append(w)
                # TODO: da pra juntar esses dois for numa funcao, deixei assim por enquanto
                for w in self.seguidores[v]:
                    if not visitado[w]:
                        visitado[w] = True
                        fila.append(w)
            tamanhos.append(len(fila))
        return tamanhos
