from io import StringIO
from math import ceil
import pandas as pd
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

def upload_data(conn, data, table: str, sep = ','):
    """Uploads dataframe to the table in the database
    
    Parameters
    ----------
    conn: psycopg2.extensions.connection
        The connection to the database
    data: pandas.DataFrame
        The dataframe to be uploaded
    table: str
        The name of the table where the data will be stored
    sep: str
        The seperator to use when saving the dataframe to a csv
    
    Returns
    -------
    None:
        If executed properly the data should be in specified table of the database
    """
    
    cursor = conn.cursor()
    datastream = StringIO()
    
    data.to_csv(datastream, sep=sep, index=False, header=False)
    datastream.seek(0)
    
    cursor.execute('rollback;')
    cursor.copy_from(datastream, table, sep=sep)
    conn.commit()
    
    return None  

"============================================================================="

def get_random_rows(conn, service: str, samples) -> pd.DataFrame(): #Analyze
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

def delete_duration_outliers(conn, service: str, outliers: tuple) -> None: #(Tables) GENERIC QUERY
    """Deletes outliers from trip tables
    
    Parameters
    ----------
    conn: psycopg2.extensions.connection
        The connection to the database
    service: str
        The bike station service whose outlier trips are going to be deleted
    outlier: tuple(2)
        lower_outlier - The value of the 2.5th quantile of the distribution
        upper_outlier - The value of the 97.5th quantile of the distrubtion
    
    
    Returns
    -------
    None:
        Executes the query   
    """
    
    
    delete_duration_query = f"""
            DELETE FROM trips.{service}_trip
            WHERE duration < {outliers[0]}
              OR duration > {outliers[1]}
            """
    
    execute_query(conn, delete_duration_query)
    return None

"============================================================================="

