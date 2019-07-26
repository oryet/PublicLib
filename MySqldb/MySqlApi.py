#!/usr/bin/python3
# coding=utf-8

import pymysql

class MySqlApi():
    def __init__(self, db):
        # prepare a cursor object using cursor() method
        self.cursor = db.cursor()
        self.db = db

    def showaddrlist(self, sql):
        # print (sql)
        try:
            # Execute the SQL command
            self.cursor.execute(sql)
            # Fetch all the rows in a list of lists.
            results = self.cursor.fetchall()
            for row in results:
                # print (row)
                addr = row[0]
                ip = row[1]
                port = row[2]
                curvetime = row[3]

                # Now print fetched result
                print("addr = %s,ip = %s,port = %d,curvetime = %s" % \
                      (addr, ip, port, curvetime))
        except:
            import traceback
            traceback.print_exc()
            print("Error: unable to fetch data")

    def showdata(self, cursor, sql):
        pass

    def execut(self, sql):
        try:
            # Execute the SQL command
            self.cursor.execute(sql)
            # Commit your changes in the database
            self.db.commit()
        except:
            # Rollback in case there is any error
            self.db.rollback()