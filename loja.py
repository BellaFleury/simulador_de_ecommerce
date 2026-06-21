# loja.py
# Classe Loja que orquestra catálogo, carrinho e pedidos

from produto import ProdutoRoupa, ProdutoAcessorioModa
from carrinho import Carrinho
from pedido import Pedido


class Loja:
    """Orquestra o catálogo, os pedidos e as regras de negócio."""

    def __init__(self, nome="Loja de Moda"):
        self.__nome = nome
        self.__catalogo = self.__criar_catalogo()
        self.__carrinho = Carrinho()
        self.__historico = []

    def __criar_catalogo(self):
        return [
            ProdutoRoupa(1,  "Blusa Florida", 70.00,  25, estacao="Verão"),
            ProdutoRoupa(2,  "Vestido", 80.00,  30, estacao="Verão"),
            ProdutoAcessorioModa(3, "Brinco", 15.00,  25, tipo="Bijuteria"),
            ProdutoAcessorioModa(4, "Cinto de Couro", 20.00,  10, tipo="Couro"),
            ProdutoRoupa(5,  "Calça Jeans", 140.00,  40, estacao="Casual"),
            ProdutoRoupa(6,  "Calça Social", 120.00,  20, estacao="Formal"),
            ProdutoRoupa(7,  "Camiseta Inverno", 80.00,  15, estacao="Inverno"),
            ProdutoRoupa(8,  "Jaqueta", 100.00,  45, estacao="Inverno"),
            ProdutoRoupa(9,  "Suéter", 75.00,  30, estacao="Inverno"),
            ProdutoRoupa(10, "Conjunto Academia", 160.00,  25, estacao="Fitness"),
        ]

    # --- Catálogo ---
    def buscar_por_id(self, produto_id):
        for p in self.__catalogo:
            if p.id == produto_id:
                return p
        return None

    def buscar_por_nome(self, termo):
        termo = termo.strip().lower()
        return [p for p in self.__catalogo if termo in p.nome.lower()]

    def buscar_por_categoria(self, categoria):
        cat = categoria.strip().lower()
        return [p for p in self.__catalogo if p.categoria.lower() == cat]

    def listar_categorias(self):
        return sorted(set(p.categoria for p in self.__catalogo))

    def exibir_catalogo(self):
        print("\n" + "=" * 70)
        print(f" {self.__nome.upper()} — CATÁLOGO DE PRODUTOS")
        print("=" * 70)
        for categoria in self.listar_categorias():
            print(f"\n  📂 {categoria}")
            for p in self.buscar_por_categoria(categoria):
                print(f"  {p}")
        print()

    # --- Carrinho ---
    def adicionar_ao_carrinho(self, produto_id, quantidade=1):
        produto = self.buscar_por_id(produto_id)
        if produto is None:
            return False, f"Produto de ID {produto_id} não encontrado."
        return self.__carrinho.adicionar(produto, quantidade)

    def remover_do_carrinho(self, produto_id, quantidade=None):
        return self.__carrinho.remover(produto_id, quantidade)

    def aplicar_cupom(self, codigo):
        return self.__carrinho.aplicar_cupom(codigo)

    def exibir_carrinho(self):
        print(self.__carrinho)

    @property
    def carrinho(self):
        return self.__carrinho

    # --- Pedidos ---
    def finalizar_pedido(self):
        if self.__carrinho.esta_vazio():
            return False, "O carrinho está vazio."

        for item in self.__carrinho.itens.values():
            produto = item["produto"]
            qtd = item["quantidade"]
            if not produto.tem_estoque(qtd):
                return False, f"Estoque insuficiente para '{produto.nome}'."

        itens_snapshot = []
        for item in self.__carrinho.itens.values():
            produto = item["produto"]
            qtd = item["quantidade"]
            itens_snapshot.append({
                "nome":           produto.nome,
                "quantidade":     qtd,
                "preco_unitario": produto.preco,
                "subtotal_item":  produto.preco * qtd,
            })
            produto.debitar_estoque(qtd)

        pedido = Pedido(
            itens=itens_snapshot,
            subtotal=self.__carrinho.subtotal(),
            cupom=self.__carrinho.cupom,
            percentual_desconto=self.__carrinho.percentual_desconto,
            valor_desconto=self.__carrinho.valor_desconto(),
            total=self.__carrinho.total(),
        )

        self.__historico.append(pedido)
        self.__carrinho.limpar()
        return True, pedido

    @property
    def historico(self):
        return list(self.__historico)

    def exibir_historico(self):
        if not self.__historico:
            print("\n  Nenhum pedido realizado ainda.\n")
            return
        print("\n" + "=" * 60)
        print(" HISTÓRICO DE PEDIDOS")
        print("=" * 60)
        for pedido in self.__historico:
            cupom_info = (
                f" | Cupom: {pedido.cupom} (-{pedido.percentual_desconto}%)"
                if pedido.cupom else ""
            )
            print(
                f"  Pedido #{pedido.numero:04d}  |  {pedido.data_hora}"
                f"  |  Total: R$ {pedido.total:.2f}{cupom_info}"
            )
        print()

    def __str__(self):
        return f"Loja(nome='{self.__nome}', produtos={len(self.__catalogo)}, pedidos={len(self.__historico)})"

    def __repr__(self):
        return self.__str__()