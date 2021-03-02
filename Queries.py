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
        return (data, colnames)
    else:
        conn.commit()
        return None

"============================================================================="

def get_random_100k_rows(conn, shuffles: int=1, speed: bool=False, distance: bool=False) -> pd.DataFrame(): #Analyze
    """
    Randomly Samples 1% of data (1M rows) shuffles it and then takes the first n 100K rows
    """
    # 10s * shuffles = time to execute
    
    cursor = conn.cursor()
    cursor.execute('rollback;')
    
    get_row_query = ""
    row_data = pd.DataFrame()
    
    if distance:
        get_row_query = """
                SELECT tp.*, round(CAST(ST_Distance(s1.geometry, s2.geometry)*0.000621371 AS numeric),2) AS distance
                  FROM trip AS tp TABLESAMPLE SYSTEM(1) 
                       LEFT JOIN station AS s1 
                            ON tp.startid = s1.stationid
                       LEFT JOIN station AS s2
                            ON tp.endid = s2.stationid
                 ORDER BY RANDOM()
                 LIMIT 100000;
                """
    else:
        get_row_query = """
                SELECT * 
                  FROM trip TABLESAMPLE SYSTEM(1) 
                 ORDER BY RANDOM() LIMIT 100000;
                """
    
    for i in range(shuffles):
        cursor.execute(get_row_query)
        colnames = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()
        row_data = pd.concat([row_data, pd.DataFrame(data, columns=colnames)], ignore_index=True)
    
    row_data = row_data.astype({'startid':'int', 'endid':'int','usertype':'category','gender':'category'})
    
    if distance and speed:
        row_data['distance'] = pd.to_numeric(row_data.distance)
        row_data['MPH'] = row_data.distance / (row_data.tripduration / 60)
    if distance:
        row_data['distance'] = pd.to_numeric(row_data.distance)
    
    return row_data

"============================================================================="

def VACUUM(conn): # (TAbles) GENERIC QUERY
    cursor = conn.cursor()
    cursor.execute('rollback;')
    cursor.execute('VACUUM;')
    conn.commit()
    return None

"============================================================================="

def delete_duration_outliers(conn) -> None: #(Tables) GENERIC QUERY
    cursor = conn.cursor()
    cursor.execute("rollback")

    delete_duration_query = """
             DELETE FROM trip
             WHERE tripduration > 96
                """
    
    cursor.execute(delete_duration_query)
    conn.commit()    
    return None

"============================================================================="


def find_time_swaps(conn) -> pd.DataFrame(): # (Analyze) GENERIC QUERY
    cursor = conn.cursor()
    cursor.execute('rollback;')
    
    find_swaps_query = """
                SELECT * 
                  FROM trip 
                 WHERE starttime >= endtime;
                """
    cursor.execute(find_swaps_query)
    colnames = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    
    df = pd.DataFrame(data, columns=colnames)
    return(df)

"============================================================================="


def delete_time_swaps(conn) -> None: #(Tables) GENERIC QUERY
    cursor = conn.cursor()
    cursor.execute("rollback;")

    delete_swap_query = """
             DELETE FROM trip
             WHERE starttime > endtime
                """
    
    cursor.execute(delete_swap_query)
    conn.commit()    
    return None

"============================================================================="

def birth_certificate(conn) -> None: #(Tables)
    cursor = conn.cursor()
    cursor.execute("rollback;")
    
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
    
    cursor.execute(birth_certificate_query)
    conn.commmit()
    return None

"============================================================================="

def voronoi_data(conn) -> None: #(Tables)
    cursor = conn.cursor()
    cursor.execute("rollback;")
    
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
    
    cursor.execute(voronoi_data_query)
    conn.commit()
    return None

"============================================================================="
