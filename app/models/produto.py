class Produto:
    """Produto da loja AURA. O id identifica unicamente cada registro."""

    def __init__(self, id, nome, categoria, preco, tamanho, cor):
        self.id = int(id)
        self.nome = str(nome).strip()
        self.categoria = str(categoria).strip()
        self.preco = float(preco)
        self.tamanho = str(tamanho).strip()
        self.cor = str(cor).strip()

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "categoria": self.categoria,
            "preco": self.preco,
            "tamanho": self.tamanho,
            "cor": self.cor,
        }
