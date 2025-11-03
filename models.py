from backend.database_connection import get_db_connection

def init_db():
    """Creates all database tables if they don't exist."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feeders (
                feeder_id INTEGER PRIMARY KEY AUTOINCREMENT,
                feeder_name TEXT NOT NULL,
                ip_address TEXT,
                location TEXT,
                max_capacity_g INTEGER DEFAULT 0,
                current_weight_g INTEGER DEFAULT 0,
                status TEXT DEFAULT 'offline',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS schedules (
                schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
                feeder_id INTEGER,
                schedule_time TEXT,
                amount_g INTEGER,
                day_of_week TEXT,
                FOREIGN KEY (feeder_id) REFERENCES feeders(feeder_id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                feeder_id INTEGER,
                event_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                action TEXT,
                weight_dispensed INTEGER,
                FOREIGN KEY (feeder_id) REFERENCES feeders(feeder_id)
            )
        """)
        
        print("✅ Database initialized successfully.")
