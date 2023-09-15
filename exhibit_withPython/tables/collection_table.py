# Таблица персоны и особые действия с ней
import dbtable
from dbtable import *

class CollectionTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "Collections"

    def columns(self):
        return {"id": ["serial", "PRIMARY KEY"],
                "name": ["varchar(64)", "NOT NULL"],
                "short_describe": ["varchar(128)"]}

    def find_by_position(self, num):
        try:
            sql = "SELECT * FROM " + self.table_name()
            sql += " ORDER BY "
            sql += ", ".join(self.primary_key())
            sql += " LIMIT 1 OFFSET %(offset)s"
            cur = self.dbconn.conn.cursor()
            cur.execute(sql, {"offset": num - 1})
            return cur.fetchone()
        except Exception as err:
            dbtable.print_error(err)
            self.dbconn.conn.rollback()
    def del_collection(self, id):
        try:
            sql = "DELETE FROM " + self.table_name()
            sql += " WHERE id = %(id)s"
            cur = self.dbconn.conn.cursor()
            cur.execute(sql, {"id": id})
            self.dbconn.conn.commit()
            return
        except Exception as err:
            dbtable.print_error(err)
            self.dbconn.conn.rollback()

    def change_collection(self, vals):
        try:
            sql = "UPDATE "+self.table_name()
            sql += " SET name=%(name)s, short_describe=%(short_describe)s WHERE id=%(id)s"
            cur = self.dbconn.conn.cursor()
            cur.execute(sql, {"name": vals[1], "short_describe": vals[2], "id": vals[0]})
            self.dbconn.conn.commit()
            return
        except Exception as err:
            dbtable.print_error(err)
            self.dbconn.conn.rollback()
    
