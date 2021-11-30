#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 12:13:26 2021

@author: skems
"""

import os
import pandas as pd
import csv


def bigquery_to_pandas(query, project='gabinete-compartilhado', credentials_file='/home/skems/gabinete/projetos/keys-configs/gabinete-compartilhado.json'):
    """
    Run a query in Google BigQuery and return its results as a Pandas DataFrame. 

    Input
    -----

    query : str
        The query to run in BigQuery, in standard SQL language.
    project : str
        
    
    Given a string 'query' with a query for Google BigQuery, returns a Pandas 
    dataframe with the results; The path to Google credentials and the name 
    of the Google project are hard-coded.
    """

    import google.auth
    import os

    # Set authorization to access GBQ and gDrive:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_file

    
    credentials, project = google.auth.default(scopes=[
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/bigquery',
    ])
    
    return pd.read_gbq(query, project_id=project, dialect='standard', credentials=credentials)


def load_data_from_local_or_bigquery(query, filename, force_bigquery=False, save_data=True, 
                                     project='gabinete-compartilhado', 
                                     credentials_file='/home/skems/gabinete/projetos/keys-configs/gabinete-compartilhado.json',
                                     low_memory=False):
    """
    Loads data from local file if available or download it from BigQuery otherwise.
    
    
    Input
    -----
    
    query : str
        The query to run in BigQuery.
    
    filename : str
        The path to the file where to save the downloaded data and from where to load it.
        
    force_bigquery : bool (default False)
        Whether to download data from BigQuery even if the local file exists.
        
    save_data : bool (default True)
        Wheter to save downloaded data to local file or not.
        
    project : str (default 'gabinete-compartilhado')
        The GCP project where to run BigQuery.
        
    credentials_file : str (default path to 'gabinete-compartilhado.json')
        The path to the JSON file containing the credentials used to access GCP.
        
    low_memory : bool (default False)
        Whether or not to avoid reading all the data to define the data types
        when loading data from a local file.

    Returns
    -------
    
    df : Pandas DataFrame
        The data either loaded from `filename` or retrieved through `query`.
    """
    
    # Download data from BigQuery and save it to local file:
    if os.path.isfile(filename) == False or force_bigquery == True:
        print('Loading data from BigQuery...')
        df = bigquery_to_pandas(query, project, credentials_file)
        if save_data:
            print('Saving data to local file...')
            df.to_csv(filename, quoting=csv.QUOTE_ALL, index=False)
    
    # Load data from local file:
    else:
        print('Loading data from local file...')
        df = pd.read_csv(filename, low_memory=low_memory)
        
    return df
