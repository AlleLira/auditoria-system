import streamlit as st
import pandas as pd

from datetime import datetime

from config import *
from lojas import LOJAS
from relatorio import gerar_relatorio_imagem
from relatorio_excel import gerar_relatorio_excel

from utils import (
    carregar_pendencias,
    carregar_produtos,
    salvar_pendencia,
    atualizar_pendencia,
    excluir_pendencia,
    salvar_entrada_produto,
    buscar_encomenda_dav,
    buscar_produto_codigo
)

st.set_page_config(
    page_title="Sistema Auditoria",
    layout="wide"
)

aba1, aba2 = st.tabs([

    "📋 Auditoria",

    "📦 Encomenda / Pré-ordem"

])

with aba1:

    st.title("Sistema Auditoria")
    
    if "novo" not in st.session_state:
        st.session_state.novo = False
    
    if "editar" not in st.session_state:
        st.session_state.editar = None
    
    
    @st.cache_data
    def produtos_cache():
    
        return carregar_produtos()
    
    
    produtos = produtos_cache()
    
    hoje = datetime.today()
    
    inicio_mes = hoje.replace(day=1)
    
    dados = carregar_pendencias()
    
    if not dados.empty:
    
        dados["data"] = pd.to_datetime(
            dados["data"],
            utc=True,
            errors="coerce"
        ).dt.tz_localize(None)
    
    col_botao, espaco = st.columns(
        [1,8]
    )
    
    with col_botao:
    
        if st.button(
    
            "Nova Pendência",
    
            type="primary"
    
        ):
    
            st.session_state.novo = True
    
    
    
    
    st.divider()
    
    
    
    col1,col2,col3,col4,col5,col6=st.columns(6)
    
    with col1:
    
        filtro_bloco = st.selectbox(
    
            "Bloco",
    
            ["Todos"] + BLOCOS
    
        )
    
    
    with col2:
    
        lojas = []
    
        if filtro_bloco == "Todos":
    
            for l in LOJAS.values():
    
                lojas.extend(l)
    
        else:
    
            lojas = LOJAS.get(
                filtro_bloco,
                []
            )
    
        filtro_loja = st.selectbox(
    
            "Loja",
    
            ["Todos"] + lojas
    
        )
    
    
    with col5:
    
        data_inicial = st.date_input(
    
            "Inicial",
    
            inicio_mes
    
        )
    
    
    with col6:
    
        data_final = st.date_input(
    
            "Final",
    
            hoje
    
        )
    
    
    if not dados.empty:
    
        dados = dados[
    
            (
                dados["data"]
                >=
                pd.to_datetime(
                    data_inicial
                )
            )
    
            &
    
            (
                dados["data"]
                <=
                pd.to_datetime(
                    data_final
                )
            )
    
        ]
    
    
    consultores = []
    
    temp = dados.copy()
    
    if filtro_bloco != "Todos":
    
        temp = temp[
            temp["bloco"]
            ==
            filtro_bloco
        ]
    
    
    if filtro_loja != "Todos":
    
        temp = temp[
            temp["loja"]
            ==
            filtro_loja
        ]
    
    
    if not temp.empty:
    
        consultores = sorted(
    
            temp["consultor"]
    
            .dropna()
    
            .unique()
    
        )
    
    
    with col3:
    
        filtro_consultor = st.multiselect(
    
            "Consultor",
    
            consultores
    
        )
    
    
    with col4:
    
        filtro_status = st.selectbox(
    
            "Status",
    
            [
    
                "Pendente",
    
                "Finalizado",
    
                "Todos"
    
            ]
    
        )
    
    
    dados_filtrado = dados.copy()
    
    
    if filtro_bloco != "Todos":
    
        dados_filtrado = dados_filtrado[
    
            dados_filtrado["bloco"]
    
            ==
    
            filtro_bloco
    
        ]
    
    
    if filtro_loja != "Todos":
    
        dados_filtrado = dados_filtrado[
    
            dados_filtrado["loja"]
    
            ==
    
            filtro_loja
    
        ]
    
    
    if filtro_consultor:
    
        dados_filtrado = dados_filtrado[
    
            dados_filtrado["consultor"]
    
            .isin(
    
                filtro_consultor
    
            )
    
        ]
    
    
    if filtro_status != "Todos":
    
        dados_filtrado = dados_filtrado[
    
            dados_filtrado["status"]
    
            .fillna("")
    
            .str.upper()
    
            ==
    
            filtro_status.upper()
    
        ]
    
    
    
    if st.session_state.novo:
    
    
        @st.dialog(
            "Nova Pendência"
        )
        def modal():
    
            data = st.date_input(
                "Data"
            )
    
            bloco = st.selectbox(
                "Bloco",
                BLOCOS
            )
    
            loja = st.selectbox(
    
                "Loja",
    
                LOJAS.get(
                    bloco,
                    []
                )
    
            )
    
            consultor = st.text_input(
                "Consultor"
            )
    
            controle = st.text_input(
                "Controle DAV"
            )
    
            tipo = st.selectbox(
                "Tipo",
                TIPOS
            )
    
            valor = st.number_input(
                "Valor",
                min_value=0.0
            )
    
            produto = st.selectbox(
                "Produto",
                produtos
            )
    
            erro = st.selectbox(
                "Erro",
                ERROS
            )
    
            obs = st.text_area(
                "Observação"
            )
    
            salvar = st.button(
                "Salvar"
            )
    
            if salvar:
    
                salvar_pendencia({
    
                    "data":
                    str(data),
    
                    "bloco":
                    bloco,
    
                    "loja":
                    loja,
    
                    "consultor":
                    consultor,
    
                    "controle_dav":
                    controle,
    
                    "produto":
                    produto,
    
                    "erro":
                    erro,
    
                    "tipo":
                    tipo,
    
                    "valor":
                    valor,
    
                    "observacao":
                    obs,
    
                    "status":
                    "Pendente"
    
                })
    
                st.session_state.novo = False
    
                st.rerun()
    
        modal()
    
    
    if not dados_filtrado.empty:
    
        tabela = dados_filtrado.copy()
    
        tabela["data"] = pd.to_datetime(
            tabela["data"]
        ).dt.strftime("%d/%m/%Y")
    
        tabela.insert(
            0,
            "Selecionar",
            False
        )
    
        tabela = st.data_editor(
    
            tabela,
    
            hide_index=True,
    
            use_container_width=True,
    
            disabled=[
    
                c
    
                for c in tabela.columns
    
                if c != "Selecionar"
    
            ]
    
        )
    
        selecionado = tabela[
            tabela["Selecionar"]
        ]
    
    else:
    
        st.warning(
            "Nenhuma pendência encontrada."
        )
    
        selecionado = pd.DataFrame()
    
    
    if len(selecionado) == 1:
    
        linha = selecionado.iloc[0]
    
        c1,c2,c3 = st.columns(3)
    
    
        with c1:
    
            if st.button(
                "Excluir"
            ):
    
                excluir_pendencia(
                    linha["id"]
                )
    
                st.rerun()
    
    
        with c2:
    
            if st.button(
                "Finalizar"
            ):
    
                atualizar_pendencia(
    
                    linha["id"],
    
                    {
    
                        "status":
                        "Finalizado"
    
                    }
    
                )
    
                st.rerun()
    
    
        with c3:
    
            if st.button(
                "Editar"
            ):
    
                st.session_state.editar = linha
    
                st.rerun()
    
    if st.button(
        "📄 Gerar Relatório"
    ):
    
        caminho = gerar_relatorio_imagem(
    
            dados_filtrado,
    
            filtro_bloco,
    
            filtro_loja,
    
            filtro_consultor,
    
            data_inicial,
    
            data_final
    
        )
    
        with open(
            caminho,
            "rb"
        ) as file:
    
            st.download_button(
    
                "⬇️ Download Relatório",
    
                file,
    
                file_name="relatorio.png",
    
                mime="image/png"
    
            )
    
        st.image(caminho)
    
    if st.button(
        "📊 Gerar Excel"
    ):
    
        caminho_excel = gerar_relatorio_excel(
    
            dados_filtrado,
    
            data_inicial
    
        )
    
        with open(
            caminho_excel,
            "rb"
        ) as file:
    
            st.download_button(
    
                "⬇️ Download Excel",
    
                file,
    
                file_name="relatorio_auditoria.xlsx",
    
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    
            )
    
    
    if st.session_state.editar is not None:
    
    
        linha = st.session_state.editar
    
    
        @st.dialog(
            "Editar Pendência"
        )
        def editar_modal():
    
            data = st.date_input(
    
                "Data",
    
                pd.to_datetime(
                    linha["data"]
                )
    
            )
    
            bloco = st.selectbox(
    
                "Bloco",
    
                BLOCOS,
    
                index=BLOCOS.index(
                    linha["bloco"]
                )
    
            )
    
            loja = st.selectbox(
    
                "Loja",
    
                LOJAS.get(
                    bloco,
                    []
                )
    
            )
    
            consultor = st.text_input(
    
                "Consultor",
    
                linha["consultor"]
    
            )
    
            controle = st.text_input(
    
                "Controle DAV",
    
                linha["controle_dav"]
    
            )
    
            valor = st.number_input(
    
                "Valor",
    
                value=float(
                    linha["valor"]
                )
    
            )
    
            obs = st.text_area(
    
                "Observação",
    
                linha["observacao"]
    
            )
    
            if st.button(
    
                "Salvar Alterações"
    
            ):
    
                atualizar_pendencia(
    
                    linha["id"],
    
                    {
    
                        "data":
                        str(data),
    
                        "bloco":
                        bloco,
    
                        "loja":
                        loja,
    
                        "consultor":
                        consultor,
    
                        "controle_dav":
                        controle,
    
                        "valor":
                        valor,
    
                        "observacao":
                        obs
    
                    }
    
                )
    
                st.session_state.editar = None
    
                st.rerun()
    
    
    
    
        editar_modal()

