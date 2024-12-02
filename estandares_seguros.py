import pandas as pd

if __name__ == '__main__':
    df = pd.read_excel('./raw/Pacifico-Template-Habilitadores_Seguros.xlsx',
                       sheet_name="Habilitadores Cloud", usecols='A:C')

    # Mantener columna como DataFrame con valores únicos
    valores_unicos_df = df[['Dimensión']].drop_duplicates()

    # Aplicar distinct por las columnas "Dimensión" y "Dominio"
    df_distinct = df[['Dimensión', 'Dominio']].drop_duplicates()
    df_distinct_dominio = df[['Dominio']].drop_duplicates()

    # Mostrar el resultado
    print(df_distinct)
    print("**************************")
    print(valores_unicos_df)

    valores_unicos_df.to_csv('./result/seguridad_seguros_1.csv', index=False)
    df_distinct.to_csv('./result/seguridad_seguros_2.csv', index=False)
    df_distinct_dominio.to_csv('./result/seguridad_seguros_3.csv', index=False)
