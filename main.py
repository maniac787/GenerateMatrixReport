import pandas as pd

if __name__ == '__main__':

    # Cargar el archivo Excel
    # 'ruta_del_archivo.xlsx' con la ruta real de tu archivo
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

    # Mostrar el resultado
    print(df_detalle)

    df_detalle.to_excel('./raw/detalle_dependencias.xlsx', index=False)
