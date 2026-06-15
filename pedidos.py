#pedidos.py
#finalizar pedido

from datetime import datetime
import carrinho as c
import cupons

historico_pedidos = []

def finalizar_pedido():
    if c.carrinho_esta_vazio():
        return False, "O carrinho está vazio. Adicione produtos antes de finalizar."

    # Verificação final de estoque antes de confirmar
    for produto_id, item in c.carrinho.items():
        produto = item["produto"]
        qtd = item["quantidade"]
        if produto["estoque"] < qtd:
            return False, (
                f"Estoque insuficiente para '{produto['nome']}' no momento da finalização. "
                f"Disponível: {produto['estoque']}, solicitado: {qtd}."
            )

    percentual = cupons.obter_desconto_atual()
    subtotal = c.calcular_subtotal()
    valor_desconto = subtotal * (percentual / 100)
    total = subtotal - valor_desconto

    itens_pedido = []
    for item in c.carrinho.values():
        produto = item["produto"]
        qtd = item["quantidade"]
        itens_pedido.append({
            "nome":          produto["nome"],
            "quantidade":    qtd,
            "preco_unitario": produto["preco"],
            "subtotal_item": produto["preco"] * qtd,
        })

        produto["estoque"] -= qtd #atualizar estoque 

    pedido = {
        "numero":         len(historico_pedidos) + 1,
        "data_hora":      datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "itens":          itens_pedido,
        "subtotal":       subtotal,
        "cupom":          cupons.obter_cupom_atual(),
        "percentual_desconto": percentual,
        "valor_desconto": valor_desconto,
        "total":          total,
    }

    historico_pedidos.append(pedido)

    c.limpar_carrinho() #começar de novo
    cupons.remover_cupom()

    return True, pedido

def exibir_resumo_pedido(pedido):
    print("\n" + "=" * 60)
    print(f"PEDIDO #{pedido['numero']:04d} CONFIRMADO!")
    print(f"    {pedido['data_hora']}")
    print("=" * 60)
    print("  ITENS:")
    for item in pedido["itens"]:
        print(
            f"    {item['quantidade']:2d}x  {item['nome']:<25}"
            f"  R$ {item['preco_unitario']:>8.2f}  =  R$ {item['subtotal_item']:>9.2f}"
        )
    print("-" * 60)
    print(f"  {'Subtotal':<42}  R$ {pedido['subtotal']:>9.2f}")
    if pedido["cupom"]:
        print(
            f"  {'Cupom ' + pedido['cupom'] + ' (' + str(pedido['percentual_desconto']) + '%)':<42}"
            f"  R$ {pedido['valor_desconto']:>9.2f}"
        )
    print(f"  {'TOTAL PAGO':<42}  R$ {pedido['total']:>9.2f}")
    print("=" * 60)
    print("Obrigado pela sua compra!\n")

def exibir_historico():
    if not historico_pedidos:
        print("\n  Nenhum pedido realizado ainda.\n")
        return

    print("\n" + "=" * 60)
    print("HISTÓRICO DE PEDIDOS")
    print("=" * 60)
    for pedido in historico_pedidos:
        cupom_info = f" | Cupom: {pedido['cupom']} (-{pedido['percentual_desconto']}%)" if pedido["cupom"] else ""
        print(
            f"  Pedido #{pedido['numero']:04d}  |  {pedido['data_hora']}"
            f"  |  Total: R$ {pedido['total']:.2f}{cupom_info}"
        )
    print()