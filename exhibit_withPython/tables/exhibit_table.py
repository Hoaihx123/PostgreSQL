# Таблица Телефоны и особые действия с ней.
import dbtable
from dbtable import *

class ExhibitsTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "Exhibits"

    def columns(self):
        return {"id": ["serial"],
                "name": ["varchar(64)", "NOT NULL"],
                "short_describe": ["varchar(128)"],
                "insurance_value": ["integer", "NOT NULL"],
                "century": ["integer", "NOT NULL"],
                "collection_id": ["integer", "NOT NULL", "REFERENCES Collections(id) ON DELETE CASCADE"],
                "height": ["integer"],
                "weight": ["integer"],
                "length": ["integer"],
                "tempe_max": ["integer"],
                "tempe_min": ["integer"],
                "humidity_max": ["integer"],
                "humidity_min": ["integer"],
                "protec_people": ["boolean", "NOT NULL"]}
    
    def primary_key(self):
        return ['id']

    def table_constraints(self):
        return ["PRIMARY KEY(id)"]

    def all_by_collection_id(self, cid):
        try:
            sql = "SELECT * FROM " + self.table_name()
            sql += " WHERE collection_id = %s"
            sql += " ORDER BY "
            sql += ", ".join(self.primary_key())
            cur = self.dbconn.conn.cursor()
            cur.execute(sql, str(cid))
            return cur.fetchall()
        except Exception as err:
            dbtable.print_error(err)
            self.dbconn.conn.rollback()

    def find_by_position(self, num, collection_id):
        try:
            sql = "SELECT * FROM " + self.table_name()
            sql += " WHERE collection_id=%(collection_id)s ORDER BY "
            sql += ", ".join(self.primary_key())
            sql += " LIMIT 1 OFFSET %(offset)s"
            cur = self.dbconn.conn.cursor()
            cur.execute(sql, {"collection_id": collection_id, "offset": num - 1})
            return cur.fetchone()
        except Exception as err:
            dbtable.print_error(err)
            self.dbconn.conn.rollback()

    def del_exhibit(self, id):
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

    def change_exhibit(self, vals):
        try:
            sql = "UPDATE "+self.table_name()
            sql += " SET name=%(name)s, short_describe=%(short_describe)s, protec_people=%(protec_people)s WHERE id=%(id)s"
            cur = self.dbconn.conn.cursor()
            cur.execute(sql, {"name": vals[1], "short_describe": vals[2], "protec_people": vals[13], "id": vals[0]})
            self.dbconn.conn.commit()
            return
        except Exception as err:
            dbtable.print_error(err)
            self.dbconn.conn.rollback()