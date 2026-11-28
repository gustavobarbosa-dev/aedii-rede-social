########## GUSTAVO DUTRA LUIZ BARBOSA ##########

Linguagem escolhida: Python

## 1. O que foi feito

Todas as funcionalidades do enunciado foram implementadas e estão funcionando:

- 3.1 BUSCAR (tabela hash)
- 3.2 SUGERIR (grafo + heap)
- 3.3 COMUNIDADES (BFS no grafo)
- 3.4 POSTS_ENTRE (árvore AVL com consulta por intervalo)
- 3.5 TOP_SEGUIDOS e TOP_CURTIDOS (heap)
- 3.6 RANKING (merge sort)
- 3.7 Bônus: a API por linha de comando, com ajuda, opção --json e código de saída 1 quando dá erro

Não ficou nada incompleto. Não usei dict, set, sorted, .sort(), heapq nem nenhuma outra estrutura proibida. O único import da biblioteca padrão fora o sys é o json, que uso só pra escrever texto e número no formato JSON (explico na parte da API).

## 2. Como foi feito

O código fica todo na pasta `py/`. Separei cada estrutura num arquivo:

| Arquivo | O que tem |
|---|---|
| `tabela_hash.py` | classe `TabelaHash` (hash com encadeamento) |
| `grafo.py` | classe `Grafo` (lista de adjacência, amigos de amigos e BFS) |
| `heap.py` | classe `Heap` (heap binária num vetor) |
| `avl.py` | classes `NoAVL` e `ArvoreAVL` (com as rotações e a busca por intervalo) |
| `ordenacao.py` | função `merge_sort` |
| `rede.py` | classe `RedeSocial`, que lê os dados, monta as estruturas e tem um método pra cada comando |
| `main.py` | a interface: lê os argumentos, chama a `RedeSocial` e imprime o resultado (texto ou JSON) |
| `aedlib.py` | a leitura dos CSV que veio pronta do professor, não mexi |

A ideia foi deixar as estruturas sem saber nada da rede social (a heap e o merge sort recebem uma função de comparação, então servem pra qualquer coisa). A `RedeSocial` é quem junta tudo e devolve listas com os resultados, sem imprimir nada. Quem imprime é só o `main.py`. Assim, quando fiz a API, não precisei mexer nas estruturas, só no main.

Como os ids dos usuários vão de 1 a 2000, usei o próprio id como índice das listas (`usuarios[id]`, `seguindo[id]`, `qtd_posts[id]` etc.). Isso substitui o dict nos lugares onde a chave é um número. A tabela hash ficou só pra buscar pelo @usuario, que é texto.

## 3. Escolhas e por quê

**Tabela hash.** Usei hash polinomial: pra cada letra faço `h = (h * 31 + ord(letra)) % tamanho`. É a mesma ideia do hashCode de String do Java. Escolhi essa porque soma simples dos códigos das letras daria o mesmo valor pra anagramas (@ana e @naa), e com a multiplicação a posição da letra conta. As colisões são tratadas por encadeamento: cada posição do vetor é uma lista de pares [chave, valor]. O tamanho da tabela é 4099, que é primo e fica perto do dobro da quantidade de usuários (fator de carga mais ou menos 0,5). Conferi com o método `maior_balde()` e a maior lista de colisão ficou com 4 elementos, então a busca continua praticamente O(1).

**Grafo.** Representei com lista de adjacência porque são 2000 usuários e 15000 conexões. Uma matriz teria 4 milhões de posições, quase todas vazias. Guardo duas listas: `seguindo[v]` (quem v segue) e `seguidores[v]` (quem segue v). A segunda deixa contar seguidores só com `len` e permite andar nas duas direções na BFS das comunidades, que tem que tratar o grafo como não dirigido.

**Comunidades.** Usei BFS. A fila é uma lista normal com um índice `frente` apontando quem sai, porque `pop(0)` em lista do Python é O(n). Componente de tamanho 1 é usuário que não segue e não é seguido por ninguém, e esses eu conto como isolados, separados da lista de comunidades.

**AVL e não lista ordenada.** Com uma lista ordenada a busca por data seria O(log n) com busca binária, mas cada inserção ia ter que empurrar os elementos pro lado, O(n), e com 20000 posts isso pesa. Na AVL a inserção e a busca são O(log n), e ela continua balanceada sozinha pelas rotações. Como muitas datas se repetem, cada nó guarda uma data e a lista de posts daquela data. Assim a árvore ficou com 669 nós e altura 11. A data é comparada como texto, o que funciona porque o formato AAAA-MM-DD vai do ano pro dia. Na consulta por intervalo, só desço pra esquerda se a data do nó for maior que o início, e só desço pra direita se for menor que o fim. Como visito em ordem (esquerda, nó, direita), os posts já saem em ordem cronológica.

