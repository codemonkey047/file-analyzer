import sqlite3

from scanner import FileScanner, BaseFileScanHandler
from sql_handler import SqlWrapper

conn = sqlite3.connect('file.db')

file_handler = SqlWrapper(conn, override_or_create=True, source='laptop')
# file_handler = BaseFileScanHandler()

scanner = FileScanner(file_handler, 15)

scanner.process_dir("C:/Users/swill", 0)
