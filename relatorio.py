import pandas as pd
import matplotlib.pyplot as plt


def gerar_relatorio_imagem(

    df,

    filtro_bloco,

    filtro_loja,

    filtro_consultor,

    data_inicial,

    data_final

):

    if df.empty:

        return None


    df = df.copy()


    df["data"] = pd.to_datetime(
        df["data"]
    ).dt.strftime("%d/%m/%Y")


    colunas = [

        "data",
        "controle_dav",
        "consultor",
        "produto",
        "erro",
        "tipo"

    ]


    if not filtro_consultor:

        colunas.append(
            "valor"
        )


    colunas.append(
        "observacao"
    )


    tabela = df[colunas]


    tabela.columns = [

        "DATA",
        "DAV"
        "CONSULTOR",
        "PRODUTO",
        "ERRO",
        "TIPO",

        *(
            ["VALOR"]
            if not filtro_consultor
            else []
        ),

        "OBSERVAÇÃO"

    ]


    qtd_linhas = len(tabela)


    altura = max(
        4,
        qtd_linhas * 0.45
    )


    fig, ax = plt.subplots(

        figsize=(20, altura)

    )


    ax.axis("off")


    fig.text(

        0.02,

        0.96,

        "RELATÓRIO DE PENDÊNCIAS",

        fontsize=30,

        fontweight="bold",

        ha="left"

    )


    fig.text(

        0.02,

        0.86,

        f"Período: "

        f"{data_inicial.strftime('%d/%m/%Y')}"

        f" até "

        f"{data_final.strftime('%d/%m/%Y')}",

        fontsize=20,

        fontweight="bold",

        ha="left"

    )

    if filtro_consultor:

        larguras = [

            0.10,  # DATA
            0.12,  # DAV
            0.33,  # CONSULTOR
            0.20,  # PRODUTO
            0.15,  # ERRO
            0.10,  # TIPO
            0.20   # OBS

        ]

    else:

        larguras = [

            0.10,  # DATA
            0.10,  # DAV
            0.25,  # CONSULTOR
            0.15,  # PRODUTO
            0.13,  # ERRO
            0.10,  # TIPO
            0.10,  # VALOR
            0.20   # OBS

        ]

    table = ax.table(

        cellText=tabela.values,

        colLabels=tabela.columns,

        loc="upper left",

        cellLoc="left",

        colWidths=larguras

    )


    table.auto_set_font_size(
        False
    )


    table.set_fontsize(11)


    table.scale(
        1,
        2
    )


    for (row,col), cell in table.get_celld().items():

        cell.set_edgecolor(
            "#BFBFBF"
        )


        if row == 0:

            cell.set_text_props(

                weight='bold',

                color='white'

            )

            cell.set_facecolor(
                '#ED7D31'
            )

            cell.set_height(
                0.08
            )

        else:

            if row % 2 == 0:

                cell.set_facecolor(
                    '#F8F8F8'
                )

            else:

                cell.set_facecolor(
                    'white'
                )


    caminho = "relatorio.png"


    plt.subplots_adjust(

        left=0.01,

        right=0.99,

        top=0.82,

        bottom=0.02

    )
    plt.savefig(

        caminho,

        bbox_inches="tight",

        dpi=300,

        pad_inches=0.3

    )


    plt.close()


    return caminho
