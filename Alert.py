import pyodbc
from datetime import datetime

def connect_to_db():
    """Establish connection to Azure SQL Database"""
    print("Connecting to Azure SQL Database...")
    server = 'sqldatabasedd.database.windows.net'
    database = '3DSP'
    username = 'roottest'
    password = 'U2qkyMtVpsWrCH@'
    driver = '{ODBC Driver 18 for SQL Server}'
    
    cnxn_str = f"DRIVER={driver};SERVER=tcp:{server},1433;DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
    
    try:
        conn = pyodbc.connect(cnxn_str)
        print("Database connection established successfully.")
        return conn
    except pyodbc.Error as e:
        print(f"Database connection error: {e}")
        return None
    

def get_or_create_driver(conn, driver_name):
    """Get driver_id if exists, or create new driver and return id"""
    try:
        cursor = conn.cursor()
        
        # Check if driver exists
        cursor.execute("SELECT driver_id FROM drivers WHERE name = ?", (driver_name,))
        row = cursor.fetchone()

        
        if row:
            # Driver exists, return id
            driver_id = row[0]
            print(f"Driver '{driver_name}' found with ID: {driver_id}")
        else:
            # Driver doesn't exist, create new driver
            cursor.execute("INSERT INTO drivers (name) VALUES (?)", (driver_name,))
            conn.commit()
            
            # Get the newly created driver_id
            cursor.execute("SELECT @@IDENTITY")  # Get the last inserted ID
            driver_id = cursor.fetchone()[0]
            print(f"New driver '{driver_name}' created with ID: {driver_id}")
        
        cursor.close()
        return driver_id
    
    except pyodbc.Error as e:
        print(f"Error in get_or_create_driver: {e}")
        conn.rollback()
        raise

def alert_notification(name):
    """
    Create alert notification for a driver.
    
    Args:
        name (str): The name of the driver
        
    Returns:
        bool: True if alert was created successfully, False otherwise
    """
    if not name or name.strip() == "":
        print("Error: Driver name cannot be empty")
        return False
    
    conn = connect_to_db()
    if not conn:
        return False
    
    try:
        # Get current date and time
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        current_time = now.strftime("%H:%M:%S")
        
        # Get or create driver
        driver_id = get_or_create_driver(conn, name)
        
        # Insert alert with "drowsy" label
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO alerts (driver_id, date, time) 
            VALUES (?, ?, ?)
        """, (driver_id, current_date, current_time))
        
        conn.commit()
        print(f"Alert created successfully for driver: {name}")
        
        cursor.close()
        return True
    
    except Exception as e:
        print(f"Error creating alert: {e}")
        if conn:
            conn.rollback()
        return False
    
    finally:
        if conn:
            conn.close()
            print("Database connection closed")



if __name__ == "__main__":
    driver_name = input("Enter driver name: ")
    alert_notification(driver_name)