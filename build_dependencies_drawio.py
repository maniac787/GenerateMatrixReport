from datetime import datetime

import pandas as pd
from pandas import DataFrame

import utilitario


def __build_drawio(df: DataFrame, satelite_name: str):
    # Plantilla básica de Draw.io XML
    drawio_template = """<mxGraphModel dx="1098" dy="585" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" math="0" shadow="0">
            <root>
                <mxCell id="0"/>
                <mxCell id="1" parent="0"/>
                {cells}
            </root>
        </mxGraphModel>"""

    # Generar las celdas para Draw.io
    cells = []
    x_offset = 100
    y_offset = 100
    step = 150

    # Crear nodos únicos y sus posiciones
    unique_nodes = pd.concat([df['Origen'], df['Destino']]).unique()
    node_positions = {node: (x_offset, i * step + y_offset) for i, node in enumerate(unique_nodes)}

    for node, (x, y) in node_positions.items():
        cells.append(
            f'<mxCell id="{node}" value="{node}" style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="1">'
            f'<mxGeometry x="{x}" y="{y}" width="120" height="60" as="geometry"/>'
            f'</mxCell>'
        )

    # Crear conexiones (aristas)
    for index, row in df.iterrows():
        source, destination = row['Origen'], row['Destino']
        connection_id = f"edge-{index}"
        cells.append(
            f'<mxCell id="{utilitario.normalize_name(connection_id)}" value="{utilitario.normalize_name(row["Tipo conexion"])}" style="edgeStyle=elbowEdgeStyle;rounded=1;" edge="1" parent="1" source="{source}" target="{destination}">'
            f'<mxGeometry relative="1" as="geometry"/>'
            f'</mxCell>'
        )

    # Formatear todo el XML
    drawio_content = drawio_template.format(cells="\n".join(cells))

    # Obtener la fecha actual
    fecha_actual = datetime.now()

    # Formatear la fecha
    fecha_formateada = fecha_actual.strftime("%d%m%Y-%H_%M_%S")

    if (satelite_name):
        satelite_name = satelite_name + '_'
    else:
        satelite_name = 'global_'
    # Guardar el archivo
    output_file = f'result/integracion/{satelite_name}{fecha_formateada}.drawio'
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(drawio_content)

    print(f"Diagrama generado y guardado como {output_file}")


if __name__ == '__main__':
    # Leer el archivo Excel
    excel_file = "./raw/Matriz PoV Satélites (INTERNO).xlsx"  # Cambia esto por el nombre de tu archivo
    df = pd.read_excel(excel_file, sheet_name="28_NOV_Feedback_Integraciones")

    df_origen = utilitario.unique_values(df, "Origen")
    df_destino = utilitario.unique_values(df, "Destino")
    df_destino = df_destino.rename(columns={"Destino": "Origen"})
    df_result = pd.concat([df_origen, df_destino])
    df_result = utilitario.unique_values(df_result, 'Origen')

    for id, row in df_result.iterrows():
        satelite_iter = row[0]
        df_filtro = df[(df['Origen'] == satelite_iter) | (df['Destino'] == satelite_iter)]
        # Diagrama por satelite individual
        __build_drawio(df_filtro, satelite_iter)
