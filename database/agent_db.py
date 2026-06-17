import db_connection

class AgentDB:
    def __init__(self):
        self.conn = db_connection.DB_connection().get_connection()

    def create_agent(self, data):
        columns = list(data.keys())
        vals = list(data.values())
        columns_str = ",".join(columns)
        placeholders = ",".join(["%s"] * len(columns))
        
        query = f"INSERT INTO agents({columns_str} VALUES({placeholders}))"
        with self.conn.cursor() as cursor:
            cursor.execute(query, vals)
            self.conn.commit()
            changed = cursor.rowcount > 0
        return changed
    
    def get_all_agents(self):
        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM agents")
            rows = cursor.fetchall()
        if rows:
            return rows
        else:
            return []
        
    def get_agent_by_id(self, id):
        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM agents WHERE id = %s",(id,))
            row = cursor.fetchall()
        if row:
            return row
        else:
            return []

    def update_agent(self, id, data):
        columns = [f"{key} = %s" for key in data]
        columns_str = ",".join(columns)
        query = "UPDATE agents SET "
        vals = list(data.values())
