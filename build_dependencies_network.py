import pandas as pd
from pyvis.network import Network

if __name__ == '__main__':

    if __name__ == '__main__':
        # Leer datos desde la hoja específica
        # datos = pd.read_excel('./raw/matrix_pov.xlsx', sheet_name="dynamic-resultado-matriz", usecols='A:C')
        datos = pd.read_excel('./raw/matrix_pov.xlsx', sheet_name="dynamic-resultado-matriz")

        # Crear el grafo interactivo
        net = Network(height="800px", width="100%", notebook=True)

        # Agregar nodos y aristas
        for _, fila in datos.iterrows():
            if pd.notna(fila["Origen"]) and pd.notna(fila["Tipo conexion"]) and pd.notna(fila["Destino"]):
                origen = fila['Origen']
                destino = fila['Destino']
                tipo_conexion = fila['Tipo conexion']
                macro_proceso = fila['Macro proceso']

                # Agregar nodos
                net.add_node(origen, title=origen, label=origen)
                net.add_node(destino, title=destino, label=destino)

                # Agregar aristas con título personalizado
                # 'title' aparece cuando pasas el cursor sobre la arista, mostrando la conexión
                net.add_edge(origen, destino,
                             title=f'Tipo de Conexión: {tipo_conexion}<br>Macro Proceso: {macro_proceso}',
                             label=f'{tipo_conexion}')

        # Mostrar el grafo interactivo
        net.show("./result/graph.html")
