from supabase_client import supabase

import pandas as pd
import streamlit as st


def carregar_produtos():

    dados = (

        supabase

        .table("produtos")

        .select("*")

        .order("nome_produto")

        .execute()

    )

    return [

        x["nome_produto"]

        for x in dados.data

    ]


def carregar_pendencias():

    retorno = (

        supabase

        .table("pendencias")

        .select("*")

        .execute()

    )

    return pd.DataFrame(

        retorno.data

    )


def salvar_pendencia(dados):

    supabase.table(

        "pendencias"

    ).insert(

        dados

    ).execute()


def atualizar_pendencia(

    id_pendencia,

    dados

):

    (

        supabase

        .table("pendencias")

        .update(dados)

        .eq(

            "id",

            id_pendencia

        )

        .execute()

    )


def excluir_pendencia(id_p):

    (

        supabase

        .table("pendencias")

        .delete()

        .eq(

            "id",

            id_p

        )

        .execute()

    )


def salvar_entrada_produto(dados):

    (

        supabase

        .table(

            "entrada_produtos"

        )

        .insert(

            dados

        )

        .execute()

    )


def buscar_encomenda_dav(dav):

    response = (

        supabase

        .table(

            "entrada_produtos"

        )

        .select("*")

        .eq(

            "dav",

            dav

        )

        .execute()

    )

    return response.data


def buscar_produto_codigo(codigo):
    try:
        codigo_int = int(str(codigo).strip())  # garante inteiro sem espaços
    except ValueError:
        return ""

    response = (
        supabase
        .table("codigos_produto")
        .select("nome")
        .eq("codigo", codigo_int)
        .execute()
    )

    # Debug: veja o que vem do banco
    print("Resposta Supabase:", response.data)

    if response.data and len(response.data) > 0:
        return response.data[0]["nome"]

    return ""