**Heap de máximo.** Fiz uma heap só, que recebe uma função `vem_antes(a, b)`. Passando "a é maior que b", ela vira heap de máximo. Pro top-k eu coloco todos os candidatos na heap e tiro o topo k vezes. Escolhi máximo porque o resultado já sai na ordem certa (do maior pro menor), sem precisar inverter depois. Daria pra fazer com uma heap de mínimo de tamanho k, que seria um pouco mais rápida (O(n log k)), mas com esse volume de dados a diferença não aparece e a de máximo ficou mais simples de entender. Nos empates, o SUGERIR e o TOP_SEGUIDOS usam ordem alfabética do @usuario, e o TOP_CURTIDOS usa o post de menor id.

**Merge Sort.** Escolhi porque é O(n log n) sempre, até no pior caso (o Quick Sort pode cair pra O(n²)). Também é estável, e eu deixei estável de propósito: no empate ele pega o elemento da esquerda. A comparação do ranking é engajamento maior primeiro e, se empatar, @usuario em ordem alfabética.

## 4. Complexidade

n = usuários (2000), m = conexões (15000), p = posts (20000), d = datas diferentes (669).

| Comando | Complexidade | Por quê |
|---|---|---|
| BUSCAR | O(1) em média | uma busca na hash, e as contagens já ficam guardadas por id |
| SUGERIR | O(S + c log c) | S = soma de quantos cada amigo segue, c = candidatos. Monta os candidatos e insere todos na heap |
| COMUNIDADES | O(n + m) | a BFS passa uma vez por cada usuário e por cada aresta (mais o merge sort dos tamanhos, que é pequeno) |
| POSTS_ENTRE | O(log d + r) | desce só pelos ramos do intervalo. r = posts encontrados |
| TOP_SEGUIDOS | O(n log n) | insere os n usuários na heap e tira k (k ≤ n) |
| TOP_CURTIDOS | O(p log p) | mesma coisa com os posts |
| RANKING | O(n log n) | calcula o engajamento em O(n) e ordena com merge sort |

A montagem das estruturas, que acontece toda vez que o programa roda, é O(n + m + p log d) por causa das inserções na AVL. Na minha máquina cada comando roda em menos de meio segundo.

## 5. Testes feitos

Rodei tudo pelo terminal. Algumas saídas eu cortei porque eram muito grandes.

**Busca normal e usuário inexistente:**
```
$ python py/main.py buscar @henrique_nascimento
Usuario:       @henrique_nascimento
Nome:          Henrique Nascimento
Cadastro:      2022-10-26
Seguindo:      10
Seguidores:    12
Posts:         8

$ python py/main.py buscar @naoexiste
Erro: usuario @naoexiste nao encontrado
```

**Sugestões, k maior que o número de candidatos e usuário isolado:**
```
$ python py/main.py sugerir @henrique_nascimento 3
1. @andre_martins2 (André Martins) - 2 em comum
2. @beatriz_moreira3 (Beatriz Moreira) - 2 em comum
3. @eduarda_rocha5 (Eduarda Rocha) - 2 em comum

$ python py/main.py sugerir @mariana_ferreira 10
So tem 2 candidatos, mostrando todos.
1. @camila_barbosa2 (Camila Barbosa) - 2 em comum
2. @isabela_rodrigues4 (Isabela Rodrigues) - 1 em comum

$ python py/main.py sugerir @mariana_gomes 5
Nenhuma sugestao para @mariana_gomes.
```
O @mariana_gomes é um dos usuários isolados (não segue ninguém), por isso não tem sugestão.

**Comunidades:**
```
$ python py/main.py comunidades
Comunidades encontradas: 18
  Comunidade 1: 930 usuarios
  Comunidade 2: 620 usuarios
  Comunidade 3: 310 usuarios
  Comunidade 4: 8 usuarios
  ...
  Comunidade 18: 3 usuarios
Usuarios isolados: 58
```
Conferi a soma: os tamanhos das 18 comunidades mais os 58 isolados dão os 2000 usuários.

**Posts entre datas** (mesmo dia, mês inteiro, intervalo sem posts, datas invertidas e data mal formatada):
```
$ python py/main.py posts-entre 2025-03-01 2025-03-01
2025-03-01 | @mariana_araujo3 | 0 curtidas | Hash grafo javascript treino viagem semana dados
2025-03-01 | @renata_martins | 0 curtidas | Grafo chuva semana muito heap música
...
Posts encontrados: 30

$ python py/main.py posts-entre 2025-03-01 2025-03-31
...
Posts encontrados: 922

$ python py/main.py posts-entre 2026-11-01 2026-11-30
Posts encontrados: 0

$ python py/main.py posts-entre 2025-03-31 2025-03-01
Erro: a primeira data e maior que a segunda (2025-03-31 > 2025-03-01)

$ python py/main.py posts-entre 2025-3-1 2025-03-31
Erro: data invalida: '2025-3-1' (use AAAA-MM-DD)
```
O primeiro teste mostra que as duas datas entram no intervalo. Os posts vão até 2026-10-31, então novembro de 2026 não tem nenhum.

