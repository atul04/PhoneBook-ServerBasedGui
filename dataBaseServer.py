# @Author: Atul Sahay <atul>
# @Date:   2018-08-23T20:25:27+05:30
# @Email:  atulsahay01@gmail.com
# @Filename: dataBaseServer.py
# @Last modified by:   atul
# @Last modified time: 2018-08-24T18:35:42+05:30

import os
import datetime
import sqlite3
from xmlrpc.server import SimpleXMLRPCServer

now = datetime.datetime.now()

class PhoneBook:
    # c, mydb
    def __init__(self):
        isFile = os.path.exists("PhoneBook_DB.db")
        if(not isFile):
            self.mydb = sqlite3.connect('PhoneBook_DB.db')
            self.c = self.mydb.cursor()
            self.c.execute('''CREATE TABLE Phone_info ( NAME varchar(50), PhoneNumber varchar(20) PRIMARY KEY, Address varchar(100), City varchar(40), Email varchar(80), Zip varchar(6), DOB varchar(20), Age int(10))''')
            self.mydb.commit()
            self.mydb.close()
    def insert(self,data):
        self.mydb = sqlite3.connect('PhoneBook_DB.db')
        self.c = self.mydb.cursor()
        for i in range(len(data[0])):
            age = now.year - int(data[6][i][-4:])
            # print(age)
            self.c.execute('''insert into Phone_info values ('{}', '{}', '{}','{}', '{}', '{}', '{}', {} )'''.format(data[0][i],data[1][i],data[2][i],data[3][i],data[4][i],data[5][i],data[6][i],age))
        self.mydb.commit()
        self.mydb.close()
    def select_all(self):
        self.mydb = sqlite3.connect('PhoneBook_DB.db')
        self.c = self.mydb.cursor()
        self.c.execute('''select * from Phone_info''')
        # for row in self.c:
        #     print("\t".join(str(i) for i in list(row)))
        data = self.c.fetchall()
        self.mydb.commit()
        self.mydb.close()
        return data
    def search(self,query):
        self.mydb = sqlite3.connect('PhoneBook_DB.db')
        self.c = self.mydb.cursor()
        self.c.execute('''Select * FROM Phone_info WHERE {}'''.format(query))
        data = self.c.fetchall()
        self.mydb.commit()
        self.mydb.close()
        return data
    def delete_entry(self,data):
        self.mydb = sqlite3.connect('PhoneBook_DB.db')
        self.c = self.mydb.cursor()
        for i in data:
            self.c.execute('''DELETE FROM Phone_info WHERE PhoneNumber='{}' '''.format(i))
        self.mydb.commit()
        self.mydb.close()

ph = PhoneBook()
phoneList = ['0010-9934809648','1010-7003045517','1234-8282926697','1234-6394947263']
nameList  = ['Atul Sahay','Aman Sahay','Aanchal Sahay','Pratima Sahay']
dobList   = ['28-05-1996','13-05-1998','28-05-1996','13-05-1998']
emailList = ['atulsahay01@gmail.com','sahayaman45@gmail.com','atulsahay01@gmail.com','sahayaman45@gmail.com']
addList   = ['House No. 1223, Shastri Nagar, Mumbai','House No. 123/B Main Road','Powai, Roadside','Flat No. 22, Sammer Towers , Rajiv Chawk']
cityList  = ['Mumbai','New Delhi','Mumbai','New Delhi']
zipList   = ['800023','800023','800023','800023']
data = [nameList, phoneList, addList, cityList, emailList, zipList, dobList]
isFile = os.path.exists("PhoneBook_DB.db")
d = ph.select_all()
if(len(d)==0):
    ph.insert(data)
with SimpleXMLRPCServer(('localhost', 1830),allow_none=True) as server:
    server.register_introspection_functions()

    server.register_function(ph.insert, 'INSERT')
    server.register_function(ph.select_all, 'SELECTALL')
    server.register_function(ph.search, 'SEARCH')
    server.register_function(ph.delete_entry, 'DELETEENTRY')
    server.serve_forever()
