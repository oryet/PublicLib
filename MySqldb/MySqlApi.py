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
                rectime = row[3]

                # Now print fetched result
                print("addr = %s,ip = %s,port = %d,rectime = %s" % \
                      (addr, ip, port, rectime))
        except:
            import traceback
            traceback.print_exc()
            print("Error: unable to fetch data")

    def selectip2addr(self, sql):
        try:
            # Execute the SQL command
            self.cursor.execute(sql)
            # Fetch all the rows in a list of lists.
            results = self.cursor.fetchall()
            for row in results:
                # print (row)
                return row[0]
        except:
            import traceback
            traceback.print_exc()
            print("Error: unable to fetch data")

    def showdata(self, sql):
        try:
            # Execute the SQL command
            self.cursor.execute(sql)
            # Fetch all the rows in a list of lists.
            results = self.cursor.fetchall()
            for row in results:
                data = []
                # print (row)
                addr = row[0]
                rectime = row[1]
                curvetime = row[2]

                for i in range(3, len(row)):
                    data += [row[i]]

                # Now print fetched result
                print("addr = %s, rectime = %s, curvetime = %s" % \
                      (addr, rectime, curvetime), data)

        except:
            import traceback
            traceback.print_exc()
            print("Error: unable to fetch data")

    def execut(self, sql):
        try:
            # Execute the SQL command
            self.cursor.execute(sql)
            # Commit your changes in the database
            self.db.commit()
            return 1
        except:
            # Rollback in case there is any error
            self.db.rollback()
            return 0