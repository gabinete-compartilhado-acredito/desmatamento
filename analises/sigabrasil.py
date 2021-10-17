import pandas as pd
import matplotlib.pyplot as pl
from glob import glob

import utils as xu


def load_sigabrasil_file(filename, drop_month_0=True):
    """
    Load SIGABrasil data stored in a XLS file.
    
    The data is supposed to be obtained from 
    the Painel Especialista in SIGA Brasil 
    website.
    """
    
    # Carregando os dados:
    siga = pd.read_excel(filename)
    
    # Limpeza:
    siga = siga.iloc[1:].reset_index(drop=True)
    siga['Mês (Número) DES'] = siga['Mês (Número) DES'].astype(int)
    if drop_month_0:
        siga = siga.loc[siga['Mês (Número) DES'] != 0]
    siga['Ano'] = siga['Ano'].astype(int)
    #siga['Subfunção (Cod) (Ajustado)'] = siga['Subfunção (Cod) (Ajustado)'].astype(int)
    #siga['Função (Cod) DESP'] = siga['Função (Cod) DESP'].astype(int)
    
    return siga


def load_sigabrasil(file_pattern, drop_month_0=True):
    """
    Load SIGABrasil data stored in multiple XLS
    files, following the glob pattern `file_pattern`
    (str).
    """
    
    file_list = sorted(glob(file_pattern))

    siga = pd.concat([load_sigabrasil_file(filename, drop_month_0) for filename in file_list], ignore_index=True)

    return siga


def deflate_values(siga_df, ipca_df):
    """
    Given a DataFrame `siga_df` with orçamento monthly 
    data from SIGA Brasil, add to it deflated columns 
    according to monthly IPCA DataFrame `ipca_df`.
    
    Return the modified DataFrame.
    """
    
    # Add data column:
    siga_df['data'] = pd.to_datetime(siga_df['Ano'].astype(str) + '-' + siga_df['Mês (Número) DES'].apply(lambda x: '{:02d}'.format(x)) + '-01')

    # Join IPCA:
    n_siga_0 = len(siga_df)
    siga_df = siga_df.join(ipca_df.set_index('mes'), how='left', on='data')
    assert len(siga_df) == n_siga_0, 'Join increased the number of rows.'

    # Get columns with values:
    value_cols = list(filter(lambda s: s.find('(R$)') != -1, siga_df.columns))

    # Compute real values (corrected for inflation):
    ipca_last = siga_df.loc[~siga_df['ipca'].isnull()].sort_values('data', ascending=False).iloc[0]['ipca']
    for col in value_cols:
        siga_df[col + ' IPCA'] = siga_df[col] / siga_df['ipca'] * ipca_last

    assert siga_df[[col + ' IPCA' for col in value_cols]].isna().sum().sum() == 0, 'Valores faltando nos R$ ajustados pelo IPCA: atualizar a base de IPCA ou extrapolar até a última data do orçamento'

    return siga_df


