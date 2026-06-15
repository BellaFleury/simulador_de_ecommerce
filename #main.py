#main.py

import catalogo as cat
import carrinho as car
import cupons
import pedidos

def menu_principal():
    print("\n" + "=" * 50)
    print("SIMULADOR DE E-COMMERCE")
    print("=" * 50)
    print("  1. Ver catálogo completo")
    print("  2. Buscar produto")
    print("  3. Adicionar produto ao carrinho")
    print("  4. Remover produto do carrinho")
    print("  5. Ver carrinho")
    print("  6. Aplicar cupom de desconto")
    print("  7. Finalizar pedido")
    print("  8. Ver histórico de pedidos")
    print("  0. Sair")
    print("-" * 50)

def submenu_busca():
    print("\nComo deseja buscar?")
    print(" 1. Por nome")
    print(" 2. Por categoria")
    opcao = input("Opção: ").strip()

    if opcao == "1":
        termo = input("Digite o nome (ou parte): ").strip()
        if not termo:
            print("Termo de busca vazio.")
            return
        resultados = cat.buscar_por_nome(termo)
        if not resultados:
            print(f"Nenhum produto encontrado com '{termo}'.")
        else:
            print(f"\nResultados para '{termo}':")
            for p in resultados:
                cat.exibir_produto(p)

    elif opcao == "2":
        cats = cat.listar_categorias()
        print("\nCategorias disponíveis:")
        for i, c in enumerate(cats, 1):
            print(f"    {i}. {c}")
        nome_cat = input("Digite a categoria: ").strip()
        resultados = cat.buscar_por_categoria(nome_cat)
        if not resultados:
            print(f"Nenhum produto na categoria '{nome_cat}'.")
        else:
            print(f"\nProdutos em '{nome_cat}':")
            for p in resultados:
                cat.exibir_produto(p)
    else:
        print("Opção inválida.")

def submenu_adicionar():
    try:
        produto_id = int(input("ID do produto a adicionar: ").strip())
        quantidade = int(input("Quantidade: ").strip())
    except ValueError:
        print("Entrada inválida. Digite números inteiros.")
        return

    sucesso, mensagem = car.adicionar_ao_carrinho(produto_id, quantidade)
    print(f"  {mensagem}")

def submenu_remover():
    if car.carrinho_esta_vazio():
        print("O carrinho já está vazio.")
        return

    car.exibir_carrinho(cupons.obter_desconto_atual())

    try:
        produto_id = int(input("ID do produto a remover (0 = cancelar): ").strip())
    except ValueError:
        print("Entrada inválida.")
        return

    if produto_id == 0:
        return

    resp = input("Remover tudo desse item? (s/N): ").strip().lower()
    if resp == "s":
        sucesso, mensagem = car.remover_do_carrinho(produto_id)
    else:
        try:
            qtd = int(input("Quantidade a remover: ").strip())
        except ValueError:
            print("Quantidade inválida.")
            return
        sucesso, mensagem = car.remover_do_carrinho(produto_id, qtd)

    print(f"  {mensagem}")

def submenu_cupom():
    cupom_atual = cupons.obter_cupom_atual()
    if cupom_atual:
        print(f"  Cupom atual: {cupom_atual} ({cupons.obter_desconto_atual():.0f}% de desconto)")
        resp = input("Deseja trocar o cupom? (s/N): ").strip().lower()
        if resp != "s":
            return

    codigo = input("Digite o código do cupom: ").strip()
    if not codigo:
        print("Código não pode ser vazio.")
        return

    sucesso, mensagem = cupons.aplicar_cupom(codigo)
    print(f"{mensagem}")

def submenu_finalizar():
    if car.carrinho_esta_vazio():
        print("O carrinho está vazio. Adicione produtos primeiro.")
        return

    car.exibir_carrinho(cupons.obter_desconto_atual())

    confirmacao = input("  Confirmar pedido? (s/N): ").strip().lower()
    if confirmacao != "s":
        print("Pedido cancelado.")
        return

    sucesso, resultado = pedidos.finalizar_pedido()
    if sucesso:
        pedidos.exibir_resumo_pedido(resultado)
    else:
        print(f"Erro ao finalizar: {resultado}")

def main():
    print("\n  Bem-vindo ao Simulador de E-Commerce! 🛍")

    while True:
        menu_principal()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cat.exibir_catalogo()

        elif opcao == "2":
            submenu_busca()

        elif opcao == "3":
            cat.exibir_catalogo()
            submenu_adicionar()

        elif opcao == "4":
            submenu_remover()

        elif opcao == "5":
            car.exibir_carrinho(cupons.obter_desconto_atual())

        elif opcao == "6":
            submenu_cupom()

        elif opcao == "7":
            submenu_finalizar()

        elif opcao == "8":
            pedidos.exibir_historico()

        elif opcao == "0":
            print("\n Até logo!\n")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()