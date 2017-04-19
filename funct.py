#Debbie Yung
#Student Number: 10417380
#Price watch tracking product: Zelda games
#FUNCTIONS PAGE

import sqlite3
import sys
import urllib2
from bs4 import BeautifulSoup

#Soup Url Stuff
ozGameURL = "http://www.ozgameshop.com/gaming/sort-most-popular/refine-search/zelda"
mightyApeURL = "https://www.mightyape.com.au/games/all?q=zelda+stock%3Ainstock&sort=1"

page = urllib2.urlopen(ozGameURL)
page2 = urllib2.urlopen(mightyApeURL)
soup = BeautifulSoup(page,'html.parser')
soup2 = BeautifulSoup(page2,'html.parser')


#Function to insert
def insertNewEntry(prodnum, title, date, time, price, url): #Primary key created
    conn = sqlite3.connect('prices.db')
    params1 = (prodnum, title, url)
    conn.execute("INSERT INTO gameProduct (prodCode, prodName, prodSite) \
        VALUES (?, ?, ?)", params1);
    conn.commit()
    itemnum = getPrimaryKey(prodnum)
    params2 = (itemnum, date, time, price)
    conn.execute("INSERT INTO gamePrice (itemNum, prodDate, prodTime, prodPrice) \
        VALUES (?, ?, ?, ?)", params2);
    conn.commit()

def insertExistEntry(itemnum, date, time, price): #Primary Key for existing entry found; "Updating"
    conn = sqlite3.connect('prices.db')
    params = (itemnum, date, time, price)
    conn.execute("INSERT INTO gamePrice (itemNum, prodDate, prodTime, prodPrice) \
        VALUES (?, ?, ?, ?)", params);
    conn.commit()

def getPrimaryKey(prodcode):
    conn = sqlite3.connect('prices.db')
    cursor = conn.execute("SELECT itemNum FROM gameProduct WHERE prodCode = ?", (prodcode,))
    primaryKey = int(cursor.fetchone()[0])
    return primaryKey

#Function to Parse from Oz Game Shop
def parseOGS(url, date, time):
    conn = sqlite3.connect('prices.db')
    print "Updating prices from Oz Game Shop"
    #Parsing OzGameShop
    counter = 1
    for y in soup.findAll("div", {"class":"product4bg"}):
        #title
        for z in y.find("a"):
            title1 = z.attrs['alt']
        #product and price
        for x in y.findAll("div", {"class":"price"}):
            product1 = str(x.attrs['id'])
            prodnum1 = int(filter(str.isdigit, product1))
            price1 = x.attrs['data-product-price']
            try: #Some search results have no price
                price1 = float(price1[1:])
            except:
                continue
        #INSERT INTO DATABASE USING FUNCTIONS
        try: #To find if an item exists in database; retrieve PK
            pK = getPrimaryKey(prodnum1)
            insertExistEntry(pK, date, time, price1)
        except:
            insertNewEntry(prodnum1, title1, date, time, price1, url)
        counter = counter + 1
    print "Oz Game Shop update complete, {} prices inserted".format(counter)

def parseMA(url, date, time):
    conn = sqlite3.connect('prices.db')
    print "Updating prices from Mighty Ape"
    #Parsing MightyApe
    counter = 1
    for d in soup2.findAll("div", {"class":"product"}):
        for i in d.find("span", {"class":"price"}):
            price2 = float(i[1:])
        for f in d.find("a", {"class":"title"}):
            title2 = str(f)
        g = d.find("a").attrs['href']
        try: #Games only have 8 digit product numbers
            prodnum2 = int(g[-8:])
        except:
            print "Oops no games found."
            sys.exit()
        #INSERT INTO DATABASE USING FUNCTIONS
        try: #To find if an item exists in database; retrieve PK
            pK = getPrimaryKey(prodnum2)
            insertExistEntry(pK, date, time, price2)
        except:
            insertNewEntry(prodnum2, title2, date, time, price2, url)
        counter = counter + 1
    print "Mighty Ape update complete, {} prices inserted".format(counter)
