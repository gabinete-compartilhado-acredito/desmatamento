import pandas as pd
import re


# Prodes data columns with areas (km2):
areas_col = ['Incremento', 'AreaKm2', 'Desmatado', 'Floresta', 'Nuvem', 'NaoObservado', 'NaoFloresta', 'Hidrografia', 'Desmatavel', 'Disponivel']


def load_one_prodes_csv(prefix, year, std_cols=True, extension='.txt'):
    """
    Load deflorestation INPE Prodes Data
    from a CSV file with prefix (including
    path) `prefix` (str), for the `year`
    (int), assuming the year appears in the 
    filename right after prefix and before
    `extension` (str).
    
    If `std_cols` is True, standardize the 
    column names by trimming the columns and
    removing references to years.
    
    Returns a DataFrame.
    """
    
    # Load data:
    df = pd.read_csv('{}{}{}'.format(prefix, year, extension), encoding='latin-1')
    orig_cols = list(df.columns)
    
    if std_cols:
        new_cols = [re.sub(r'\d{4,}', '', col).strip() for col in orig_cols]
        col_dict = dict(zip(orig_cols, new_cols))
        df.rename(col_dict, axis=1, inplace=True)
    else:
        new_cols = orig_cols
        
    # Add year column:
    df['Ano'] = year
    
    return df[['Ano'] + new_cols]


def load_prodes_csv_data(prefix, first_year, last_year, extension='.txt'):
    """
    Load deflorestation INPE Prodes Data
    from CSV files with prefix (including
    path) `prefix` (str), for years from 
    `first_year` (int) to `last_year` (int)
    (inclusive).
    """
    
    # Carrega dados:
    df = pd.concat([load_one_prodes_csv(prefix, year, extension) for year in range(first_year, last_year + 1)], ignore_index=True)
    
    return df


def add_prodes_extra_cols(df):
    """
    Add new columns to a Prodes deflorestation 
    dataset `df`, computed from the original 
    columns.
    
    Returns a DataFrame.
    """
    
    # Toda a área de floresta + a já desmatada:
    df['Desmatavel'] = (df['AreaKm2'] - df['NaoFloresta'] - df['Hidrografia']).clip(lower=0)
    # A área de floresta no ano anterior:
    df['Disponivel'] = df['Floresta'] + df['Incremento']
    df['frac_desmatavel'] = df['Incremento'] / df['Desmatavel']
    df['frac_area'] = df['Incremento'] / df['AreaKm2']
    
    return df


def etl_prodes_data(prefix, first_year, last_year, extension='.txt'):
    """
    Load, clean and process Prodes deflorestation
    data.
    """
    
    # Load data:
    df = load_prodes_csv_data(prefix, first_year, last_year, extension)
    # Add new columns:
    df = add_prodes_extra_cols(df)
    
    return df


def date_series_to_ano_prodes(series):
    """
    Translate a datetime Series `series`
    into a Prodes year. The Prodes year 
    Y goes from 01/08/Y-1 to 31/07/Y.
    """
    return series.dt.year + (series.dt.month >= 8).astype(int)
