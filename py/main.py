"""
Atividade Final - AED II - Rede Social
API de consulta por linha de comando.

Exemplo: python py/main.py buscar @henrique_nascimento
         python py/main.py ajuda
"""
import sys
import json
import aedlib  # biblioteca base do projeto (obrigatoria - nao remova)
from rede import RedeSocial, data_valida

AJUDA = """Comandos:
  buscar @usuario                  dados do usuario
  sugerir @usuario k               ate k sugestoes de quem seguir
  comunidades                      comunidades (componentes conexos) e isolados
  posts-entre DATA1 DATA2          posts entre duas datas (AAAA-MM-DD)
  top-seguidos k                   k usuarios com mais seguidores
  top-curtidos k                   k posts com mais curtidas
  ranking [--limite N] [--usuario @x]  ranking de engajamento (padrao: 20 primeiros)
  ajuda                            mostra esta ajuda

Opcao --json em qualquer comando: mostra a saida em JSON.

Exemplos:
  python py/main.py buscar @henrique_nascimento
  python py/main.py sugerir @henrique_nascimento 5 --json
  python py/main.py posts-entre 2025-03-01 2025-03-31
  python py/main.py ranking --limite 10"""


# ---------- funcoes pra montar o JSON sem usar dict ----------
# (dict e proibido, entao monto o texto na mao. json.dumps so pra texto/numero)

def valor_json(v):
    return json.dumps(v)


def objeto_json(pares):
    """pares = lista de [chave, valor_ja_em_json]. Devolve o texto do objeto."""
    partes = []
    for p in pares:
        partes.append(json.dumps(p[0]) + ": " + p[1])
    return "{" + ", ".join(partes) + "}"


def lista_json(itens):
    """itens = lista de textos ja em json."""
    return "[" + ", ".join(itens) + "]"


# ---------- erros ----------

def erro(msg, modo_json):
    """Mostra a mensagem de erro e sai com codigo 1."""
    if modo_json:
        print(objeto_json([["erro", valor_json(msg)]]))
    else:
        print("Erro: " + msg)
    sys.exit(1)


def ler_k(texto, modo_json):
    """Converte o k pra inteiro positivo, senao da erro."""
    if not texto.isdigit() or int(texto) <= 0:
        erro("k deve ser um numero inteiro maior que zero (recebido: '" + texto + "')", modo_json)
    return int(texto)


def conferir_args(args, qtd, uso, modo_json):
    if len(args) < qtd:
        erro("parametros faltando. Uso: " + uso, modo_json)


# ---------- comandos ----------

def cmd_buscar(rede, args, modo_json):
    conferir_args(args, 1, "buscar @usuario", modo_json)
    dados = rede.buscar(args[0])
    if dados is None:
        erro("usuario " + args[0] + " nao encontrado", modo_json)
    if modo_json:
        print(objeto_json([["usuario", valor_json(dados[0])],
                           ["nome", valor_json(dados[1])],
                           ["data_cadastro", valor_json(dados[2])],
                           ["seguindo", valor_json(dados[3])],
                           ["seguidores", valor_json(dados[4])],
                           ["posts", valor_json(dados[5])]]))
    else:
        print("Usuario:       " + dados[0])
        print("Nome:          " + dados[1])
        print("Cadastro:      " + dados[2])
        print("Seguindo:      " + str(dados[3]))
        print("Seguidores:    " + str(dados[4]))
        print("Posts:         " + str(dados[5]))


def cmd_sugerir(rede, args, modo_json):
    conferir_args(args, 2, "sugerir @usuario k", modo_json)
    k = ler_k(args[1], modo_json)
    sugestoes = rede.sugerir(args[0], k)
    if sugestoes is None:
        erro("usuario " + args[0] + " nao encontrado", modo_json)
    if modo_json:
        itens = []
        for s in sugestoes:
            itens.append(objeto_json([["usuario", valor_json(s[0])],
                                      ["nome", valor_json(s[1])],
                                      ["em_comum", valor_json(s[2])]]))
        print(lista_json(itens))
        return
    if len(sugestoes) == 0:
        print("Nenhuma sugestao para " + args[0] + ".")
        return
    if len(sugestoes) < k:
        print("So tem " + str(len(sugestoes)) + " candidatos, mostrando todos.")
    pos = 1
    for s in sugestoes:
        print(str(pos) + ". " + s[0] + " (" + s[1] + ") - " + str(s[2]) + " em comum")
        pos += 1


def cmd_comunidades(rede, args, modo_json):
    resultado = rede.comunidades()
    comunidades = resultado[0]
    isolados = resultado[1]
    if modo_json:
        tamanhos = []
        for t in comunidades:
            tamanhos.append(valor_json(t))
        print(objeto_json([["total_comunidades", valor_json(len(comunidades))],
                           ["tamanhos", lista_json(tamanhos)],
                           ["isolados", valor_json(isolados)]]))
    else:
        print("Comunidades encontradas: " + str(len(comunidades)))
        i = 1
        for t in comunidades:
            print("  Comunidade " + str(i) + ": " + str(t) + " usuarios")
            i += 1
        print("Usuarios isolados: " + str(isolados))


