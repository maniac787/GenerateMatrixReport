import pandas as pd
from pandas import DataFrame


# Normalizar los nombres de los satélites (reemplazar espacios por guiones bajos)
def normalize_name(name):
    return name.replace("(", "").replace(")", "").replace(" ", "_").replace("|", "/").replace("\n", " / ")


def generate_mermaid_code(df_detalle: DataFrame):
    mermaid_code = "```mermaid \n\tgraph TD\n"

    for _, row in df_detalle.iterrows():
        source = normalize_name(row["Nombre satelite"])
        dependency_type = normalize_name(row["Tipo dependencia"])
        target = normalize_name(row["Satelite dependiente"])
        mermaid_code += f'    {source} -->|{dependency_type}| {target}\n'
    mermaid_code += "\n```"
    with open("./result/mermaid_dependencias.md", "w") as file:
        file.write(mermaid_code)

    print(mermaid_code)


if __name__ == '__main__':

    # Cargar el archivo Excel
    df = pd.read_excel('./raw/matrix.xlsx', sheet_name="draft", usecols='B:AX', skiprows=2, header=0,
                       index_col=0)

    # Crear un nuevo DataFrame para almacenar los detalles por satélite
    detalle_dependencias = []

    # Recorrer cada satélite en la fila y columna para identificar dependencias
    for satelite_principal in df.index:
        for satelite_dependiente in df.columns:
            tipo_dependencia = df.loc[satelite_principal, satelite_dependiente]

            # Solo añadimos dependencias que no estén vacías
            if pd.notna(tipo_dependencia):
                detalle_dependencias.append({
                    'Nombre satelite': satelite_principal,
                    'Tipo dependencia': tipo_dependencia,
                    'Satelite dependiente': satelite_dependiente
                })

    # Crear un nuevo DataFrame con los detalles de las dependencias
    df_detalle = pd.DataFrame(detalle_dependencias)
    df_detalle.to_excel('./result/detalle_dependencias.xlsx', index=False)
    generate_mermaid_code(df_detalle)
