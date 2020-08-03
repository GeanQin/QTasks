#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sqlite3
import os

class DBManager:

    def __init__(self):
        self.env = os.environ
        self.conn = sqlite3.connect(self.env['HOME']+'/.qtasks.db')
        self.c = self.conn.cursor()
        self.qCreateTable()

    def __del__(self):
        self.conn.close()

    def qCreateTable(self):
        cursor = self.c.execute('SELECT count(*) FROM sqlite_master WHERE type="table" AND name = "QTASKS";')
        if cursor.fetchall()[0][0] == 0:
            self.c.execute("CREATE TABLE QTASKS \
                            (ISOK   CHAR(2)     NOT NULL,\
                            ID      INTEGER     PRIMARY KEY     AUTOINCREMENT, \
                            CONTENT TEXT        NOT NULL, \
                            DATE    TIMESTAMP   NOT NULL, \
                            ISABORT INT         NOT NULL);")

    def qDeleteTable(self):
        self.c.execute('DROP TABLE QTASKS;')

    def qAdd(self, isOK, content, date, isAbort):
        try:
            self.c.execute('INSERT INTO QTASKS (ISOK,CONTENT,DATE,ISABORT) VALUES (?,?,?,?);', (isOK, content, date, isAbort))
            self.conn.commit()
        except:
            print("ERROR: failed to add task.")
            return -1
        print("isOK\tContent\t\t\t\t\tDate\t\t\t\tisAbort")
        print(str(isOK) + "\t" + str(content) + "\t\t\t\t\t" + str(date) + "\t\t" + str(isAbort))
        cursor = self.c.execute('select last_insert_rowid();')
        return cursor.fetchall()[0][0]

    def qDel(self, id):
        try:
            self.c.execute("DELETE from QTASKS where ID=" + id)
            self.conn.commit()
        except:
            print("ERROR: failed to delete task" + id + ".")
            return -1
        return 0
    
    def qEdit(self, id, what, toWhat):
        try:
            sql = 'UPDATE QTASKS set ' + what + ' = "' + toWhat + '" where ID=' + id
            self.c.execute(sql)
            self.conn.commit()
        except:
            print("ERROR: failed to edit task" + id + ".")
            return -1
        return 0

    def qFind(self, what, isWhat):
        sql = 'SELECT * from QTASKS where ' + what + ' = "' + isWhat + '";'
        cursor = self.c.execute(sql)
        print("isOK\tID\tContent\t\t\t\t\tDate\t\t\tisAbort")
        for row in cursor:
            print(str(row[0]) + "\t" + str(row[1]) + "\t" + str(row[2]) + "\t\t\t\t\t" + str(row[3]) + "\t" + str(row[4]))

    def qList(self):
        cursor = self.c.execute('SELECT * from QTASKS')
        print("isOK\tID\tContent\t\t\t\t\tDate\t\t\tisAbort")
        for row in cursor:
            print(str(row[0]) + "\t" + str(row[1]) + "\t" + str(row[2]) + "\t\t\t\t\t" + str(row[3]) + "\t" + str(row[4]))

    def getByID(self, id):
        sql = 'SELECT * from QTASKS where ID = ' + id + ";"
        cursor = self.c.execute(sql)
        return cursor.fetchall()

