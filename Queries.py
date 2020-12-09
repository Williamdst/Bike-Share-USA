def countTrips(conn):
    cursor = conn.cursor()
    
    countTrips_query = """
            SELECT EXTRACT(YEAR FROM starttime) as Year, Count(*) as Trips
              FROM trip
             GROUP BY Year
             ORDER BY Year;
            """
    cursor.execute("rollback")
    cursor.execute(countTrips_query)
    
    colnames = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
 
    return (colnames, data)

"============================================================================="

def countNJTrips(conn):
    cursor = conn.cursor()
    
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
    cursor.execute("rollback")
    cursor.execute(countNJTrips_query)
    
    colnames = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    
    return (colnames, data)

"============================================================================="