def cmd_posts_entre(rede, args, modo_json):
    conferir_args(args, 2, "posts-entre AAAA-MM-DD AAAA-MM-DD", modo_json)
    d1 = args[0]
    d2 = args[1]
    if not data_valida(d1):
        erro("data invalida: '" + d1 + "' (use AAAA-MM-DD)", modo_json)
    if not data_valida(d2):
        erro("data invalida: '" + d2 + "' (use AAAA-MM-DD)", modo_json)
    if d1 > d2:
        erro("a primeira data e maior que a segunda (" + d1 + " > " + d2 + ")", modo_json)
    posts = rede.posts_entre(d1, d2)
    if modo_json:
        itens = []
        for p in posts:
            itens.append(objeto_json([["id", valor_json(p[0])],
                                      ["autor", valor_json(rede.arroba(p[1]))],
                                      ["data", valor_json(p[2])],
                                      ["curtidas", valor_json(p[3])],
                                      ["texto", valor_json(p[4])]]))
        print(objeto_json([["quantidade", valor_json(len(posts))],
                           ["posts", lista_json(itens)]]))
    else:
        for p in posts:
            print(p[2] + " | " + rede.arroba(p[1]) + " | " + str(p[3]) + " curtidas | " + p[4])
        print("Posts encontrados: " + str(len(posts)))


def cmd_top_seguidos(rede, args, modo_json):
    conferir_args(args, 1, "top-seguidos k", modo_json)
    k = ler_k(args[0], modo_json)
    top = rede.top_seguidos(k)
    if modo_json:
        itens = []
        for t in top:
            itens.append(objeto_json([["usuario", valor_json(t[0])],
                                      ["nome", valor_json(t[1])],
                                      ["seguidores", valor_json(t[2])]]))
        print(lista_json(itens))
    else:
        pos = 1
        for t in top:
            print(str(pos) + ". " + t[0] + " (" + t[1] + ") - " + str(t[2]) + " seguidores")
            pos += 1


def cmd_top_curtidos(rede, args, modo_json):
    conferir_args(args, 1, "top-curtidos k", modo_json)
    k = ler_k(args[0], modo_json)
    top = rede.top_curtidos(k)
    if modo_json:
        itens = []
        for p in top:
            itens.append(objeto_json([["id", valor_json(p[0])],
                                      ["autor", valor_json(p[1])],
                                      ["data", valor_json(p[2])],
                                      ["curtidas", valor_json(p[3])],
                                      ["texto", valor_json(p[4])]]))
        print(lista_json(itens))
    else:
        pos = 1
        for p in top:
            print(str(pos) + ". " + str(p[3]) + " curtidas | " + p[1] + " | " + p[2] + " | " + p[4])
            pos += 1


def cmd_ranking(rede, args, modo_json):
    limite = 20
    usuario = None
    i = 0
    while i < len(args):
        if args[i] == "--limite" and i + 1 < len(args):
            limite = ler_k(args[i + 1], modo_json)
            i += 2
        elif args[i] == "--usuario" and i + 1 < len(args):
            usuario = args[i + 1]
            i += 2
        else:
            erro("parametro invalido no ranking: '" + args[i] + "'", modo_json)

    lista = rede.ranking()

    # posicao do usuario informado (busca linear, a lista ja ta ordenada)
    posicao = None
    if usuario is not None:
        if rede.achar_id(usuario) is None:
            erro("usuario " + usuario + " nao encontrado", modo_json)
        if not usuario.startswith("@"):
            usuario = "@" + usuario
        for j in range(len(lista)):
            if lista[j][0] == usuario:
                posicao = j + 1
                break

    if modo_json:
        itens = []
        for j in range(min(limite, len(lista))):
            r = lista[j]
            itens.append(objeto_json([["posicao", valor_json(j + 1)],
                                      ["usuario", valor_json(r[0])],
                                      ["engajamento", valor_json(r[1])],
                                      ["seguidores", valor_json(r[2])],
                                      ["curtidas", valor_json(r[3])]]))
        pares = [["ranking", lista_json(itens)]]
        if posicao is not None:
            pares.append(["posicao_usuario", objeto_json([["usuario", valor_json(usuario)],
                                                           ["posicao", valor_json(posicao)]])])
        print(objeto_json(pares))
    else:
        for j in range(min(limite, len(lista))):
            r = lista[j]
            print(str(j + 1) + ". " + r[0] + " - engajamento " + str(r[1])
                  + " (" + str(r[2]) + " seguidores, " + str(r[3]) + " curtidas)")
        if posicao is not None:
            print("Posicao de " + usuario + ": " + str(posicao) + " de " + str(len(lista)))


def main():
    args = sys.argv[1:]

    # tira o --json da lista e guarda se ele apareceu
    modo_json = False
    resto = []
    for a in args:
        if a == "--json":
            modo_json = True
        else:
            resto.append(a)

    if len(resto) == 0 or resto[0] == "ajuda":
        print(AJUDA)
        return

    comando = resto[0].lower()
    parametros = resto[1:]

    # confere o comando antes de carregar tudo (carregar demora um pouco)
    comandos = ["buscar", "sugerir", "comunidades", "posts-entre",
                "top-seguidos", "top-curtidos", "ranking"]
    if comando not in comandos:
        print("Comando invalido: " + resto[0] + "\n")
        print(AJUDA)
        sys.exit(1)

    rede = RedeSocial()

    if comando == "buscar":
        cmd_buscar(rede, parametros, modo_json)
    elif comando == "sugerir":
        cmd_sugerir(rede, parametros, modo_json)
    elif comando == "comunidades":
        cmd_comunidades(rede, parametros, modo_json)
    elif comando == "posts-entre":
        cmd_posts_entre(rede, parametros, modo_json)
    elif comando == "top-seguidos":
        cmd_top_seguidos(rede, parametros, modo_json)
    elif comando == "top-curtidos":
        cmd_top_curtidos(rede, parametros, modo_json)
    elif comando == "ranking":
        cmd_ranking(rede, parametros, modo_json)


if __name__ == "__main__":
    main()
