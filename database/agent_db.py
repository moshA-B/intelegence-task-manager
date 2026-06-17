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
            last_id = cursor.lastrowid
        last_created = self.get_agent_by_id(last_id)
        return last_created
    
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
            return None

    def update_agent(self, id, data):
        columns = [f"{key} = %s" for key in data]
        columns_str = ",".join(columns)
        query = f"UPDATE agents SET {columns_str} WHERE id = %s"
        vals = list(data.values()) + [id]
        with self.conn.cursor() as cursor:
            cursor.execute(query, vals)
            self.conn.commit()
            changed = cursor.rowcount > 0
        return changed
    
    def deactivate_agent(self, id):
        with self.conn.cursor() as cursor:
            cursor.execute("UPDATE agents SET is_active = FALSE WHERE id = %s",(id,))
            self.conn.commit()
            changed = cursor.rowcount > 0
        return changed
    
    def increment_completed(self, id):
        with self.conn.cursor() as cursor:
            cursor.execute("UPDATE agents SET completed_missions = completed_missions + 1 WHERE id = %s", (id,))
            self.conn.commit()
            changed = cursor.rowcount > 0 
        return changed
    
    def increment_failed(self, id):
        with self.conn.cursor() as cursor:
            cursor.execute("UPDATE agents SET failed_missions = failed_missions + 1 WHERE id = %s", (id,))
            self.conn.commit()
            changed = cursor.rowcount > 0 
        return changed
    
    def get_agent_performance(self, id):
        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute("""SELECT completed_missions + failed_missions AS total,
                            completed_missions AS completed,
                            failed_missions AS failed,
                            ((completed_missions + failed_missions)/100 )* completed_missions AS success_rate
                           WHERE id = %s """, (id,))
            performance = cursor.fetchall()
        return performance
        

    def count_active_agents(self):
        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT COUNT(*) AS active FROM agents WHERE is_active = TRUE")
            num = cursor.fetchone()
        return num["active"]

