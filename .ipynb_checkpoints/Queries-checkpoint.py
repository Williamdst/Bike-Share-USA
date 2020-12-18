def countYearlyTrips(conn):   # Query-0001
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

def countYearlyNJTrips(conn): # Query-0002
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

def deleteNJTrips(conn) -> None:
    cursor = conn.cursor()

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
    
    cursor.execute("rollback")
    cursor.execute(deleteNJTrips_query)
    
    return None