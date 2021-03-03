import pandas as pd

def execute_query(conn, query, cols_data=False, to_frame=False):
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

def get_random_50k_rows(conn, table: str, shuffles: int=1) -> pd.DataFrame(): #Analyze
    """
    Randomly Samples 1% of the data shuffles it and then takes the first 50K rows. Does this process
    for the number of shuffles passed. 
    """
    
    cursor = conn.cursor()
    cursor.execute('rollback;')
    
    get_row_query = ""
    row_data = pd.DataFrame()
    
    get_row_query = f"""
            SELECT * 
            FROM trips.{table}_trip TABLESAMPLE SYSTEM(1) 
            ORDER BY RANDOM() LIMIT 50000;
            """
    
    for i in range(shuffles):
        colnames, data = execute_query(conn, get_row_query, cols_data = True)
        row_data = pd.concat([row_data, pd.DataFrame(data, columns=colnames)], ignore_index=True)
        
    return row_data

"============================================================================="

def VACUUM(conn): # (TAbles) GENERIC QUERY
    execute_query(conn, 'VACUUM;')
    return None

"============================================================================="

def delete_duration_outliers(conn) -> None: #(Tables) GENERIC QUERY
    delete_duration_query = """
            DELETE FROM trip
            WHERE tripduration > 96
            """
    
    execute_query(conn, delete_duration_query)
    return None

"============================================================================="


def find_time_swaps(conn) -> pd.DataFrame(): # (Analyze) GENERIC QUERY  
    find_swaps_query = """
                SELECT * 
                  FROM trip 
                 WHERE starttime >= endtime;
                """    
    
    df = execute_query(conn, find_swaps_query, to_frame=True)
    return(df)

"============================================================================="


def delete_time_swaps(conn) -> None: #(Tables) GENERIC QUERY
    delete_swap_query = """
             DELETE FROM trip
             WHERE starttime > endtime
                """

    execute_query(conn, delete_swap_query)
    return None

"============================================================================="

def birth_certificate(conn) -> None: #(Tables)
    birth_certificate_query = """
                WITH timestamps AS (
                    SELECT DISTINCT startid, 
                                    MIN(DATE_TRUNC('day',starttime)::date) over w AS birth, 
                                    MAX(DATE_TRUNC('day',starttime)::date) over w AS death
                      FROM trip_ds
                    WINDOW w as (PARTITION BY startid)
                )
            
                UPDATE station AS s
                   SET birth = ts.birth,
                       death = ts.death
                  FROM timestamps AS ts
                 WHERE s.stationid = ts.startid;
                """  
    execute_query(conn, birth_certificate_query)
    return None

"============================================================================="

def voronoi_data(conn) -> None: #(Tables)
    voronoi_data_query = """
         WITH voronoi AS(
              SELECT (g.gdump).path, (g.gdump).geom
                FROM (SELECT ST_DUMP(ST_VoronoiPolygons(ST_Collect(geometry::geometry))) AS gdump
                        FROM station
                       WHERE death IS NULL
                      ) AS g
        )
        UPDATE station AS s
           SET voronoi = v.geom
          FROM voronoi AS v
         WHERE ST_Contains(v.geom, s.geometry::geometry)
               AND s.death IS NULL;
        """
    
    execute_query(conn, voronoi_data_query)
    return None

"============================================================================="
