from database import db_connection


class MissionDB:
    def __init__(self):
        db_connection.DB_connection.create_database()
        self.conn = db_connection.DB_connection().get_connection()

    def create_mission(self, data):
        mission_calculation = data["difficulty"] * 2 + data["importance"]
        if 0 <= mission_calculation < 10:
            tag = "LOW"
        elif 10 <= mission_calculation <= 17:
            tag = "MEDIUM"
        elif 18 <= mission_calculation <= 24:
            tag = "HIGH"
        else:
            tag = "CRITICAL"
        columns = list(data.keys()) + ["risk_level"]
        vals = list(data.values()) + [tag]
        columns_str = ",".join(columns)
        placeholders = ",".join(["%s"] * len(columns))
        query = f"INSERT INTO missions({columns_str}) VALUES({placeholders})"

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, vals)
                self.conn.commit()
                last_id = cursor.lastrowid
            last_created = self.get_mission_by_id(last_id)
            return last_created

        except Exception as e:
            print(e)
            return None

    def get_all_missions(self):
        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM missions")
            rows = cursor.fetchall()

        if rows:
            return rows
        else:
            return []

    def get_mission_by_id(self, id):
        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM missions WHERE id = %s", (id,))
            row = cursor.fetchone()
        return row

    def assign_missions(self, m_id, a_id):
        assigned_missions = self.get_open_missions_by_agent(a_id)
        if assigned_missions >= 3:
            return None
        with self.conn.cursor() as cursor:
            cursor.execute(
                "UPDATE missions SET assigned_agent_id = %s, status = 'ASSIGNED' WHERE id = %s AND status= 'NEW'",
                (a_id, m_id),
            )
            self.conn.commit()
            changed = cursor.rowcount > 0
        return changed

    def update_mission_status(self, id, status):
        with self.conn.cursor() as cursor:
            cursor.execute(
                "UPDATE missions SET status = %s WHERE id = %s", (status, id)
            )
            self.conn.commit()
            changed = cursor.rowcount > 0
        return changed

    def get_open_missions_by_agent(self, id):
        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute(
                """SELECT COUNT(*) AS open FROM missions 
                           WHERE assigned_agent_id = %s 
                           AND (status = 'ASSIGNED' OR status = 'IN_PROGRESS')""",
                (id,),
            )
            num = cursor.fetchone()
        return num["open"]

    def count_all_missions(self):
        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT COUNT(*) AS total FROM missions")
            num = cursor.fetchone()

        return num["total"]

    def count_by_stats(self, status):
        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute(
                "SELECT COUNT(*) AS total FROM missions WHERE status = %s", (status,)
            )
            num = cursor.fetchone()

        return num["total"]

    def count_open_missions(self):
        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute(
                "SELECT COUNT(*) AS open FROM missions WHERE status = 'NEW' or status = 'ASSIGNED' OR status = 'IN_PROGRESS'"
            )
            num = cursor.fetchone()

        return num["open"]

    def count_critical_missions(self):
        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute(
                "SELECT COUNT(*) AS critical FROM missions WHERE risk_level = 'CRITICAL' "
            )
            num = cursor.fetchone()

        return num["critical"]
    
    def get_top_agent(self):
        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute("""SELECT * FROM agents WHERE completed_missions =
                            (SELECT MAX(completed_missions) FROM agents) 
                            """)
            top = cursor.fetchall()
        return top

    # SELECT assigned_agent_id, COUNT(*) AS total
    #                         FROM missions
    #                         GROUP BY assigned_agent_id
    #                         WHERE assigned_agent_id IS NOT NULL
    #                         ORDER BY total DESC
    #                         LIMIT 1""")
