#catalogo.py 
#catalogo e-commerce

catalogo = [
    {"id": 1, "nome": "blusa florida", "preco": 70.00, "ctegoria": "Verão", "estoque": 25},
    {"id": 2, "nome": "vestido", "preco": 80.00, "ctegoria": "Verão", "estoque": 30},
    {"id": 3, "nome": "brinco", "preco": 15.00, "ctegoria": "Acessorios", "estoque": 25},
    {"id": 4, "nome": "cinto de couro", "preco": 20.00, "ctegoria": "Acessorios", "estoque": 10},
    {"id": 5, "nome": "calça jeans", "preco": 140.00, "ctegoria": "Calca", "estoque": 40},
    {"id": 6, "nome": "calça social", "preco": 120.00, "ctegoria": "Calca", "estoque": 20},
    {"id": 7, "nome": "camiseta inverno", "preco": 80.00, "ctegoria": "Inverno", "estoque": 15},
    {"id": 8, "nome": "jaqueta", "preco": 100.00, "ctegoria": "Inverno", "estoque": 45},
    {"id": 9, "nome": "suéter", "preco": 75.00, "ctegoria": "Inverno", "estoque": 30},
    {"id": 10, "nome": "conjunto academia", "preco": 160.00, "ctegoria": "Fit", "estoque": 25},
]

def buscar_por_nome(nome):
    termo= nome.strip().lower()
    resultado= [p for p in catalogo if termo in p["nome"].lower()]
    return resultado

def listar_categorias():
    return sorted(set(p["categoria"] for p in catalogo))

def buscar_por_id(produto_id):
    for produto in catalogo:
        if produto["id"] == produto_id:
            return produto
    return None

def exibir_produto(produto):
    if produto:
        print(f"id: {produto['id']}")
        print(f"nome: {produto['nome']}")
        print(f"preco: {produto['preco']}")
        print(f"categoria: {produto['categoria']}")
        print(f"estoque: {produto['estoque']}")
    else:
        print("Produto não encontrado.")

def exibir_catalogo():
    print("\n" + "=" * 70)
    print(" CATÁLOGO DE PRODUTOS")
    print("=" * 70)
    for categoria in listar_categorias():
        print(f"\n {categoria}")
        produtos_da_cat = buscar_por_categoria(categoria)
        for p in produtos_da_cat:
            exibir_produto(p)
    print()