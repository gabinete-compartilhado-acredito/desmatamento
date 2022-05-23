import pandas as pd


def date_range(first_date, last_date, freq='D'):
    """
    Return a Pandas sequence of dates within
    the specified range limit.
    
    Parameters
    ----------
    first_date : str ('%Y-%m-%d') or datetime
        Start of the interval from where to 
        get the date range (inclusive).
    last_date : str ('%Y-%m-%d') or datetime
        End of the interval from where to 
        get the date range (inclusive).
    freq : str
        Frequency (i.e. unit of time) used to
        sample the interval. It can be one day
        ('D'), one month ('M'), five days ('5D')
        and so on. If 'M', return the first day 
        of the month for each month in the interval.
    
    Returns
    -------
    dates : DatetimeIndex
        Range of dates contained in the interval
        from `first_date` to `last_date`, both 
        inclusive. If the interval does not start 
        and end at the dates chosen to represent
        each time step (e.g. a month, a week), 
        return the ones contained in the interval,
        e.g.: 
        date_range('2019-01-15', '2019-03-01', 'M')
        returns ['2019-02-01', '2019-03-01'].
    """,
    if freq == 'M':
        first_date = pd.to_datetime(first_date) - pd.DateOffset(days=1)
        dates = pd.date_range(first_date, last_date, freq=freq) + pd.DateOffset(days=1) 
    else: 
        dates = pd.date_range(first_date, last_date, freq=freq)
        
    return dates


def month_name_to_num(month_name):
    """
    Translate a `month_name` (str) to a number (int) from 
    1 to 12. Works with portuguese and english, and with 
    full name and 3-letter abbreviation.
    """
    
    translate_dict = {'jan': 1, 'fev': 2, 'mar': 3, 'abr': 4, 'mai': 5, 'jun': 6, 
                      'jul': 7, 'ago': 8, 'set': 9, 'out': 10, 'nov': 11, 'dez': 12, 
                      'janeiro': 1, 'fevereiro': 2, 'março': 3, 'abril': 4, 'maio': 5, 'junho': 6, 
                      'julho': 7, 'agosto': 8, 'setembro': 9, 'outubro': 10, 'novembro': 11, 'dezembro': 12, 
                      'marco': 3, 'feb': 2, 'apr': 4, 'may': 5, 'aug': 8, 'sep': 9, 'oct': 10, 'dec': 12, 
                      'january': 1, 'february': 2, 'march': 3, 'april': 4, 'june': 6, 
                      'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november': 11, 'december': 12}
    
    return translate_dict[month_name.lower().strip()]


def parse_ptbr_number(string):
    """
    Input: a string representing a float number in Brazilian currency format, e.g.: 1.573.345,98
    
    Returns the corresponding float number.
    """
    number = string
    number = number.replace('.', '').replace(',', '.')
    return float(number)


def parse_ptbr_series(string_series):
    """
    Input: a Series of strings representing a float number in Brazilian currency format, e.g.: 1.573.345,98
    
    Returns a Series with the corresponding float number.
    """
    
    number_series = string_series.str.split().str.join('').str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float)
    return number_series


class translate_dict(dict):
    """
    A dict that returns the key used if no translation was provided for it.
    """
    def __missing__(self,key):
        return key


def interleave(l1, l2):
    """
    Return a list containing the elements in 
    lists `l1` and `l2` interleaved, that is,
    shuffled in an ordered manner, one from 
    each list.
    """
    
    return [val for pair in zip(l1, l2) for val in pair]
