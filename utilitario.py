from pandas import DataFrame


def unique_values(df: DataFrame, columna: str) -> DataFrame:
    return df[[columna]].drop_duplicates()
