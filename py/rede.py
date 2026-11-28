# Aqui fica a "regra de negocio": monta as estruturas com os dados
# e tem um metodo pra cada comando. Nao imprime nada, quem imprime e o main.
import aedlib
from tabela_hash import TabelaHash
from grafo import Grafo
from heap import Heap
from avl import ArvoreAVL
from ordenacao import merge_sort


def data_valida(texto):
    """Confere se o texto esta no formato AAAA-MM-DD (com mes e dia que fazem sentido)."""
    if len(texto) != 10 or texto[4] != "-" or texto[7] != "-":
        return False
    ano = texto[0:4]
    mes = texto[5:7]
    dia = texto[8:10]
    if not (ano.isdigit() and mes.isdigit() and dia.isdigit()):
        return False
    if int(mes) < 1 or int(mes) > 12:
        return False
    if int(dia) < 1 or int(dia) > 31:
        return False
    return True


class RedeSocial:
    """Junta todas as estruturas da rede social e responde os comandos."""

    def __init__(self):
        """Le os CSVs e monta: tabela hash, grafo, AVL e os contadores por usuario."""
        usuarios, seguidores, posts = aedlib.social_carregar_dados()

        # descobre o maior id pra saber o tamanho das listas
        maior_id = 0
        for u in usuarios:
            if int(u[0]) > maior_id:
                maior_id = int(u[0])
        self.maior_id = maior_id

        # usuarios[id] = [id, @usuario, nome, data_cadastro]
        self.usuarios = [None] * (maior_id + 1)
        self.tabela = TabelaHash()
        for u in usuarios:
            id_usuario = int(u[0])
            self.usuarios[id_usuario] = u
            self.tabela.inserir(u[1], id_usuario)

        self.grafo = Grafo(maior_id)
        for s in seguidores:
            self.grafo.adicionar_aresta(int(s[0]), int(s[1]))

        # cada post vira [id, autor, data, curtidas, texto] ja com os numeros convertidos
        self.posts = []
        self.qtd_posts = [0] * (maior_id + 1)
        self.soma_curtidas = [0] * (maior_id + 1)
        self.arvore = ArvoreAVL()
        for p in posts:
            post = [int(p[0]), int(p[1]), p[2], int(p[3]), p[4]]
            self.posts.append(post)
            self.qtd_posts[post[1]] += 1
            self.soma_curtidas[post[1]] += post[3]
            self.arvore.inserir(post[2], post)

    def achar_id(self, usuario):
        """Devolve o id do @usuario pela tabela hash, ou None."""
        return self.tabela.buscar(usuario)

    def arroba(self, id_usuario):
        return self.usuarios[id_usuario][1]

    # ---------- 3.1 BUSCAR ----------
    def buscar(self, usuario):
        """Dados do usuario: [@usuario, nome, cadastro, segue, seguidores, posts]. None se nao existe."""
        id_usuario = self.achar_id(usuario)
        if id_usuario is None:
            return None
        u = self.usuarios[id_usuario]
        return [u[1], u[2], u[3],
                self.grafo.qtd_seguindo(id_usuario),
                self.grafo.qtd_seguidores(id_usuario),
                self.qtd_posts[id_usuario]]

    # ---------- 3.2 SUGERIR ----------
    def sugerir(self, usuario, k):
        """Ate k sugestoes de amigos de amigos: lista de [@usuario, nome, em_comum].

        Usa heap de maximo pelo numero de conexoes em comum
        (no empate, ordem alfabetica do @usuario).
        """
        id_usuario = self.achar_id(usuario)
        if id_usuario is None:
            return None
        candidatos = self.grafo.amigos_de_amigos(id_usuario)

        def vem_antes(a, b):
            if a[1] != b[1]:
                return a[1] > b[1]
            return self.arroba(a[0]) < self.arroba(b[0])

        heap = Heap(vem_antes)
        for c in candidatos:
            heap.inserir(c)

        resultado = []
        while len(resultado) < k and not heap.vazia():
            c = heap.remover_topo()
            resultado.append([self.arroba(c[0]), self.usuarios[c[0]][2], c[1]])
        return resultado

    # ---------- 3.3 COMUNIDADES ----------
    def comunidades(self):
        """Devolve [tamanhos das comunidades do maior pro menor, quantidade de isolados].

        Usuario isolado e quem nao segue ninguem e nao e seguido por ninguem,
        ou seja, ficou num componente de tamanho 1. Esses eu conto separado.
        """
        tamanhos = self.grafo.componentes()
        comunidades = []
        isolados = 0
        for t in tamanhos:
            if t == 1:
                isolados += 1
            else:
                comunidades.append(t)
        comunidades = merge_sort(comunidades, lambda a, b: a > b)
        return [comunidades, isolados]
