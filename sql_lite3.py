

import sqlite3

conn = sqlite3.connect('test.db')
conn.execute("create table t1(name text,age int)")
conn.close()