with aba2:

    st.title(
        "Encomendas / Pré-ordens Antigas"
    )


    # CONTROLE DOS POPUPS
    if "abrir_nova_encomenda" not in st.session_state:

        st.session_state.abrir_nova_encomenda = False


    if "abrir_busca_dav" not in st.session_state:

        st.session_state.abrir_busca_dav = False


    col1, col2 = st.columns(2)


    # BOTÃO NOVA ENTRADA
    with col1:

        if st.button(
            "➕ Nova Entrada"
        ):

            st.session_state.abrir_nova_encomenda = True


    # BOTÃO BUSCAR DAV
    with col2:

        if st.button(
            "🔎 Buscar DAV"
        ):

            st.session_state.abrir_busca_dav = True


    # MODAL NOVA ENCOMENDA
    if st.session_state.abrir_nova_encomenda:


        @st.dialog(
            "Cadastrar Encomenda"
        )
        def modal_encomenda():

            bloco = st.selectbox(

                "Bloco",

                BLOCOS

            )


            loja = st.selectbox(

                "Loja",

                LOJAS.get(
                    bloco,
                    []
                )

            )


            data = st.date_input(
                "Data"
            )


            dav = st.text_input(
                "DAV"
            )


            codigo = st.text_input(
                "Código Produto"
            )


            produto = ""


            if codigo:

                produto = buscar_produto_codigo(
                    codigo
                )


            st.text_input(

                "Produto",

                produto,

                disabled=True

            )


            quantidade = st.number_input(

                "Quantidade",

                min_value=1,

                step=1

            )


            col_salvar, col_cancelar = st.columns(2)


            with col_salvar:

                if st.button(
                    "Salvar"
                ):

                    salvar_entrada_produto(

                        {

                            "bloco":
                            bloco,

                            "loja":
                            loja,

                            "data":
                            str(data),

                            "dav":
                            dav,

                            "codigo":
                            codigo,

                            "produto":
                            produto,

                            "quantidade":
                            quantidade

                        }

                    )

                    st.session_state.abrir_nova_encomenda = False

                    st.success(
                        "Cadastro realizado!"
                    )

                    st.rerun()


            with col_cancelar:

                if st.button(
                    "Cancelar"
                ):

                    st.session_state.abrir_nova_encomenda = False

                    st.rerun()


        modal_encomenda()


    # MODAL BUSCA DAV
    if st.session_state.abrir_busca_dav:


        @st.dialog(
            "Buscar Encomenda"
        )
        def buscar_modal():

            dav_busca = st.text_input(
                "Digite a DAV"
            )


            if st.button(
                "Buscar"
            ):

                resultado = buscar_encomenda_dav(
                    dav_busca
                )


                if resultado:

                    df = pd.DataFrame(
                        resultado
                    )

                    df["data"] = pd.to_datetime(

                        df["data"]

                    ).dt.strftime(
                        "%d/%m/%Y"
                    )

                    st.dataframe(

                        df,

                        use_container_width=True

                    )

                else:

                    st.warning(
                        "Nenhuma DAV encontrada"
                    )


            if st.button(
                "Fechar"
            ):

                st.session_state.abrir_busca_dav = False

                st.rerun()


        buscar_modal()
    
