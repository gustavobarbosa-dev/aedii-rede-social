# Tabela hash feita na mao, porque nao pode usar dict.
# Tratamento de colisao: encadeamento (cada posicao guarda uma lista de pares).


class TabelaHash:
    """Tabela hash com encadeamento separado.

    Guarda pares [chave, valor]. No projeto a chave e o @usuario
    e o valor e o id do usuario.
    """

    def __init__(self, tamanho=4099):
        """Cria a tabela vazia com 'tamanho' posicoes (baldes).

        4099 e primo e fica perto do dobro de usuarios (2000), assim
        cada balde fica com 0 ou 1 elemento na maioria das vezes.
        """
        self.tamanho = tamanho
        self.baldes = []
        for i in range(tamanho):
            self.baldes.append([])
        self.quantidade = 0

    def funcao_hash(self, chave):
        """Calcula em qual balde a chave vai ficar. O(tamanho da chave).

        Hash polinomial: para cada letra multiplica o valor anterior por 31
        e soma o codigo da letra (a mesma ideia do hashCode de String do Java).
        O % em cada passo deixa o numero sempre dentro do tamanho da tabela.
        Assim '@ana' e '@naa' caem em lugares diferentes, porque a posicao
        da letra muda o resultado (soma simples dos codigos daria igual).
        """
        h = 0
        for letra in chave:
            h = (h * 31 + ord(letra)) % self.tamanho
        return h

    def inserir(self, chave, valor):
        """Insere chave -> valor. Se a chave ja existe, troca o valor. O(1) em media."""
        pos = self.funcao_hash(chave)
        balde = self.baldes[pos]
        for par in balde:
            if par[0] == chave:
                par[1] = valor
                return
        # colisao: se ja tem outra chave nesse balde, ela so vai pro final da lista
        balde.append([chave, valor])
        self.quantidade += 1

    def buscar(self, chave):
        """Devolve o valor da chave, ou None se ela nao existir. O(1) em media."""
        pos = self.funcao_hash(chave)
        for par in self.baldes[pos]:
            if par[0] == chave:
                return par[1]
        return None

    def maior_balde(self):
        """Tamanho da maior lista de colisao (usei pra conferir se o hash espalha bem)."""
        maior = 0
        for balde in self.baldes:
            if len(balde) > maior:
                maior = len(balde)
        return maior
