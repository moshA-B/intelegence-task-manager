import mysql.connector

class DB_connection:
    @staticmethod
    def get_connection():
        return mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="1234",
            database="intelligence_db"
        )
    
    @staticmethod
    def create_database():
        cnx = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="1234",
        )
        cursor = cnx.cursor()
        try:
            cursor.execute("CREATE DATABASE intelligence_db")
        except Exception as e:
            print(e)
            return True
        
    @staticmethod
    def create_tables():
        conn = DB_connection.get_connection()
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS agents(
                       id INT AUTO_INCREMENT PRIMARY KEY,
                       name VARCHAR(50) NOT NULL,
                       specialty VARCHAR(50),
                       is_active BOOLEAN DEFAULT TRUE,
                       completed_missions INT DEFAULT 0,
                       failed_missions INT DEFAULT 0,
                       agent_rank ENUM('Junior','Senior','Commander') NOT NULL);""")
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS missions(
                       id INT AUTO_INCREMENT PRIMARY KEY,
                       title VARCHAR(50) NOT NULL,
                       description TEXT NOT NULL,
                       location VARCHAR(50) NOT NULL,
                       difficulty INT CHECK (difficulty >= 1 AND difficulty <= 10),
                       importance INT CHECK(importance >=1 AND importance <= 10),
                       status VARCHAR(50) DEFAULT 'NEW',
                       risk_level VARCHAR(50),
                       assigned_agent_id INT);""")
        conn.commit()
        cursor.close()
        conn.close()