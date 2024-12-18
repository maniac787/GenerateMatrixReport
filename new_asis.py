import glob
import os

import pandas as pd
from pandas import DataFrame


def export_csv(data_frame_satelites: DataFrame, dominio: str):
    # Obtener el número de registros
    num_filas = data_frame_satelites.shape[0]
    print(f"Satélites en la infraestructura de {dominio}: {num_filas}")

    print(f"Satélites en la infraestructura de {dominio}")
    print(data_frame_satelites['Satélite'])

    # Exportar a un archivo CSV
    data_frame_satelites['Satélite'].to_csv(f'./result/satelites_infra_{dominio}.csv', index=False)


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
        satelite = row['Satélite']
        if index < num_boxes:
            xml_code += (
                f'\n \t\t\t        <mxCell id="{id}" value="{satelite}" style="rounded=1;whiteSpace=wrap;html=1;{color_style}" vertex="1" parent="1">\n'
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


def generar_reporte(df_excel: DataFrame, columna: str, filtro: str, dominio: str, tipo_reporte: str,
                    style_color_box: str
                    ) -> None:
    df_filtro = df_excel[df_excel[f'{columna}'] == filtro]
    export_csv(df_filtro, f'{dominio}')
    print_box(df_filtro, f'draw_{tipo_reporte}_{dominio}', 100, style_color_box)


if __name__ == '__main__':
    df = pd.read_excel('./raw/ajustes_pov.xlsx',
                       sheet_name="Ajustado",
                       index_col=0,
                       skiprows=1, header=0, nrows=48)
    color_seguros = f'fillColor=#d5e8d4;strokeColor=#82b366;'
    color_salud = f'fillColor=#dae8fc;strokeColor=#6c8ebf;'
    color_externo = f'fillColor=#fff2cc;strokeColor=#d6b656;'

    clear_draw_files()
    # REPORTE para infraestructura de satelite
    generar_reporte(df, 'Infraestructura', 'PAC Seguros', 'seguros', 'infra', color_seguros)
    generar_reporte(df, 'Infraestructura', 'PAC Salud', 'salud', 'infra', color_salud)
    generar_reporte(df, 'Infraestructura', 'O. Externas', 'externo', 'infra', color_externo)
    generar_reporte(df, 'Infraestructura', 'E.Reguladores', 'regulador', 'infra', color_externo)

    # REPORTE para gestion de cambios de satelite
    generar_reporte(df, 'Gestión de Cambios del Satélite', 'PAC Seguros', 'seguros', 'ge_cambio', color_seguros)
    generar_reporte(df, 'Gestión de Cambios del Satélite', 'PAC Salud', 'salud', 'ge_cambio', color_salud)
    generar_reporte(df, 'Gestión de Cambios del Satélite', 'O. Externas', 'externo', 'ge_cambio', color_externo)
    generar_reporte(df, 'Gestión de Cambios del Satélite', 'E.Reguladores', 'regulador', 'ge_cambio', color_externo)

    # REPORTE para gestion de cambios de satelite
    generar_reporte(df, 'Owner del satelite', 'Pacifico Seguros', 'seguros', 'owner', color_seguros)
    generar_reporte(df, 'Owner del satelite', 'Pacifico Salud', 'salud', 'owner', color_salud)
    generar_reporte(df, 'Owner del satelite', 'Externo', 'externo', 'owner', color_externo)
    generar_reporte(df, 'Owner del satelite', 'Pacifico Salud, Pacifico Seguros', 'compartido', 'owner', color_externo)
