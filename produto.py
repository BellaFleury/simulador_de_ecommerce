# produto2.py 
# Classes de produto com herança


class Produto:
    """Classe base que representa um produto do catálogo."""

    def __init__(self, id, nome, preco, categoria, estoque):
        self._id = id
        self._nome = nome
        self._preco = preco
        self._categoria = categoria
        self._estoque = estoque

    @property
    def id(self):
        return self._id

    @property
    def nome(self):
        return self._nome

    @property
    def preco(self):
        return self._preco

    @property
    def categoria(self):
        return self._categoria

    @property
    def estoque(self):
        return self._estoque

    def tem_estoque(self, quantidade=1):
        """Retorna True se houver estoque suficiente para a quantidade pedida."""
        return self._estoque >= quantidade

    def debitar_estoque(self, quantidade):
        """Debita a quantidade do estoque. Lança erro se insuficiente."""
        if not self.tem_estoque(quantidade):
            raise ValueError(f"Estoque insuficiente para '{self._nome}'.")
        self._estoque -= quantidade

    def info_extra(self):
        """Retorna informações extras do produto (sobrescrita nas subclasses)."""
        return ""

    def __str__(self):
        status = f"{self._estoque} em estoque" if self._estoque > 0 else "⚠ Fora de estoque"
        extra = f" | {self.info_extra()}" if self.info_extra() else ""
        return (
            f"[{self._id:2d}] {self._nome:<25} R$ {self._preco:>8.2f}"
            f"  |  {self._categoria:<14} | {status}{extra}"
        )

    def __repr__(self):
        return f"Produto(id={self._id}, nome='{self._nome}', preco={self._preco})"


class ProdutoRoupa(Produto):
    """Roupa com estação/ocasião indicada."""

    def __init__(self, id, nome, preco, estoque, estacao):
        super().__init__(id, nome, preco, "Roupa", estoque)
        self._estacao = estacao

    @property
    def estacao(self):
        return self._estacao

    def info_extra(self):
        return f"Estação: {self._estacao}"

    def __repr__(self):
        return f"ProdutoRoupa(id={self._id}, nome='{self._nome}', estacao='{self._estacao}')"


class ProdutoAcessorioModa(Produto):
    """Acessório de moda com tipo indicado."""

    def __init__(self, id, nome, preco, estoque, tipo):
        super().__init__(id, nome, preco, "Acessório", estoque)
        self._tipo = tipo

    @property
    def tipo(self):
        return self._tipo

    def info_extra(self):
        return f"Tipo: {self._tipo}"

    def __repr__(self):
        return f"ProdutoAcessorioModa(id={self._id}, nome='{self._nome}', tipo='{self._tipo}')"