def std_orgaos(siga_df):
    """
    Add columns to DataFrame `siga_df` of 
    orçamento federal extracted from SIGA Brasil
    containing standardized (and grouped) ministries
    names according to hard-coded dicts.
    """
    
    # Standardizing dict (órgãos superiores):
    ministerio_dict = {
        'MINIST.DA CIENCIA,TECNOL.,INOV.E COMUNICACOES':'MINISTERIO DA CIENCIA E TECNOLOGIA',
        'MINISTERIO DA CIENCIA, TECNOLOGIA E INOVACAO': 'MINISTERIO DA CIENCIA E TECNOLOGIA',
        'MINISTERIO DA CIENCIA, TECNOLOGIA E INOVACOES': 'MINISTERIO DA CIENCIA E TECNOLOGIA',
        'MINISTERIO DA INTEGRACAO NACIONAL': 'MINISTERIO DO DESENVOLVIMENTO REGIONAL',
        'MINISTERIO DA JUSTICA E CIDADANIA': 'MINISTERIO DA JUSTICA',
        'MINISTERIO DA JUSTICA E SEGURANCA PUBLICA': 'MINISTERIO DA JUSTICA',
        'MINIST. DO PLANEJAMENTO, DESENVOLV. E GESTAO': 'MINISTERIO DA ECONOMIA',
        'MINISTERIO DO PLANEJAMENTO,ORCAMENTO E GESTAO': 'MINISTERIO DA ECONOMIA',
        'MINISTERIO DA FAZENDA':'MINISTERIO DA ECONOMIA',
        'MINISTERIO DO TRABALHO E EMPREGO':'MINISTERIO DA ECONOMIA',
        'MINISTERIO DA PESCA E AQÜICULTURA':'MINISTERIO DA AGRICULTURA, PECUARIA E ABASTECIMENTO',
        'MINIST. DA AGRICUL.,PECUARIA E ABASTECIMENTO':'MINISTERIO DA AGRICULTURA, PECUARIA E ABASTECIMENTO'
    }
    # Standardizing dict (órgão):
    orgao_dict = {
        'COMPANHIA DE DESENV. DO VALE DO SAO FRANCISCO':'CIA.DE DES.DOS VALES DO S.FRANC.E DO PARNAIBA',
        'MINIST. DA AGRICUL.,PECUARIA E ABASTECIMENTO':'MINISTERIO DA AGRICULTURA, PECUARIA E ABASTECIMENTO',
        'MINIST. DO PLANEJAMENTO, DESENVOLV. E GESTAO':'MINISTERIO DA ECONOMIA',
        'MINISTERIO DO PLANEJAMENTO,ORCAMENTO E GESTAO': 'MINISTERIO DA ECONOMIA',
        'MINIST.DA CIENCIA,TECNOL.,INOV.E COMUNICACOES':'MINISTERIO DA CIENCIA E TECNOLOGIA',
        'MINISTERIO DA CIENCIA, TECNOLOGIA E INOVACAO':'MINISTERIO DA CIENCIA E TECNOLOGIA',
        'MINISTERIO DA INTEGRACAO NACIONAL':'MINISTERIO DO DESENVOLVIMENTO REGIONAL',
        'MINISTERIO DA FAZENDA':'MINISTERIO DA ECONOMIA',
        'MINISTERIO DO TRABALHO E EMPREGO':'MINISTERIO DA ECONOMIA',
        'MINISTERIO DA JUSTICA E CIDADANIA':'MINISTERIO DA JUSTICA',
        'MINISTERIO DA JUSTICA E SEGURANCA PUBLICA':'MINISTERIO DA JUSTICA',
        'MINISTERIO DA PESCA E AQÜICULTURA':'MINISTERIO DA AGRICULTURA, PECUARIA E ABASTECIMENTO'
    }
    
    # Standardize:
    siga_df['Órgão Superior (UG) STD'] = siga_df['Órgão Superior (UG) DESP'].map(xu.translate_dict(ministerio_dict))
    siga_df['Órgão (UG) STD'] = siga_df['Órgão (UG) DESP'].map(xu.translate_dict(orgao_dict))
    
    return siga_df


def project_ipca(ipca, final_date):
    """
    Return a DataFrame that extrapolates 
    `ipca` (DataFrame containing months and
    IPCA in decreasing chronological order)
    up to date `final_date`.
    """
    
    # Compute the average IPCA fractional increase in the last 12 months:
    avg_ipca = (ipca['ipca'] / ipca['ipca'].shift(-1)).iloc[:12].mean()
    
    # Build a monthly sampled dates, from last one in `ipca` up to `final_date`:
    last_date = ipca['mes'].max()
    dates = pd.date_range(last_date, final_date, freq='M') + pd.DateOffset(days=1)
    
    # Use avg. IPCA to extrapolate:
    last_ipca = ipca.loc[ipca['mes'] == last_date, 'ipca'].iloc[0]
    proj_ipca = last_ipca * pd.Series([avg_ipca] * len(dates)).cumprod()

    # Build DataFrame:
    proj_df = pd.DataFrame()
    proj_df['mes'] = dates
    proj_df['ipca'] = proj_ipca
    proj_df = proj_df.sort_values('mes', ascending=False)
    
    return proj_df


def complement_ipca(ipca, final_date):
    """
    Extend `ipca` (DataFrame) up to 
    `final_date`.
    """
    # Get extrapolation for IPCA:
    proj  = project_ipca(ipca, final_date)
    # Concatenate to existing data:
    compl = pd.concat([proj, ipca], ignore_index=True)
    
    return compl


def etl_sigabrasil(file_pattern, ipca_file, verbose=True):
    """
    Load SIGA Brasil orçamento data from glob pattern 
    `file_pattern` (str), deflate them using IPCA data 
    from `ipca_file` (str) and standardize órgão names.
    """
    
    # Load orçamento data:
    siga_df = load_sigabrasil(file_pattern)

    # Find the most recent month in the SIGA data:
    last_entry = siga_df.sort_values(['Ano', 'Mês (Número) DES']).iloc[-1]
    final_ipca_date = '{}-{:02d}-01'.format(last_entry['Ano'], last_entry['Mês (Número) DES'])

    # Load IPCA:
    ipca_df = xu.load_data_from_local_or_bigquery('SELECT * FROM `gabinete-compartilhado.bruto_gabinete_administrativo.ipca`', ipca_file)
    ipca_df['mes'] = pd.to_datetime(ipca_df['mes'])
    if verbose:
        print('Last IPCA date: ', ipca_df['mes'].max().date())

    # Extrapolate IPCA:
    ipca_df = complement_ipca(ipca_df, final_ipca_date)

    # Deflate SIGA values:
    siga_df = deflate_values(siga_df, ipca_df)
    
    # Standardize órgãos names:
    siga_df = std_orgaos(siga_df)
    
    return siga_df



