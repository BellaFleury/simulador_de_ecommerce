# pedido.py
# Classe Pedido

from datetime import datetime


class Pedido:
    """Representa um pedido finalizado com snapshot dos itens e valores."""

    _contador = 0  # Contador de pedidos na sessão

    def __init__(self, itens, subtotal, cupom, percentual_desconto, valor_desconto, total):
        Pedido._contador += 1
        self.__numero = Pedido._contador
        self.__data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.__itens = itens  # lista de dicts com snapshot
        self.__subtotal = subtotal
        self.__cupom = cupom
        self.__percentual_desconto = percentual_desconto
        self.__valor_desconto = valor_desconto
        self.__total = total

    # --- Getters ---
    @property
    def numero(self):
        return self.__numero

    @property
    def data_hora(self):
        return self.__data_hora

    @property
    def itens(self):
        return list(self.__itens)

    @property
    def subtotal(self):
        return self.__subtotal

    @property
    def cupom(self):
        return self.__cupom

    @property
    def percentual_desconto(self):
        return self.__percentual_desconto

    @property
    def valor_desconto(self):
        return self.__valor_desconto

    @property
    def total(self):
        return self.__total

    # --- Exibição ---
    def __str__(self):
        linhas = [
            "\n" + "=" * 60,
            f" PEDIDO #{self.__numero:04d} CONFIRMADO!",
            f"    {self.__data_hora}",
            "=" * 60,
            "  ITENS:",
        ]
        for item in self.__itens:
            linhas.append(
                f"    {item['quantidade']:2d}x  {item['nome']:<25}"
                f"  R$ {item['preco_unitario']:>8.2f}  =  R$ {item['subtotal_item']:>9.2f}"
            )
        linhas.append("-" * 60)
        linhas.append(f"  {'Subtotal':<42}  R$ {self.__subtotal:>9.2f}")
        if self.__cupom:
            linhas.append(
                f"  {'Cupom ' + self.__cupom + ' (' + str(self.__percentual_desconto) + '%)':<42}"
                f"  R$ {self.__valor_desconto:>9.2f}"
            )
        linhas.append(f"  {'TOTAL PAGO':<42}  R$ {self.__total:>9.2f}")
        linhas.append("=" * 60)
        linhas.append("  Obrigado pela sua compra! 🛍\n")
        return "\n".join(linhas)

    def __repr__(self):
        return f"Pedido(numero={self.__numero}, total={self.__total:.2f}, data='{self.__data_hora}')"