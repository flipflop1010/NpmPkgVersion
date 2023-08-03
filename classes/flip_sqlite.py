import sqlite3
import re
from .npm_pkg import *


class FlipSqlite:
    obj = None

    def __init__(self):
        self.conn = sqlite3.connect("db/main.db")
        # print ("Opened database successfully")
        self.table_define()

    def table_define(self):
        q = """create table if not exists npm_packages(
            id INTEGER primary key AUTOINCREMENT,
            title text,
            version text,
            npm_latest_ver text null,
            dependency_type text
        )
        """
        self.conn.execute(q)

    @staticmethod
    def get_instance():
        if not FlipSqlite.obj:
            FlipSqlite.obj = FlipSqlite()
        return FlipSqlite.obj

    def exec_raw_query(self, query: str):
        cur = self.conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        return rows

    def update_npm_package(self, pkg_title: str, version: str, pkg_type: str):
        pkg_latest_version = NpmPkg.getPkgVersion(pkg_title)
        print(pkg_latest_version)

        res = self.exec_raw_query(
            f"select * from npm_packages where title='{pkg_title}' and dependency_type='{pkg_type}'"
        )
        row = None
        cur = self.conn.cursor()

        if len(res) == 0:
            q = f"insert into npm_packages(title,version,npm_latest_ver,dependency_type) values('{pkg_title}','{version}','{pkg_latest_version}','{pkg_type}')"
            # print(q)
            res = cur.execute(q)
            self.conn.commit()
            return {"success": True, "message": "pkg inserted"}

        row = res[0]
        ret_res = None
        if not re.match("[a-zA-z]+", version) and version > row[2]:
            q = f"update npm_packages set version='{version}' where id={row[0]}"
            res = cur.execute(q)
            self.conn.commit()
            ret_res = {"success": True, "message": "pkg updated"}

        if (
            pkg_latest_version != None
            and not re.match("[a-zA-Z]+", pkg_latest_version)
            and pkg_latest_version > row[3]
        ):
            q = f"update npm_packages set npm_latest_ver='{pkg_latest_version}' where id={row[0]}"
            res = cur.execute(q)
            self.conn.commit()

        if ret_res:
            return ret_res
        return {"success": False, "message": "nothing happend"}


a = FlipSqlite.get_instance()

# res=a.update_npm_package('@types/aws-lambda','8.10.65','devDependencies')
# print(res)
