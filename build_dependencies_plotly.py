import networkx as nx
import pandas as pd
import plotly.graph_objects as go

if __name__ == '__main__':
    # generate_mermaid_code(df)

    # Leer datos desde un archivo Excel
    df_raw = pd.read_excel('./raw/Matriz PoV Satélites (INTERNO).xlsx', sheet_name="dynamic-resultado-matriz", usecols='A:C')
    df = df_raw[df_raw[f'Origen'] == 'SGS']
    # Crear el grafo dirigido
    G = nx.DiGraph()

    # Agregar nodos y aristas
    for _, row in df.iterrows():
        if pd.notna(row["Origen"]) and pd.notna(row["Tipo conexion"]) and pd.notna(row["Destino"]):
            origen = row["Origen"]  # Asegúrate de que los nombres de las columnas coincidan con el archivo Excel
            tipo_conexion = row["Tipo conexion"]
            destino = row["Destino"]
            G.add_edge(origen, destino, tipo=tipo_conexion)

    # Posiciones de los nodos
    pos = nx.spring_layout(G, seed=42)  # Genera posiciones para los nodos

    # Extraer las posiciones para los nodos
    x_nodes = [pos[node][0] for node in G.nodes()]
    y_nodes = [pos[node][1] for node in G.nodes()]

    # Crear los trazos para las aristas
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    # Crear las aristas como líneas
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='gray'),
        hoverinfo='none',
        mode='lines')

    # Crear los nodos como puntos
    node_trace = go.Scatter(
        x=x_nodes, y=y_nodes,
        mode='markers+text',
        text=[f"{node}" for node in G.nodes()],
        textposition="top center",
        marker=dict(
            size=15,
            color='lightblue',
            line=dict(width=2, color='black')
        ),
        hoverinfo='text'
    )

    # Añadir los datos al gráfico
    fig = go.Figure(data=[edge_trace, node_trace])

    # Personalizar el diseño
    fig.update_layout(
        showlegend=False,
        title="Mapa de Dependencias Interactivo",
        titlefont_size=16,
        margin=dict(l=0, r=0, t=40, b=0),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
    )

    # Guardar como archivo HTML
    ruta_html = "./result/mapa_dependencias_interactivo.html"  # Cambia la ruta si es necesario
    fig.write_html(ruta_html)
    print(f"El mapa de dependencias interactivo se guardó como '{ruta_html}'")