def remove_unwanted_siga_data(siga_df, keep_only_executado=True, remove_funcoes=True, remove_elemento_despesa=True, remove_gnd=True):
    """
    Remove rows from SIGA Brasil DataFrame `siga_df`
    based on the specified requirements.
    """
    
    # Start with the input data:
    out_df = siga_df
    
    # Only keep rows with info about despesas executadas:
    if keep_only_executado:
        out_df = out_df.loc[out_df['Despesa Executada (R$) IPCA'] != 0]
    
    # Remove expenses with previdência social:
    if remove_funcoes:
        out_df = out_df.loc[~out_df['Função DESP'].isin(['PREVIDÊNCIA SOCIAL', 'ENCARGOS ESPECIAIS'])]
    
    # Remove expenses with court-mandated payments:
    if remove_elemento_despesa:
        out_df = out_df.loc[~out_df['Elemento Despesa DESP'].isin(['SENTENCAS JUDICIAIS', 'AUXÍLIO FINANCEIRO A PESQUISADORES', 'AUXÍLIO FINANCEIRO A ESTUDANTES', 
                                                                   'PREMIAÇÕES CULTURAIS, ARTÍSTICAS, CIENTÍFICAS, DESPORTIVAS E OUTRAS', 'PENSOES ESPECIAIS', 
                                                                   'DEPOSITOS COMPULSORIOS', 'EQUALIZAÇÃO DE PREÇOS E TAXAS'])]
    
    # Remove expenses with public servants:
    if remove_gnd:
        out_df = out_df.loc[~out_df['GND DESP'].isin(['PESSOAL E ENCARGOS SOCIAIS', 'JUROS E ENCARGOS DA DIVIDA', 'RESERVA DE CONTINGENCIA', 'AMORTIZACAO DA DIVIDA'])]
        
    return out_df


def count_by_category(siga, col):
    """
    Return a dataframe with number of 
    entries and their aggregated value
    (realizado) for data grouped by 
    `col`.
    """
    df = pd.DataFrame()
    n = siga.groupby(col).size()
    df['n_registros'] = n
    v = siga.groupby(col)['Despesa Executada (R$) IPCA'].sum()
    df['valor_realizado'] = v
    return df.sort_values('valor_realizado', ascending=False)


def count_by_col_pos(df, pos):
    """
    Return a DataFrame with the 
    number of entries in `df` 
    and their aggregated values
    grouped by `df` column at 
    position `pos`.
    """
    return count_by_category(df, df.columns[pos])


def sample_by_valor(df, n_samples=5, abs_weight=True, weight_col='Despesa Executada (R$) IPCA'):
    """
    Sample instances from `df` using weights given 
    by `weight_col`. If `abs_weight` is True, use 
    the absolute value of `weight_col` as weight
    (to deal with negative values). Otherwise, 
    ignore negative values.
    """
    
    if abs_weight:
        weights = df[weight_col].clip(lower=0.0)
    else:
        weights = df[weight_col].abs()

    sample = df.sample(n_samples, weights=weights)
    
    return sample


def value_timeseries(df, groupby, vcol='Despesa Executada (R$) IPCA', drop_last=False):
    """
    Sum all values in column `vcol` (str) of `df`
    (DataFrame) for groups grouped by `groupby` 
    (str) column. If `drop_last` (bool) is True,
    ignore the last group.
    
    Return a series with `groupby` as index 
    and aggregated `vcol` as values.
    """
    
    # Aggregate values:
    series = df.groupby(groupby)[vcol].sum()

    if drop_last:
        series = series.sort_index().iloc[:-1]
    else:
        series = series.sort_index()

    return series


def plot_value_timeseries(df, x_axis, label=None, color=None, kind='line', sum_y='Despesa Executada (R$) IPCA', drop_last=False, scale_factor=1.0, linestyle=None):
    """
    Plot the aggregated values of column `sum_y` 
    (str) as a function of column `x_axis`, both
    of DataFrame `df`. If `drop_last` is True, 
    drop the last entry from the plot.
    """
    
    series = value_timeseries(df, x_axis, sum_y, drop_last) * scale_factor
    
    series.plot(kind=kind, label=label, color=color, linestyle=linestyle)
    pl.ylabel(sum_y, fontsize=12)
    pl.tick_params(labelsize=12)



def plot_expenditure(df, label=None, title=None, sum_y='Despesa Executada (R$) IPCA'):
    """
    Plot the values of `df` (DataFrame) column
    `sum_y` aggregated by month (left plot) and
    year (right plot).
    """
    
    pl.figure(figsize=(20,4))
    
    pl.subplot(1,2,1)
    plot_value_timeseries(df, 'data', label=label, sum_y=sum_y, drop_last=True)
    pl.grid()
    if type(label) != type(None):
        pl.legend()

    pl.subplot(1,2,2)
    plot_value_timeseries(df, 'Ano', kind='bar', label=label, color='lightblue', sum_y=sum_y, drop_last=True)
    if type(label) != type(None):
        pl.legend()
        
    if type(title) != type(None):
        pl.suptitle(title, fontsize=16, fontweight='bold')
        
    pl.show()
