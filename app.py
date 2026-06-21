# app.py
# Interface gráfica do simulador de e-commerce usando Streamlit
# st.set_page_config — configura o título e ícone que aparece na aba do navegador.
# st.session_state — guarda a Loja na memória pra não perder o carrinho a cada clique.
# st.tabs — cria as três abas (Catálogo, Carrinho, Histórico).
# st.columns — divide a tela em colunas. Por exemplo [3, 1] cria duas colunas onde a primeira é 3x maior que a segunda.
# st.number_input — campo numérico pra escolher quantidade.
# st.button — botão clicável. Quando clicado, retorna True.
# st.success / st.error / st.warning / st.info — são os feedbacks visuais coloridos (verde, vermelho, amarelo, azul).
# st.rerun() — reroda a página após uma ação como remover item do carrinho, pra atualizar a tela.
# st.balloons() — animação de balões quando o pedido é finalizado.

import streamlit as st
from loja import Loja

# ── Configuração da página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Loja de Moda",
    page_icon="👗",
    layout="wide",
)

# ── Session state ───────────────────────────────────────────────────────────
if "loja" not in st.session_state:
    st.session_state.loja = Loja("Loja de Moda")

loja = st.session_state.loja

# ── Cabeçalho ───────────────────────────────────────────────────────────────
st.title(" Loja de Moda")
st.markdown("---")

# ── Navegação por abas ──────────────────────────────────────────────────────
aba_catalogo, aba_carrinho, aba_historico = st.tabs([
    "🛍 Catálogo",
    "🛒 Carrinho",
    "📋 Histórico de Pedidos",
])


# ════════════════════════════════════════════════════════════════════════════
# ABA 1 — CATÁLOGO
# ════════════════════════════════════════════════════════════════════════════
with aba_catalogo:
    st.header("Catálogo de Produtos")

    categorias = ["Todas"] + loja.listar_categorias()
    categoria_escolhida = st.selectbox("Filtrar por categoria:", categorias)

    if categoria_escolhida == "Todas":
        produtos = []
        for cat in loja.listar_categorias():
            produtos.extend(loja.buscar_por_categoria(cat))
    else:
        produtos = loja.buscar_por_categoria(categoria_escolhida)

    st.markdown(f"**{len(produtos)} produto(s) encontrado(s)**")
    st.markdown("---")

    for produto in produtos:
        col_info, col_acao = st.columns([3, 1])

        with col_info:
            status = f"{produto.estoque} em estoque" if produto.estoque > 0 else "Fora de estoque"
            st.markdown(f"### {produto.nome}")
            st.markdown(f"**R$ {produto.preco:.2f}** &nbsp;|&nbsp; {produto.categoria} &nbsp;|&nbsp; {produto.info_extra()}")
            st.caption(status)

        with col_acao:
            if produto.estoque > 0:
                quantidade = st.number_input(
                    "Qtd",
                    min_value=1,
                    max_value=produto.estoque,
                    value=1,
                    key=f"qtd_{produto.id}",
                )
                if st.button("Adicionar ao carrinho", key=f"add_{produto.id}"):
                    sucesso, mensagem = loja.adicionar_ao_carrinho(produto.id, quantidade)
                    if sucesso:
                        st.success(mensagem)
                    else:
                        st.error(mensagem)
            else:
                st.warning("Fora de estoque")

        st.markdown("---")