**Tops:**
```
$ python py/main.py top-seguidos 3
1. @nicolas_mendes (Nicolas Mendes) - 110 seguidores
2. @mariana_costa (Mariana Costa) - 109 seguidores
3. @renata_pinto (Renata Pinto) - 109 seguidores

$ python py/main.py top-curtidos 3
1. 2988 curtidas | @zeca_pinto | 2025-06-16 | De jogo de fim viagem livro café bom árvore cansado estruturas
2. 1274 curtidas | @ursula_martins | 2025-01-17 | Sol café finalmente ontem sabe algoritmo ruim
3. 789 curtidas | @renata_souza2 | 2026-06-03 | Dados viagem algoritmo academia
```
Testei também `top-seguidos 5000`, que é maior que o total, e ele mostra os 2000 usuários sem dar erro. No empate de 109 seguidores dá pra ver a ordem alfabética (mariana antes de renata).

**Ranking com a posição de um usuário:**
```
$ python py/main.py ranking --limite 3 --usuario @henrique_nascimento
1. @zeca_pinto - engajamento 3012 (7 seguidores, 2998 curtidas)
2. @ursula_martins - engajamento 1301 (5 seguidores, 1291 curtidas)
3. @renata_souza2 - engajamento 939 (7 seguidores, 925 curtidas)
Posicao de @henrique_nascimento: 927 de 2000
```
Conferi a conta do primeiro: 7 × 2 + 2998 = 3012.

**Erros de parâmetro:**
```
$ python py/main.py top-seguidos abc
Erro: k deve ser um numero inteiro maior que zero (recebido: 'abc')

$ python py/main.py sugerir @henrique_nascimento
Erro: parametros faltando. Uso: sugerir @usuario k
```

## 6. API de linha de comando (bônus)

Todos os comandos rodam numa chamada só: `python py/main.py <comando> [parâmetros] [--json]`.

| Comando | Parâmetros | Exemplo |
|---|---|---|
| `buscar` | @usuario | `python py/main.py buscar @henrique_nascimento` |
| `sugerir` | @usuario k | `python py/main.py sugerir @henrique_nascimento 5` |
| `comunidades` | nenhum | `python py/main.py comunidades` |
| `posts-entre` | data1 data2 (AAAA-MM-DD) | `python py/main.py posts-entre 2025-03-01 2025-03-31` |
| `top-seguidos` | k | `python py/main.py top-seguidos 10` |
| `top-curtidos` | k | `python py/main.py top-curtidos 10` |
| `ranking` | opcionais: --limite N, --usuario @x | `python py/main.py ranking --limite 20` |
| `ajuda` | nenhum | `python py/main.py ajuda` |

- `ajuda`, ou rodar sem nenhum comando, mostra a lista de comandos com exemplos. Um comando inválido mostra a mesma ajuda, mas termina com código 1.
- `--json` pode ir em qualquer posição e troca a saída por JSON.
- Em qualquer erro (parâmetro faltando, k que não é número, data inválida ou invertida, usuário inexistente) aparece uma mensagem começando com "Erro:" e o programa termina com `sys.exit(1)`. No sucesso, termina com código 0.

Exemplos com JSON:
```
$ python py/main.py top-seguidos 2 --json
[{"usuario": "@nicolas_mendes", "nome": "Nicolas Mendes", "seguidores": 110}, {"usuario": "@mariana_costa", "nome": "Mariana Costa", "seguidores": 109}]

$ python py/main.py buscar @naoexiste --json
{"erro": "usuario @naoexiste nao encontrado"}
```

Pra conferir o código de saída no Windows usei `echo %errorlevel%` logo depois do comando.

Sobre o JSON: o jeito normal seria montar um dict e usar `json.dumps`, mas dict é proibido. Então fiz três funções pequenas no `main.py` (`valor_json`, `objeto_json` e `lista_json`) que montam o texto do JSON a partir de listas. O `json.dumps` só é usado em texto e número soltos, pra ele cuidar das aspas e dos acentos. Os acentos saem escapados (tipo `é`), mas continua sendo JSON válido. Testei redirecionando pra um arquivo e abrindo com `python -m json.tool saida.json`.

Uma dificuldade que tive: no começo eu carregava os dados antes de olhar qual era o comando, então até um comando errado demorava pra mostrar a ajuda. Mudei pra conferir o comando primeiro e só depois montar as estruturas.

## Referências

- CORMEN, T. et al. Algoritmos: teoria e prática. 3. ed. (capítulos de heap, merge sort, tabelas hash e BFS)
- Documentação do Python: https://docs.python.org/3/library/sys.html e https://docs.python.org/3/library/json.html
- Material de aula da disciplina (AVL e rotações)
