import pandas as pd
from math import ceil
from typing import Union

def execute_query(conn, query: str, cols_data=False, to_frame=False) -> Union[None, tuple, pd.DataFrame]:
    """Uploads dataframe to the table in the database
    
    Parameters
    ----------
    conn: psycopg2.extensions.connection
        The connection to the database
    query: str
        The query to send to the database
    cols_data: bool
        Determines if the results of the query will be returned as a tuple of (colnames, data)
    to_frame: bool
        Determines if the results of the query will be returned as a dataframe.
    
    Returns
    -------
    None:
        Only executes the query
    tuple(2):
        colnames - The column names that were returned from the query
        data - The data that was returned from the query
    pd.DataFrame:
        The results of the query stored as a dataframe
        
    """
    cursor = conn.cursor()
    cursor.execute("rollback;")
    cursor.execute(query)
    conn.commit()

    if to_frame:
        colnames = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()
        df = pd.DataFrame(data,columns=colnames)
        return df
    elif cols_data:
        colnames = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()
        return (colnames, data)
    else:
        return None

"============================================================================="

def get_random_100k_rows(conn, service: str, samples) -> pd.DataFrame(): #Analyze
    """ Randomly Samples 1% of the data shuffles it and then takes the first 100K rows. Does this process
    for the number of shuffles passed. 
    
  
    Parameters
    ----------
    conn: psycopg2.extensions.connection
        The connection to the database
    service: str
        The bike share service's table in the database trips schema to query from
    shuffles: int (default=1)
        The number of times to shuffle the data and select 20,000 rows (100K for citi)
    
    Returns
    -------
    pd.DataFrame:
        The results of all the shuffles appended to each other as a dataframe
        
    """
        
    cursor = conn.cursor()
    cursor.execute('rollback;')
    
    row_data = pd.DataFrame()  
    shuffles = ceil(samples/20000)
    
    get_row_query = f"""
            SELECT * 
            FROM trips.{service}_trip TABLESAMPLE SYSTEM(1) 
            ORDER BY RANDOM() 
            LIMIT 20000;
            """
    
    if service == 'citi':
        get_row_query = f"""
                SELECT * 
                FROM trips.{service}_trip TABLESAMPLE SYSTEM(1) 
                ORDER BY RANDOM() 
                LIMIT 100000;
                """ 
        shuffles = ceil(samples/100000)
  

    for i in range(shuffles):
        colnames, data = execute_query(conn, get_row_query, cols_data = True)
        row_data = pd.concat([row_data, pd.DataFrame(data, columns=colnames)], ignore_index=True)
    
    row_data[['duration', 'distance', 'speed']] = row_data[['duration','distance','speed']].astype('float32')
    return row_data

"============================================================================="

def VACUUM_FULL(conn) -> None: # (TAbles) GENERIC QUERY
    """Performs a full vacuum on the database
    
    Parameters
    ----------
    conn: psycopg2.extensions.connection
        The connection to the database
    
    Returns
    -------
    None:
        Executes the query        
    """
    
    
    execute_query(conn, 'VACUUM FULL;')
    return None

"============================================================================="

def delete_duration_outliers(conn, service: str, outlier: float) -> None: #(Tables) GENERIC QUERY
    """Deletes outliers from trip tables
    
    Parameters
    ----------
    conn: psycopg2.extensions.connection
        The connection to the database
    service: str
        The bike station service whose outlier trips are going to be deleted
    outlier: float
        The outlier/cut-off value for outliers
    
    
    Returns
    -------
    None:
        Executes the query   
    """
    
    
    delete_duration_query = f"""
            DELETE FROM trips.{service}_trip
            WHERE tripduration > {outlier}
            """
    
    execute_query(conn, delete_duration_query)
    return None

"============================================================================="


def find_time_swaps(conn, service: str) -> pd.DataFrame(): # (Analyze) GENERIC QUERY  
    """Finds the trips in the specificed service table that has time-swap errors
    
    Parameters
    ----------
    conn: psycopg2.extensions.connection
        The connection to the database
    service: str
        The bike station service whose trips will be checked for time swaps
    
    Returns
    -------
    pd.DataFrame:
        Returns, as a dataframe, the trips that have a time swap error     
    """
    
    find_swaps_query = f"""
                SELECT * 
                  FROM trips.{serive}_trip 
                 WHERE starttime >= endtime;
                """    
    
    df = execute_query(conn, find_swaps_query, to_frame=True)
    return(df)

"============================================================================="


def delete_time_swaps(conn, service: str) -> None: #(Tables) GENERIC QUERY
    """Delete the rows from the table that have time-swap errors
    
    Parameters
    ----------
    conn: psycopg2.extensions.connection
        The connection to the database
    service: str
        The bike station service whose time swap error trips will be removed
    
    Returns
    -------
    None:
        Executes the query   
    """
    
    delete_swap_query = f"""
             DELETE FROM trips.{service}_trip
             WHERE starttime > endtime
                """

    execute_query(conn, delete_swap_query)
    return None

"============================================================================="

def birth_certificate(conn, service) -> None: #(Tables)
    """Adds a birth and death column to the station table of the service indicating
    the first day that a station appeared in the system and the last day it appeared in the systme
    
    Parameters
    ----------
    conn: psycopg2.extensions.connection
        The connection to the database
    service: str
        The bike station service whose station table will be updated with birth and death columns
    
    Returns
    -------
    None:
        Executes the query that adds birth/death columns
    """   
    
    
    birth_certificate_query = f"""
                WITH timestamps AS (
                    SELECT DISTINCT startid, 
                                    MIN(DATE_TRUNC('day',starttime)::date) over w AS birth, 
                                    MAX(DATE_TRUNC('day',starttime)::date) over w AS death
                      FROM trips.{service}_trip
                    WINDOW w as (PARTITION BY startid)
                )
            
                UPDATE stations.{service}_station AS s
                   SET birth = ts.birth,
                       death = ts.death
                  FROM timestamps AS ts
                 WHERE s.stationid = ts.startid;
                """  
    execute_query(conn, birth_certificate_query)
    return None

"============================================================================="

def voronoi_data(conn, service) -> None: #(Tables)
    """Delete the rows from the table that have time-swap errors
    
    Parameters
    ----------
    conn: psycopg2.extensions.connection
        The connection to the database
    service: str
        The bike station service whose stations will be given a voronoi polygon
    
    Returns
    -------
    None:
        Executes the query to find the voronoi polygons for each station   
    """

    voronoi_data_query = f"""
         WITH voronoi AS(
              SELECT (g.gdump).path, (g.gdump).geom
                FROM (SELECT ST_DUMP(ST_VoronoiPolygons(ST_Collect(geometry::geometry))) AS gdump
                        FROM stations.{service}_station
                       WHERE death IS NULL
                      ) AS g
        )
        UPDATE stations.{service}_station AS s
           SET voronoi = v.geom
          FROM voronoi AS v
         WHERE ST_Contains(v.geom, s.geometry::geometry)
               AND s.death IS NULL;
        """
    
    execute_query(conn, voronoi_data_query)
    return None

"============================================================================="