def birth_certificate(conn, service, id_type = 'NUMERIC') -> None: #(Tables)
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
                    SELECT DISTINCT 
                      startid, 
                      MIN(DATE_TRUNC('day',starttime)::date) over w AS birth, 
                      MAX(DATE_TRUNC('day',starttime)::date) over w AS death
                    FROM trips.{service}_trip
                    WINDOW w as (PARTITION BY startid)
                )
            
                UPDATE stations.{service}_station AS s
                SET 
                  birth = ts.birth,
                  death = ts.death
                FROM timestamps AS ts
                WHERE 
                  s.stationid::numeric = ts.startid;
                """  
    
    if id_type == 'VARCHAR':
        birth_certificate_query = f"""
                WITH timestamps AS (
                    SELECT DISTINCT 
                      startid, 
                      MIN(DATE_TRUNC('day',starttime)::date) over w AS birth, 
                      MAX(DATE_TRUNC('day',starttime)::date) over w AS death
                    FROM trips.{service}_trip
                    WINDOW w as (PARTITION BY REPLACE(startid, '.0', ''))
                )
            
                UPDATE stations.{service}_station AS s
                SET 
                  birth = ts.birth,
                  death = ts.death
                FROM timestamps AS ts
                WHERE 
                   s.stationid = ts.startid;
                """
        
    execute_query(conn, birth_certificate_query)
    return None

"============================================================================="

def station_growth(conn, service: str):  #Analysis
    
    station_growth_query = f"""
            SELECT
              year,
              ({service}_births - (CASE WHEN {service}_deaths IS NULL 
                                        THEN 0 
                                        ELSE {service}_deaths 
                                   END)) AS {service}_added,
              SUM(({service}_births - (CASE WHEN {service}_deaths IS NULL 
                                            THEN 0 
                                            ELSE {service}_deaths 
                                       END))) OVER(ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS {service}_total
            FROM 
                (SELECT 
                   DATE_TRUNC('year', birth) AS year,
                   count(birth) AS {service}_births
                 FROM stations.{service}_station
                 GROUP BY year
                 ORDER BY year) AS births
            FULL JOIN
                (SELECT 
                  DATE_TRUNC('year', death) AS year,
                  count(death) AS {service}_deaths
                 FROM stations.{service}_station
                 GROUP BY year
                 ORDER BY year) AS deaths
              USING (year)
            WHERE year IS NOT NULL;
            """
    
    df = execute_query(conn, station_growth_query, to_frame=True)
    return df
"============================================================================="

def voronoi_data(conn) -> None: #(Tables)

    voronoi_data_query_citi = f"""
         WITH voronoi AS(
              SELECT 
                (g.gdump).path, 
                (g.gdump).geom
              FROM (
                    SELECT 
                      ST_DUMP(ST_VoronoiPolygons(ST_Collect(geometry::geometry))) AS gdump
                    FROM stations.citi_station
                    WHERE death IS NULL
                   ) AS g
        )
        UPDATE stations.citi_station AS s
        SET 
          voronoi = v.geom
        FROM voronoi AS v
        WHERE ST_Contains(v.geom, s.geometry::geometry)
          AND s.death IS NULL;
        """
    
    voronoi_data_query_bay = f"""
         WITH voronoi AS(
              SELECT (g.gdump).path, (g.gdump).geom
                FROM (SELECT ST_DUMP(ST_VoronoiPolygons(ST_Collect(geometry::geometry))) AS gdump
                        FROM stations.bay_station
                       WHERE death IS NULL
                         AND stationid like 'SF%'
                      ) AS g
        )
        UPDATE stations.bay_station AS s
           SET voronoi = v.geom
          FROM voronoi AS v
         WHERE ST_Contains(v.geom, s.geometry::geometry)
               AND s.death IS NULL
               AND s.stationid like 'SF%';
        """
    
    execute_query(conn, voronoi_data_query_citi)
    execute_query(conn, voronoi_data_query_bay)
    return None

"============================================================================="

def trip_from_staging(conn, service, id_type = 'NUMERIC'):
    
    trip_from_staging_query = f"""
            CREATE TABLE trips.{service}_trip as (
                SELECT 
                  *, 
                  CASE WHEN 
                         duration > 0 
                       THEN ROUND(distance/(duration / 60), 2) 
                  END AS speed
                FROM (
                    SELECT 
                      starttime, 
                      endtime, 
                      ROUND((EXTRACT(epoch FROM (endtime - starttime))/60)::NUMERIC, 2) AS duration, 
                      startid, 
                      startname, 
                      endid, 
                      endname,
                      CASE WHEN 
                             s1.latitude > 0 AND s2.latitude > 0 
                           THEN ROUND(CAST(ST_Distance(s1.geometry, s2.geometry)*0.000621371 AS NUMERIC),2)
                      END AS distance
                    FROM staging.{service}_trip AS {service}
                    LEFT JOIN stations.{service}_station AS s1
                      ON {service}.startid = s1.stationid::NUMERIC
                    LEFT JOIN stations.{service}_station AS s2
                      ON {service}.endid = s2.stationid::NUMERIC
                ) AS {service}_table
            );
            """
    
    if id_type == 'VARCHAR':
        trip_from_staging_query = f"""
                CREATE TABLE trips.{service}_trip AS (
                    SELECT 
                      *, 
                      CASE WHEN 
                             duration > 0 
                           THEN ROUND(distance/(duration / 60), 2) 
                      END AS speed
                    FROM (
                        SELECT 
                          {service}.starttime, 
                          {service}.endtime, 
                          ROUND((EXTRACT(epoch FROM (endtime - starttime))/60)::NUMERIC, 2) AS duration, 
                          replace({service}.startid, '.0','') as startid,
                          startname, 
                          replace({service}.endid, '.0','') as endid, 
                          endname,
                          CASE WHEN 
                                s1.latitude > 0 AND s2.latitude > 0
                               THEN ROUND(CAST(ST_Distance(s1.geometry, s2.geometry)*0.000621371 AS NUMERIC),2)
                          END AS distance
                        FROM staging.{service}_trip AS {service}
                        LEFT JOIN stations.{service}_station AS s1
                          ON replace({service}.startid,'.0','') = s1.stationid
                        LEFT JOIN stations.{service}_station AS s2
                          ON replace({service}.endid, '.0','') = s2.stationid
                    ) AS {service}_table 
                );
                """

    execute_query(conn, trip_from_staging_query)
    return None

"============================================================================="

def n_popular_stations(conn, service, n=5, ranking = 'total'):
    
    if ranking == 'total':
        ranking = 'startpoints.startpoints + endpoints.endpoints'
    elif ranking == 'start':
        ranking = 'startpoints.startpoints'
    elif ranking == 'end':
        ranking = 'endpoints.endpoints'
    else:
        raise ValueError("Acceptable inputs for rankings are 'total', 'start', 'end'")
    
    ranking_query = f"""
            WITH yearly_rankings AS(
                        SELECT 
                          startpoints.year,
                          startid AS stationid,
                          startname AS station,
                          startpoints.startpoints,
                          endpoints.endpoints,
                          startpoints.startpoints + endpoints.endpoints as total_points,
                          RANK() OVER(PARTITION BY startpoints.year ORDER BY {ranking} DESC) AS ranking,
                          '{service}' AS service
                        FROM (
                            SELECT 
                               DATE_TRUNC('year', starttime) AS year,
                               startid,
                               startname,
                               COUNT(*) AS startpoints
                            FROM trips.{service}_trip
                            GROUP BY year, startid, startname) AS startpoints
                        FULL JOIN (
                            SELECT 
                               DATE_TRUNC('year', starttime) AS year,
                               endid,
                               endname,
                               COUNT(*) AS endpoints
                            FROM trips.{service}_trip
                            GROUP BY year, endid, endname) AS endpoints
                          ON startpoints.year = endpoints.year
                         AND startpoints.startid = endpoints.endid
                         AND startpoints.startname = endpoints.endname
                        WHERE {ranking} IS NOT NULL
                )
                SELECT * 
                FROM yearly_rankings
                WHERE ranking <= {n}
                  AND year IS NOT null
                """
    df = execute_query(conn, ranking_query, to_frame=True)
    return df

"============================================================================="

def inter_zipcode_travel(conn, service, id_type = 'NUMERIC'): #Analysis  
    
    if id_type.upper() not in ['NUMERIC','VARCHAR']:
        raise ValueError('Argument invalid, only NUMERIC and VARCHAR aceptable')
        
    inter_zipcode_query = f"""
            SELECT 
              DATE_TRUNC('year', starttime) AS year,
              SUM(CASE WHEN s1.zipcode != s2.zipcode THEN 1 ELSE 0 END) * 100 / COUNT(*) AS percent_inter_travel,
              '{service}' as service
            FROM trips.{service}_trip AS trips
            LEFT JOIN stations.{service}_station AS s1
              ON trips.startid = s1.stationid::{id_type}
            LEFT JOIN stations.{service}_station AS s2
              ON trips.endid = s2.stationid::{id_type}
            GROUP BY year;
            """
    
    df = execute_query(conn, inter_zipcode_query, to_frame=True)
    return df

"============================================================================="

def get_zipcode_stations(conn):
    
    # WHERE birth <= '2021-01-01'
    #   AND death IS NULL
    zipcode_stations_query = """
    
            SELECT zipcode, COUNT(*) as num_stations
            FROM stations.bay_station
            GROUP BY zipcode

            UNION

            SELECT zipcode, COUNT(*) as num_stations
            FROM stations.blue_station
            GROUP BY zipcode

            UNION

            SELECT zipcode, COUNT(*) as num_stations
            FROM stations.capital_station
            GROUP BY zipcode


            UNION

            SELECT zipcode, COUNT(*) as num_stations
            FROM stations.citi_station
            GROUP BY zipcode

            UNION

            SELECT zipcode, COUNT(*) as num_stations
            FROM stations.divvy_station
            GROUP BY zipcode  
            
            ORDER BY zipcode

            """
    df= execute_query(conn, zipcode_stations_query, to_frame = True)
    return df
    
"============================================================================="

def get_stations(conn, service: str, drop_indices: list=[]) -> pd.DataFrame():
    """Derives the unqiue stations from the trip data in the staging schema
    
    Parameters
    ----------
    conn: psycopg2.extensions.connection
        The connection to the database
    service : str
        One of the five bikeshare services of interest
    drop_indices: list
        A list of indices to drop before returning the stations. Used for stations that aren't actual stations
    
    Returns
    -------
    pd.DataFrame:
        Returns a dataframe containing the stations information
    """
    
    # We use startid because stations that have at least one trip as the start destination
    # always have at least one trip as an end destination. Whereas the reverse is not true. Additionally,
    # sations that only have trips where they're an end destination are in very few trips (under 10).
    
    # Some stations get coordinate data in later trips and some never do
    station_query = f"""
            SELECT DISTINCT ON(endid) endid, endname, end_lat, end_long 
              FROM staging.{service}_trip
             WHERE end_lat > 0
             UNION
            SELECT DISTINCT ON(endid) endid, endname, end_lat, end_long
              FROM staging.{service}_trip
            ORDER BY endid, end_lat
            """
    
    station = pd.read_sql(station_query, conn)
    station.dropna(inplace=True)
    station.drop_duplicates(subset=['endid'], keep='last', inplace=True)
    
    if len(drop_indices) > 0:
        station = station.set_index('endid').drop(drop_indices).reset_index()
    
    return station


"============================================================================="

def add_bike_service_name(conn, table: str, name: str, schema: str):
    """Adds a bikeshare column in the table where every value is the name passed
    
    Parameters
    ----------
    conn: psycopg2.extensions.connection
        The connection to the database
    table : str
        The name of the table to be altered
    name: str
        The value that will fill the new column
    
    Returns
    -------
    None:
        If executed properly the table will have a new column called bikeshare that is populated with the value of name
    """
   
    add_name_query = f"""
            ALTER TABLE {schema}.{table}
            ADD COLUMN bikeshare varchar(8);

            UPDATE {schema}.{table}
            SET bikeshare = '{name}';
            """
          
    execute_query(conn, add_name_query)    
    return None

"============================================================================="

def delete_non_trips(conn, service: str, drop_indices: list) -> None:
    """Deletes trips from the table that contain any of the drop_indices as
    
     Parameters
    ----------
    conn: psycopg2.extensions.connection
        The connection to the database
    service : str
        One of the five bikeshare services of interest
    drop_indices: list
        A list of stations to determine which trips get dropped. If a trip has a value in the list it gets dropped
    
    Returns
    -------
    None:
        If executed properly there won't be trips with any of the indices   
    """
    
    # Converting the list of indices into a format that PostgreSQL understands
    drop_indices = [str(element) for element in drop_indices]
    drop_indices = '(' + ",".join(drop_indices) + ')'
    return drop_indices
    
    delete_non_trips_query = f"""
            DELETE FROM trips.{service}_trip
            WHERE startid IN {drop_indices}
               OR endid IN {drop_indices}
            """
    
    execute_query(conn, delete_non_trips_query)
    return None