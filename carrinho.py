#carrinho.py
#carrinho de compras


class Carrinho:
    """Gerencia os itens adicionados, cálculos e cupom de desconto."""

    CUPONS_VALIDOS = {
    "PRIMEIRACOMPRA10": 10.0,
    "VERAO15": 15.0,
    "BLACKFRIDAY20": 20.0,
    "SEMANADOCONSUMIDOR15": 15.0,
    }

    def __init__(self):
        # { produto.id: {"produto": Produto, "quantidade": int} }
        self.__itens = {}
        self.__cupom = None
        self.__percentual_desconto = 0.0

    # --- Itens ---
    def adicionar(self, produto, quantidade=1):
        """Adiciona um produto ao carrinho. Retorna (True, msg) ou (False, msg)."""
        if quantidade <= 0:
            return False, "Quantidade deve ser maior que zero."

        ja_no_carrinho = self.__itens[produto.id]["quantidade"] if produto.id in self.__itens else 0
        total_desejado = ja_no_carrinho + quantidade

        if not produto.tem_estoque(total_desejado):
            disponivel = produto.estoque - ja_no_carrinho
            if disponivel <= 0:
                return False, f"'{produto.nome}' está fora de estoque."
            return False, (
                f"Estoque insuficiente para '{produto.nome}'. "
                f"Você já tem {ja_no_carrinho} no carrinho e há apenas "
                f"{produto.estoque} no estoque (máx. {disponivel} a mais)."
            )

        if produto.id in self.__itens:
            self.__itens[produto.id]["quantidade"] += quantidade
        else:
            self.__itens[produto.id] = {"produto": produto, "quantidade": quantidade}

        return True, f"✅ {quantidade}x '{produto.nome}' adicionado ao carrinho."

    def remover(self, produto_id, quantidade=None):
        """Remove um produto do carrinho. Se quantidade=None, remove tudo."""
        if produto_id not in self.__itens:
            return False, "Produto não está no carrinho."

        nome = self.__itens[produto_id]["produto"].nome

        if quantidade is None or quantidade >= self.__itens[produto_id]["quantidade"]:
            del self.__itens[produto_id]
            return True, f"🗑 '{nome}' removido do carrinho."

        if quantidade <= 0:
            return False, "Quantidade deve ser maior que zero."

        self.__itens[produto_id]["quantidade"] -= quantidade
        return True, f"🗑 {quantidade}x '{nome}' removido do carrinho."

    def esta_vazio(self):
        return len(self.__itens) == 0

    def limpar(self):
        self.__itens.clear()
        self.__cupom = None
        self.__percentual_desconto = 0.0

    @property
    def itens(self):
        return dict(self.__itens)

    # --- Cupom ---
    def aplicar_cupom(self, codigo):
        codigo = codigo.strip().upper()
        if codigo not in self.CUPONS_VALIDOS:
            return False, f"❌ Cupom '{codigo}' inválido ou expirado."
        self.__cupom = codigo
        self.__percentual_desconto = self.CUPONS_VALIDOS[codigo]
        return True, f"✅ Cupom '{codigo}' aplicado! Desconto de {self.__percentual_desconto:.0f}%."

    def remover_cupom(self):
        self.__cupom = None
        self.__percentual_desconto = 0.0

    @property
    def cupom(self):
        return self.__cupom

    @property
    def percentual_desconto(self):
        return self.__percentual_desconto

    # --- Cálculos ---
    def subtotal(self):
        return sum(
            item["produto"].preco * item["quantidade"]
            for item in self.__itens.values()
        )

    def valor_desconto(self):
        return self.subtotal() * (self.__percentual_desconto / 100)

    def total(self):
        return self.subtotal() - self.valor_desconto()

    # --- Exibição ---
    def __str__(self):
        if self.esta_vazio():
            return "  O carrinho está vazio."

        linhas = ["\n" + "=" * 60, " 🛒 SEU CARRINHO", "=" * 60]
        for item in self.__itens.values():
            p = item["produto"]
            qtd = item["quantidade"]
            linhas.append(
                f"  {qtd:2d}x  {p.nome:<25}  R$ {p.preco:>8.2f}  =  R$ {p.preco * qtd:>9.2f}"
            )
        linhas.append("-" * 60)
        linhas.append(f"  {'Subtotal':<40}  R$ {self.subtotal():>9.2f}")
        if self.__percentual_desconto > 0:
            linhas.append(
                f"  {'Desconto (' + str(self.__percentual_desconto) + '%)':<40}"
                f"  R$ {self.valor_desconto():>9.2f}"
            )
        linhas.append(f"  {'TOTAL':<40}  R$ {self.total():>9.2f}")
        return "\n".join(linhas)

    def __repr__(self):
        return f"Carrinho(itens={len(self.__itens)}, total={self.total():.2f})"