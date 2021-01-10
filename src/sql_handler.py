import os
import sqlite3

from scanner import BaseFileScanHandler

# TODO add source
class SqlWrapper(BaseFileScanHandler):
    def __init__(self, connection: sqlite3.Connection, override_or_create=False, source='laptop'):
        self.db_connection = connection
        self.source = source

        # TODO make this better
        if override_or_create:
            try:
                self.db_connection.execute("drop table files;")
            except Exception as e:
                print(e)
                raise e
            self.db_connection.execute(
                "create table files ("
                "filename varchar(255), "
                "extension varchar(10), "
                "path varchar(1024), "
                "create_time int, "
                "mod_time int, "
                "size int, "
                "source varchar(20)"
                ");")

    def handle_file(self, filename: str, path: str, stats: os.stat_result):
        extension = filename.split(".")[-1]
        self.db_connection.execute(f"insert into files values (?,?,?,?,?,?,?);",
                                   (filename, extension, path, stats.st_ctime, stats.st_ctime, stats.st_size, self.source))
        self.db_connection.commit()