# ════════════════════════════════════════════════════════════════════════════
# ABA 2 — CARRINHO
# ════════════════════════════════════════════════════════════════════════════
with aba_carrinho:
    st.header("Seu Carrinho")

    carrinho = loja.carrinho

    if carrinho.esta_vazio():
        st.info("Seu carrinho está vazio. Adicione produtos no Catálogo!")
    else:
        for produto_id, item in carrinho.itens.items():
            produto = item["produto"]
            quantidade_atual = item["quantidade"]

            col_nome, col_qtd, col_preco, col_remover = st.columns([3, 1, 1, 1])

            with col_nome:
                st.markdown(f"**{produto.nome}**")
                st.caption(f"R$ {produto.preco:.2f} cada")

            with col_qtd:
                nova_qtd = st.number_input(
                    "Qtd",
                    min_value=1,
                    max_value=produto.estoque + quantidade_atual,
                    value=quantidade_atual,
                    key=f"carrinho_qtd_{produto_id}",
                )
                if nova_qtd != quantidade_atual:
                    diferenca = nova_qtd - quantidade_atual
                    if diferenca > 0:
                        loja.adicionar_ao_carrinho(produto_id, diferenca)
                    else:
                        loja.remover_do_carrinho(produto_id, abs(diferenca))
                    st.rerun()

            with col_preco:
                st.markdown(f"**R$ {produto.preco * quantidade_atual:.2f}**")

            with col_remover:
                if st.button("🗑 Remover", key=f"rem_{produto_id}"):
                    loja.remover_do_carrinho(produto_id)
                    st.rerun()

        st.markdown("---")

        # Cupom
        st.subheader("Cupom de Desconto")
        col_cupom, col_btn_cupom = st.columns([3, 1])
        with col_cupom:
            codigo_cupom = st.text_input(
                "Código do cupom",
                placeholder="Ex: PROMO20",
                label_visibility="collapsed",
            )
        with col_btn_cupom:
            if st.button("Aplicar cupom"):
                if codigo_cupom.strip():
                    sucesso, mensagem = loja.aplicar_cupom(codigo_cupom)
                    if sucesso:
                        st.success(mensagem)
                    else:
                        st.error(mensagem)
                else:
                    st.warning("Digite um código de cupom.")

        if carrinho.cupom:
            st.info(f"Cupom **{carrinho.cupom}** aplicado — {carrinho.percentual_desconto:.0f}% de desconto")

        # Resumo
        st.markdown("---")
        st.subheader("Resumo do Pedido")

        col_resumo, col_finalizar = st.columns([2, 1])

        with col_resumo:
            st.markdown(f"Subtotal: **R$ {carrinho.subtotal():.2f}**")
            if carrinho.percentual_desconto > 0:
                st.markdown(f"Desconto ({carrinho.percentual_desconto:.0f}%): **- R$ {carrinho.valor_desconto():.2f}**")
            st.markdown(f"### Total: R$ {carrinho.total():.2f}")

        with col_finalizar:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Finalizar Pedido", type="primary", use_container_width=True):
                sucesso, resultado = loja.finalizar_pedido()
                if sucesso:
                    st.success(f"Pedido #{resultado.numero:04d} realizado com sucesso!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error(f"Erro ao finalizar: {resultado}")


# ════════════════════════════════════════════════════════════════════════════
# ABA 3 — HISTÓRICO
# ════════════════════════════════════════════════════════════════════════════
with aba_historico:
    st.header("Histórico de Pedidos")

    historico = loja.historico

    if not historico:
        st.info("Nenhum pedido realizado ainda.")
    else:
        for pedido in reversed(historico):
            with st.expander(
                f"Pedido #{pedido.numero:04d} — {pedido.data_hora} — R$ {pedido.total:.2f}",
                expanded=False,
            ):
                for item in pedido.itens:
                    st.markdown(
                        f"- {item['quantidade']}x **{item['nome']}** "
                        f"— R$ {item['preco_unitario']:.2f} cada "
                        f"= R$ {item['subtotal_item']:.2f}"
                    )
                st.markdown("---")
                st.markdown(f"Subtotal: R$ {pedido.subtotal:.2f}")
                if pedido.cupom:
                    st.markdown(f"Cupom {pedido.cupom} (-{pedido.percentual_desconto:.0f}%): - R$ {pedido.valor_desconto:.2f}")
                st.markdown(f"**Total pago: R$ {pedido.total:.2f}**")