# main_oo.py
# Interface principal do simulador (versão OO)

from loja import Loja


def menu_principal():
    print("\n" + "=" * 50)
    print("  SIMULADOR DE E-COMMERCE  (v2 — OO)")
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


def submenu_busca(loja):
    print("\n  Como deseja buscar?")
    print("  1. Por nome")
    print("  2. Por categoria")
    opcao = input(" Opção: ").strip()

    if opcao == "1":
        termo = input(" Digite o nome (ou parte): ").strip()
        if not termo:
            print("  Termo de busca vazio.")
            return
        resultados = loja.buscar_por_nome(termo)
        if not resultados:
            print(f" Nenhum produto encontrado com '{termo}'.")
        else:
            print(f"\n Resultados para '{termo}':")
            for p in resultados:
                print(f"  {p}")

    elif opcao == "2":
        cats = loja.listar_categorias()
        print("\n Categorias disponíveis:")
        for c in cats:
            print(f"    • {c}")
        nome_cat = input(" Digite a categoria: ").strip()
        resultados = loja.buscar_por_categoria(nome_cat)
        if not resultados:
            print(f" Nenhum produto na categoria '{nome_cat}'.")
        else:
            for p in resultados:
                print(f"  {p}")
    else:
        print(" Opção inválida.")


def submenu_adicionar(loja):
    try:
        produto_id = int(input(" ID do produto a adicionar: ").strip())
        quantidade = int(input(" Quantidade: ").strip())
    except ValueError:
        print(" Entrada inválida. Digite números inteiros.")
        return
    sucesso, mensagem = loja.adicionar_ao_carrinho(produto_id, quantidade)
    print(f"  {mensagem}")


def submenu_remover(loja):
    if loja.carrinho.esta_vazio():
        print(" O carrinho já está vazio.")
        return

    loja.exibir_carrinho()

    try:
        produto_id = int(input(" ID do produto a remover (0 = cancelar): ").strip())
    except ValueError:
        print(" Entrada inválida.")
        return

    if produto_id == 0:
        return

    resp = input(" Remover tudo desse item? (s/N): ").strip().lower()
    if resp == "s":
        sucesso, mensagem = loja.remover_do_carrinho(produto_id)
    else:
        try:
            qtd = int(input(" Quantidade a remover: ").strip())
        except ValueError:
            print(" Quantidade inválida.")
            return
        sucesso, mensagem = loja.remover_do_carrinho(produto_id, qtd)

    print(f"  {mensagem}")


def submenu_cupom(loja):
    cupom_atual = loja.carrinho.cupom
    if cupom_atual:
        print(f" Cupom atual: {cupom_atual} ({loja.carrinho.percentual_desconto:.0f}% de desconto)")
        resp = input(" Deseja trocar o cupom? (s/N): ").strip().lower()
        if resp != "s":
            return

    codigo = input(" Digite o código do cupom: ").strip()
    if not codigo:
        print(" Código não pode ser vazio.")
        return

    sucesso, mensagem = loja.aplicar_cupom(codigo)
    print(f"  {mensagem}")


def submenu_finalizar(loja):
    if loja.carrinho.esta_vazio():
        print(" O carrinho está vazio. Adicione produtos primeiro.")
        return

    loja.exibir_carrinho()

    confirmacao = input(" Confirmar pedido? (s/N): ").strip().lower()
    if confirmacao != "s":
        print(" Pedido cancelado.")
        return

    sucesso, resultado = loja.finalizar_pedido()
    if sucesso:
        print(resultado)
    else:
        print(f" Erro ao finalizar: {resultado}")


def main():
    loja = Loja("E-Commerce Simulator")
    print("\n  Bem-vindo ao Simulador de E-Commerce! 🛍")

    while True:
        menu_principal()
        opcao = input(" Escolha uma opção: ").strip()

        if opcao == "1":
            loja.exibir_catalogo()
        elif opcao == "2":
            submenu_busca(loja)
        elif opcao == "3":
            loja.exibir_catalogo()
            submenu_adicionar(loja)
        elif opcao == "4":
            submenu_remover(loja)
        elif opcao == "5":
            loja.exibir_carrinho()
        elif opcao == "6":
            submenu_cupom(loja)
        elif opcao == "7":
            submenu_finalizar(loja)
        elif opcao == "8":
            loja.exibir_historico()
        elif opcao == "0":
            print("\n  Até logo! \n")
            break
        else:
            print(" Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()