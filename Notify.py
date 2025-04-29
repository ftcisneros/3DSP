import time
import pyodbc

def connect_to_db():
    """Establish connection to Azure SQL Database"""
    server = 'sqldatabasedd.database.windows.net'
    database = '3DSP'
    username = 'roottest'
    password = 'U2qkyMtVpsWrCH@'
    driver = '{ODBC Driver 18 for SQL Server}'
    
    cnxn_str = f"DRIVER={driver};SERVER=tcp:{server},1433;DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
    
    try:
        conn = pyodbc.connect(cnxn_str)
        return conn
    except pyodbc.Error as e:
        print(f"Database connection error: {e}")
        return None

def monitor_table():
    conn = connect_to_db()
    cursor = conn.cursor()
    last_seen = set()

    while True:
        cursor.execute("SELECT driver_id, [date], [time] FROM alerts")
        rows = set(tuple(row) for row in cursor.fetchall())
        new_rows = rows - last_seen
        if new_rows:
            for row in new_rows:
                cursor.execute("SELECT name FROM drivers WHERE driver_id = ?", (row[0],))
                driver_name = cursor.fetchone()[0]
                print("DROWSINESS ALERT:", "Driver Name:", driver_name, "Driver ID:", row[0], "Time: ", row[2], "Date: ", row[1])
            last_seen = rows
        time.sleep(.1)  # Poll every second

if __name__ == "__main__":
    monitor_table()
