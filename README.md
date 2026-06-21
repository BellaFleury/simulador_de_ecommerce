#Simulador de E-Commerce

Simulador de e-commerce em Python (três fases):
- Fase 1 — lógica procedural com funções e dicionários
- Fase 2 — refatoração para Orientação a Objetos
- Fase 3 — interface gráfica web com Streamlit

#Funcionalidades

- Catálogo de produtos com filtro por categoria
- Carrinho com adição, remoção e alteração de quantidade
- Cupons de desconto percentuais
- Resumo do pedido antes de finalizar
- Histórico de pedidos da sessão
- Feedback visual de erros (estoque, cupom inválido, carrinho vazio)

#Estrutura do Projeto
````
ecommerce-simulator/
│
├── Fase 1 — Procedural
│   ├── main.py        # Entry point da Fase 1
│   ├── catalogo.py    # Catálogo e funções de busca
│   ├── carrinho.py    # Gerenciamento do carrinho (funções)
│   ├── cupons.py      # Validação e aplicação de cupons
│   └── pedidos.py     # Finalização de pedidos e histórico
│
├── Fase 2 — Orientação a Objetos
│   ├── main_oo.py     # Entry point da Fase 2
│   ├── produto.py     # Classe Produto e subclasses (herança)
│   ├── carrinho.py    # Classe Carrinho com cupom integrado
│   ├── pedido.py      # Classe Pedido com snapshot dos dados
│   └── loja.py        # Classe Loja — orquestra tudo
│
├── Fase 3 — Interface Gráfica
│   └── app.py         # Interface web com Streamlit
│
├── requirements.txt   # Dependências do projeto
├── .gitignore
└── README.md
```

#Diagrama de Classes (Fase 2 e 3)

```
Produto  ◄──────────────────────────┐
  ├── ProdutoRoupa (+ estacao)       │
  └── ProdutoAcessorioModa (+ tipo)  │
                                     │
Carrinho  ──── usa ──────────────────┘
  └── aplica cupons de desconto

Pedido
  └── snapshot imutável dos dados na compra

Loja
  ├── possui Carrinho
  ├── gerencia catálogo de Produtos
  └── cria e armazena Pedidos

app.py (Streamlit)
  └── usa apenas Loja — toda lógica fica nas classes
```

# Como rodar

Pré-requisito: Python 3.8 ou superior.

```bash
git clone https://github.com/BellaFleury/simulador_de_ecommerce.git
cd simulador_de_ecommerce
```

#Instalar dependências

```bash
pip install -r requirements.txt
```

#Fase 1 — procedural
```bash
python main.py
```

#Fase 2 — orientação a objetos
```bash
python main_oo.py
```

#Fase 3 — interface gráfica (Streamlit)
```bash
streamlit run app.py
```

O navegador abrirá automaticamente em `http://localhost:8501`.

#Cupons disponíveis

 Código        | Desconto 
---------------|----------
 `DESCONTO5`   | 5%       
 `WELCOME10`   | 10%      
 `SEMESTRAL15` | 15%      
 `PROMO20`     | 20%      
 `BLACKFRIDAY` | 30%      