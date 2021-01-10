def countYearlyTrips(conn):   # Query-0001 (Analyze)
    cursor = conn.cursor()
    cursor.execute("rollback")
  
    countTrips_query = """
            SELECT EXTRACT(YEAR FROM starttime) as Year, Count(*) as Trips
              FROM trip
             GROUP BY Year
             ORDER BY Year;
            """
    cursor.execute(countTrips_query)
    
    colnames = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
 
    return (colnames, data)

"============================================================================="

def countYearlyNJTrips(conn): # Query-0002 (Analyze)
    cursor = conn.cursor()
    cursor.execute("rollback")
   
    countNJTrips_query = """
            WITH nj_trips AS (
                 SELECT *
                 FROM trip as t
                 WHERE startid NOT IN (
                       SELECT stationid
                         FROM station
                        WHERE t.startid = stationid
                        )
                    OR endid NOT IN (
                        SELECT stationid 
                          FROM station
                         WHERE t.endid = stationid
                        )
                )
            
            SELECT EXTRACT(YEAR FROM starttime) as Year, count(*) as Trips
              FROM nj_trips
             GROUP BY Year
             ORDER BY Year;
            """
    cursor.execute(countNJTrips_query)
    
    colnames = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    
    return (colnames, data)

"============================================================================="

def deleteNJTrips(conn) -> None: #(Tables)
    cursor = conn.cursor()
    cursor.execute("rollback")

    deleteNJTrips_query = """
                DELETE FROM trip
                WHERE startid NOT IN (
                       SELECT stationid
                         FROM station
                        WHERE trip.startid = stationid
                        )
                    OR endid NOT IN (
                        SELECT stationid 
                          FROM station
                         WHERE trip.endid = stationid
                        )
                """
    
    cursor.execute(deleteNJTrips_query)
    
    return None

"============================================================================="

def create_foreign_key(conn, fk_table, fk_col, ref_table, ref_col, fk_name=''): #(Tables)
    cursor = conn.cursor()
    cursor.execute('rollback;')

    fk_create_query = f"""
            ALTER TABLE {fk_table}
            ADD CONSTRAINT fk_{fk_col}_{ref_col}
            FOREIGN KEY ({fk_col})
            REFERENCES {ref_table}({ref_col});
            """
    
    if fk_name:
        fk_create_query = f"""
                ALTER TABLE {fk_table}
                ADD CONSTRAINT {fk_name}
                FOREIGN KEY ({fk_col})
                REFERENCES {ref_table}({ref_col});
                """
    
    cursor.execute(fk_create_query)
    conn.commit()    
    return None

"============================================================================="

def get_random_rows(conn, n_100K_rows: int=1) -> pd.DataFrame():
    """
    Randomly Samples 1% of data (1M rows) shuffles it and then takes the first n 100K rows
    """
    # 10s * n_100k_rows = time to execute
    
    cursor = conn.cursor()
    cursor.execute('rollback;')
    
    row_data = pd.DataFrame()
    get_row_query = """SELECT * FROM trip TABLESAMPLE system(1) order by random() limit 100000"""
    
    for i in range(n_100K_rows):
        cursor.execute(get_row_query)
        colnames = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()
        row_data = pd.concat([row_data, pd.DataFrame(data, columns=colnames)], ignore_index=True)
    
    return row_data

"============================================================================="

def VACUUM(conn):
    cursor = conn.cursor()
    cursor.execute('rollback;')
    cursor.execute('VACUUM;')
    conn.commit()
    return None