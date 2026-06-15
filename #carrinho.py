#carrinho.py
#carrinho de compras

from catalogo import buscar_por_id
carrinho = {}

def adicionar_ao_carrinho(produto_id, quantidade = 1):
    if quantidade <= 0:
        return False,
    produto = buscar_por_id(produto_id)
    if produto is None:
    return False, "Produto não encontrado."

quantidade_ja_no_carrinho = carrinho[produto_id]["quantidade"] if produto_id in carrinho else 0
total_desejado = quantidade_ja_no_carrinho + quantidade

if total_desejado > produto["estoque"]:
    disponivel = produto["estoque"] - quantidade_ja_no_carrinho
    if disponivel <=0:
        return False, f"Não há mais estoque disponível para {produto['nome']}."
        return False, f"Você já tem {quantidade_ja_no_carrinho} no carrinho e há apenas {disponivel} unidades restantes em estoque. Você pode adicionar até {disponivel} unidades."

if produto_id in carrinho:
    carrinho[produto_id][quantidade] += quantidade
else:
    carrinho[produto_id] = {"produto": produto, "quantidade": quantidade}
    return True, f"{quantidade}x '{produto['nome']}' adicionado ao carrinho."

def remover_do_carrinho(produto_id, quantidade = None):
    if produto_id not in carrinho:
        return False, "Produto não encontrado no carrinho."
    
    if quantidade is None or quantidade >= carrinho[produto_id]["quantidade"]:
        del carrinho[produto_id]
        return True, "Produto removido do carrinho."
    else:
        carrinho[produto_id]["quantidade"] -= quantidade
        return True, f"{quantidade}x '{carrinho[produto_id]['produto']['nome']}' removido do carrinho."

def calcular_subtotal():
    total = 0.0
    for item in carrinho.values():
        total += item["produto"]["preco"] * item["quantidade"]
    return total
def calcular_total_com_desconto(percentual_desconto=0.0):
    subtotal = calcular_subtotal()
    desconto = subtotal * (percentual_desconto / 100)
    return subtotal - desconto

def limpar_carrinho():
    carrinho.clear()

def carrinho_esta_vazio():
    return len(carrinho) == 0

def exibir_carrinho(percentual_desconto=0.0):
    if carrinho_esta_vazio():
        print("\nO carrinho está vazio.")
        return
    
    print("\n" + "=" * 60)
    print(" SEU CARRINHO DE COMPRAS")
    print("=" * 60)
    for item in carrinho.values():
        produto = item["produto"]
        quantidade = item["quantidade"]
        preco_unitario = produto["preco"]
        preco_total = preco_unitario * quantidade
        print(f"{quantidade}x {produto['nome']} - R${preco_unitario:.2f} cada - Total: R${preco_total:.2f}")
    
    subtotal = calcular_subtotal()
    total_com_desconto = calcular_total_com_desconto(percentual_desconto)
    print("-" * 60)
    print(f"Subtotal: R${subtotal:.2f}")
    if percentual_desconto > 0:
        valor_desconto = subtotal * (percentual_desconto / 100)
        total = subtotal - valor_desconto
        print(f"Desconto: {percentual_desconto}%")
        print(f"Total com desconto: R${total_com_desconto:.2f}")
    else:
        print(f"Total: R${subtotal:.2f}")
    print()