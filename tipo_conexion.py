import glob
import os

import pandas as pd
from pandas import DataFrame

def clear_draw_files():
    # Definir el directorio donde se encuentran los archivos
    directorio = './result'

    # Buscar todos los archivos .drawio en el directorio
    archivos_drawio = glob.glob(os.path.join(directorio, "*.drawio"))

    # Eliminar los archivos encontrados
    for archivo in archivos_drawio:
        os.remove(archivo)
        print(f"Archivo {archivo} eliminado.")


def print_box(satelite_data_frame: DataFrame, file_name: str, position_y: int, color_style: str) -> None:
    xml_template_start = """
        <mxfile>
          <diagram name="Diagrama 1">
            <mxGraphModel dx="600" dy="400" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="800" pageHeight="600">
              <root>
                <mxCell id="0"/>
                <mxCell id="1" parent="0"/>
        """
    xml_template_end = """
              </root>
            </mxGraphModel>
          </diagram>
        </mxfile>
        """
    xml_code = ""
    # xml_code += f'{xml_template_start}'
    pos_y = position_y
    pos_x = 300
    index = 0
    num_boxes = 7
    for id, row in satelite_data_frame.iterrows():
        satelite = row['tipo_conexion']
        if index < num_boxes:
            xml_code += (
                f'\n \t\t\t        <mxCell id="{id+2}" value="{satelite}" style="rounded=1;whiteSpace=wrap;html=1;{color_style}" vertex="1" parent="1">\n'
                f'\t\t\t\t\t\t<mxGeometry x="{pos_x}" y="{pos_y}" width="120" height="60" as="geometry"/>\n'
                f'\t\t\t\t\t</mxCell>\n')
            pos_y += 70
            index += 1
        else:
            pos_y = position_y
            pos_x += 130
            index = 0

    # xml_code += f'{xml_template_end}'

    draw_repot = xml_template_start + xml_code + xml_template_end
    # Guardar el archivo como .drawio
    if xml_code and xml_code.strip():
        with open(f'./result/{file_name}.drawio', "w") as f:
            f.write(draw_repot)

if __name__ == '__main__':
    df = pd.read_csv('./raw/integracion.csv')
    color_salud = f'fillColor=#1ba1e2;strokeColor=#006EAF;fontColor=#ffffff;'
    print_box(df, f'draw_tipo', 100, color_salud)