#Debbie Yung
#Student Number: 10417380
#Price watch tracking product: Zelda games


import funct
import sqlite3
import sys
import time
from prettytable import PrettyTable



#Arguments & URLs
oGSite = "Oz Game Shop"
mASite = "Might Ape"
date = time.strftime("%d/%m/%Y")
time = time.strftime("%X")
searchArg = sys.argv[1].lower()
param = sys.argv[2:] #any num of args after "search"/"history"


if searchArg == "update":
    conn = sqlite3.connect('prices.db')
    try: #to create table & populate  NOT WORKING
        conn.execute('''CREATE TABLE gamePrice
            (itemNum INTEGER,
            prodDate NUMERIC,
            prodTime NUMERIC,
            prodPrice NUMERIC,
            FOREIGN KEY(itemNum) REFERENCES gameProduct(itemNum));''')
        conn.execute('''CREATE TABLE gameProduct
            (itemNum INTEGER PRIMARY KEY AUTOINCREMENT,
            prodCode INT,
            prodName TEXT,
            prodSite TEXT);''')
        print "Detecting first run, creating database..."
        funct.parseOGS(oGSite, date, time)
        funct.parseMA(mASite, date, time)
    except: #just insert/populate without creating
        funct.parseOGS(oGSite, date, time)
        funct.parseMA(mASite, date, time)
    conn.close()

elif searchArg == "search":
    #Check for database for try/catch
    try:
        print 'search'
        searchParam = str(" ".join(param)).lower()
        #print searchParam
        conn = sqlite3.connect('prices.db')
        s = PrettyTable(["Item Num", "Name", "Store", "Price"])
        cursor = conn.execute("SELECT DISTINCT a.itemNum, prodName, prodSite, prodPrice FROM gamePrice AS a INNER JOIN gameProduct AS b ON a.itemNum = b.itemNum WHERE prodName LIKE ?", ('%'+searchParam+'%',))
        for row in cursor:
            s.add_row([row[0], row[1], row[2], row[3]])
        print s
    except:
        print "No search parameter detected. Enter an search title after 'history'."
elif searchArg == "history":
    #Check for database
    print 'history'
    try:
        searchParam = int(" ".join(param)) #itemnum
        conn = sqlite3.connect('prices.db')
        #update
        # conn.execute("UPDATE gamePrice SET prodPrice = 8.24 WHERE strftime('%S', prodTime) IN('21')")
        # conn.execute("UPDATE gamePrice SET prodPrice = 11.40 WHERE strftime('%M', prodTime) IN('05')")
        # conn.commit()

        e = PrettyTable(["Date", "Time", "Price"])
        cursor = conn.execute("SELECT DISTINCT prodDate, prodTime, prodPrice FROM gamePrice WHERE itemNum = ?", (searchParam,))
        for row in cursor:
            e.add_row([row[0], row[1], row[2]])
        print e
    except:
        print "No item number parameter detected. Enter an item number after 'history'."


else:
    print "Invalid parameter."
