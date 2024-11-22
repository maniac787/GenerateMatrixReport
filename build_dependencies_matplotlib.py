# Normalizar los nombres de los satélites (reemplazar espacios por guiones bajos)
def normalize_name(name):
    return name.replace("(", "").replace(")", "").replace(" ", "_").replace("|", "/").replace("\n", " / ")


import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

if __name__ == '__main__':
    # Leer datos desde un archivo Excel
    df = pd.read_excel('./raw/Matriz PoV Satélites (INTERNO).xlsx', sheet_name="dynamic-resultado-matriz", usecols='A:C')

    # Crear el grafo dirigido
    G = nx.DiGraph()

    # Agregar nodos y aristas
    for _, row in df.iterrows():
        if pd.notna(row["Origen"]) and pd.notna(row["Tipo conexion"]) and pd.notna(row["Destino"]):
            origen = row["Origen"]  # Asegúrate de que los nombres de las columnas coincidan con el archivo Excel
            tipo_conexion = row["Tipo conexion"]
            destino = row["Destino"]
            G.add_edge(origen, destino, tipo=tipo_conexion)

    # Dibujar el grafo
    plt.figure(figsize=(14, 10))

    # Posiciones de los nodos
    pos = nx.spring_layout(G, seed=42)

    # Dibujar nodos y etiquetas
    nx.draw_networkx_nodes(G, pos, node_size=2000, node_color="lightblue")
    nx.draw_networkx_labels(G, pos, font_size=10, font_color="black")

    # Dibujar aristas
    nx.draw_networkx_edges(G, pos, arrowstyle="->", arrowsize=20)

    # Dibujar etiquetas de las aristas
    edge_labels = nx.get_edge_attributes(G, "tipo")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="red", font_size=8)

    # Mostrar el grafo
    plt.title("Mapa de Dependencias")
    plt.axis("off")
    # Guardar el grafo como imagen
    ruta_imagen = "./result/mapa_dependencias.png"  # Cambia la ruta si es necesario
    plt.savefig(ruta_imagen, format="png", dpi=300, bbox_inches="tight")  # DPI alto para mayor calidad
    plt.close()  # Cerrar la figura después de guardar
    print(f"El mapa de dependencias se guardó como '{ruta_imagen}'")
    plt.show()
