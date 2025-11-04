import mysql.connector

class MySqlHelper:

    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None


    def connect(self):
        self.conn = mysql.connector.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database = self.database
        )
        self.cursor = self.conn.cursor(dictionary = True)

    def execute(self, sql, values=None):
        self.cursor.execute(sql, values)
        self.conn.commit()

    def add(self, table, columns, values):
        holder1 = ", ".join(columns)
        holder2 = ", ".join(["%s"] * len(values))
        sql = f"INSERT INTO {table}({holder1}) VALUES ({holder2})"
        self.execute(sql,values)

    def query(self, sql, values=None):
        self.cursor.execute(sql, values)
        return self.cursor.fetchall()

    def update(self, table, set_clause, holder=None, values=None):
        sql = f"update {table} set {set_clause}"
        if holder:
            sql += f"Where {holder}"
        self.execute(sql, values)

    def delete(self, table, holder, values):
        sql = f"delete from {table} where {holder}"
        self.execute(sql, values)

    def close(self):
        self.cursor.close()
        self.conn.close()