"""Python implementation for getting a list of categories from eBay



Usage: python getCategories.py [options]

Options:
  -r ..., --render=...       Render specifi category from the API
  -R, --rebuild              Update local SQLite3 Database fetching all values from the API
  -h, --help                 show this help info

Examples:
  getCategories.py             generates a "no arguments exception".
  getCategories.py -r 14567  generates an html file called 14567.html with the category information from ebay.
  getCategories.py --rebuild calls the ebay getCategory API and updates the local database with the values fetched.
  getCategories.py -h        shows this help info


  Database Structure
  Category                  Category Relationships
 ________________         __________________________
id               INT        category_id INT (foreignkey references Category.id)
name             VARCHAR    child_id INT (foreignkey references Category.id)
level            INT         
BestOfferEnabled BOOLEAN   

The Tree Structure looks like this:
                       cat1 
                     /   |  \\
                cat2__cat3   cat4
                         | \\  |
                       cat5  cat6
Calls to the eBay API are  optimized by first retrieving level=1 categories and saving it to the local db if it doesn't exist
Then, for each category of level=1 a request to the API is made to fetch all children categories from level=[2..6], and every time
a children is fetched, which at the same time is a category, is saved in the local db as long as it doesn't exist yet.
Like this, every time a categroy is iterated, less categories will be saved in the database but the relationships will be still recorded.

This program is developed for Polymath Ventures LLC as part of the Polymath Challenge.
Developed by Juan David Arroyave using python3.
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::::::::::::::::::: Juan David Arroyave :::::::::::::::::::
::::::::::::: http://www.juandavidarroyave.com ::::::::::::
::::::::::::::::: me@juandavidarroyave.com ::::::::::::::::
::::::::::::::::::::::::::: 2015 ::::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
"""

__author__ = "Juan David Arroyave (me@juandavidarroyave.com)"
__version__ = "$Revision: 0.1 $"
__date__ = "$Date: 2015/07/03 20:03:30 $"
__copyright__ = "Copyright (c) 2015 Juan David Arroyave"
__license__ = "Python"


import sys
import getopt
import xmltodict
import jinja2
import urllib
import sqlite3 as lite
import json
from itertools import cycle
class RefreshDatabase:

  def __init__(self):
    #self.pCatId = catId
    self.reqData = '''<?xml version="1.0" encoding="utf-8"?>\n
    <GetCategoriesRequest xmlns="urn:ebay:apis:eBLBaseComponents">\n
    <CategorySiteID>0</CategorySiteID>\n
    <LevelLimit>{0}</LevelLimit>\n
    <ViewAllNodes>True</ViewAllNodes>\n
    <DetailLevel>ReturnAll</DetailLevel>\n
    <RequesterCredentials>\n
    <eBayAuthToken>AgAAAA**AQAAAA**aAAAAA**t2XTUQ**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6wFk4GhCpaCpQWdj6x9nY+seQ**L0MCAA**AAMAAA**pZOn+3Cb/dnuil4E90EEeGpHlaBVP0VpLebK58TPQ210Sn33HEvjGYoC9UYVqfbhxte6wp8/fPL795uVh9/4X00HC3wAfzcV+wobN2NfReqWAXFdfuj4CbTHEzIHVLJ8tApLPlI8Nxq6oCa5KsZf5L+An85i2BnohCfscJtl9OcZYnyWnD0oA4R3zdnH3dQeKRTxws/SbVCTgWcMXBqL9TUr4CrnOFyt0BdYp4lxg0HbMv1akuz+U7wQ3aLxJeFoUow20kUtVoTIDhnpfZ40Jcl/1a2ui0ha3rl9D3oA66PUhHSnHJTznwtp1pFLANWn9I49l9rrYbzzobB6SGf18LK/5cqSwse3AWMXJkFVbgFM7e5DZBv59S1sCRdEjzw8GciKYSxGDqu8UJQHgL/QPiTFhtj2Ad/vjZ/6PLBVA9rhOxJnlhCvLXmWZIf1NNcckN8uEEIqK7Wn0DdDi8p44ozIWNaIQ319HjYYOBp4a5FLUjwXCamoqfSjYli5ikqe0jwn+LxnOWblY47TFhruRQpYaBAro4VbgirwNYT7RlEGz+u7ol9A873dnqEZgdXWfrWkyxyKGeXHnHjiynfL/JDCdl2U2s+s5iOd8hp6QklHevPOlOtZgW+K/eFIv53UATQi4vMptUKEeD6QxFzvxP7wRAkKIQZUq+LKB8lZBP/Epjni47HXKpwQdgbTWbyfHpSF3A52u8koUY9chiBk1FCpqjBM/BT5tjhIlrQUVeWUUyGeQ49sJJvaeVnaavo9</eBayAuthToken>\n
    </RequesterCredentials>\n
    {1}
    </GetCategoriesRequest>'''
    #self.reqData.replace("CATEGORY_PARENT_ID", self.pCatId, 1)
    ebay = self.loadData()
    self.saveData(ebay)
  def loadData(self,parentId = 0,maxLevel=1):
    appendString = ""
    if parentId is not 0:
        appendString = "<CategoryParent>{0}</CategoryParent>".format(parentId)
    data = self.reqData.format(maxLevel,appendString)
    binary_data = ((data).encode("UTF-8"))
    request = urllib.request.Request('https://api.sandbox.ebay.com/ws/api.dll',binary_data)
    request.add_header('X-EBAY-API-CALL-NAME', 'GetCategories')
    request.add_header('X-EBAY-API-APP-NAME', 'EchoBay62-5538-466c-b43b-662768d6841')
    request.add_header('X-EBAY-API-CERT-NAME', '00dd08ab-2082-4e3c-9518-5f4298f296db')
    request.add_header('X-EBAY-API-DEV-NAME', '16a26b1b-26cf-442d-906d-597b60c41c19')
    request.add_header('X-EBAY-API-SITEID', '0')
    request.add_header('X-EBAY-API-COMPATIBILITY-LEVEL', '861')
    file = urllib.request.urlopen(request)
    data = file.read()
    file.close()
    # print ((xmltodict.parse(data))['rss']['channel']['title'])
    #print (xmltodict.parse(data))
    #print (data)
    return xmltodict.parse(data)
  def saveData(self,ebay):
    if(ebay['GetCategoriesResponse']['Ack'].lower() == "success"):
        print("Information for Level=1 categories successfully retrieved from Ebay")
        con = None
        categories = ebay['GetCategoriesResponse']['CategoryArray']['Category']
        try:
            con = lite.connect('ebay_categories.db')
            cur = con.cursor()
            #Init Database
            cur.execute('DROP TABLE IF EXISTS category_relation')
            cur.execute('DROP TABLE IF EXISTS category')
            cur.execute("CREATE TABLE category(id INTEGER PRIMARY KEY, category_ebay_id INTEGER,name TEXT,level INTEGER, best_offer BOOLEAN);")
            cur.execute("CREATE TABLE category_relation(parent_id INTEGER, child_id INTEGER,FOREIGN KEY(parent_id) REFERENCES category(id),FOREIGN KEY(child_id) REFERENCES category(id));")
            if(int(ebay['GetCategoriesResponse']['CategoryCount']) == 1):
                cat = categories
                best_offer = False
                if 'BestOfferEnabled' in categories:
                    best_offer = True
                cur.execute("INSERT INTO category(name,category_ebay_id,level,best_offer) SELECT  ?, ?, ?, ? WHERE NOT EXISTS(SELECT 1 FROM category WHERE category_ebay_id = ?);", (cat['CategoryName'],cat['CategoryID'], 1, best_offer,cat['CategoryID']))
                categoryid = cur.lastrowid
                for x in range(2,7):
                    dashes = ("-" * (int(x/len("-"))+1))[:x]
                    print(dashes+"Fetching children from level {1} for Category {0}...".format(cat['CategoryID'],x))
                    values = self.loadData(int(cat['CategoryID']),x)
                    if(values['GetCategoriesResponse']['Ack'].lower() != "success"):
                        print(dashes+"Error fetching children from level {1} for category {0}".format(cat['CategoryID'],x))
                        sys.exit(2)
                    else:
                        print (dashes+"Success retrieving children from level {1} for category {0}".format(cat['CategoryID'],x))
                    count = int(values['GetCategoriesResponse']['CategoryCount'])
                    categories = values['GetCategoriesResponse']['CategoryArray']['Category']
                    if count == 1:
                        cat = categories
                        best_offer = False
                        if 'BestOfferEnabled' in categories:
                            best_offer = True
                        cur.execute("INSERT INTO category(name,category_ebay_id,level,best_offer) SELECT  ?, ?, ?, ? WHERE NOT EXISTS(SELECT 1 FROM category WHERE category_ebay_id = ?);", (cat['CategoryName'],cat['CategoryID'], x, best_offer,cat['CategoryID']))
                        childid = cur.lastrowid
                        cur.execute("SELECT * FROM category WHERE category_ebay_id = "+cat['CategoryID']+";")
                        row = cur.fetchone()
                        childid = row[0] #category_id in row selected
                        cur.execute("INSERT INTO category_relation(parent_id,child_id) VALUES(?,?);",(categoryid,childid))
                    else:
                        for cat in categories:
                            best_offer = False
                            if 'BestOfferEnabled' in categories:
                                best_offer = True
                            cur.execute("INSERT INTO category(name,category_ebay_id,level,best_offer) SELECT  ?, ?, ?, ? WHERE NOT EXISTS(SELECT 1 FROM category WHERE category_ebay_id = ?);", (cat['CategoryName'],cat['CategoryID'], x, best_offer,cat['CategoryID']))
                            childid = cur.lastrowid
                            cur.execute("SELECT * FROM category WHERE category_ebay_id = "+cat['CategoryID']+";")
                            row = cur.fetchone()
                            childid = row[0] #category_id in row selected
                            cur.execute("INSERT INTO category_relation(parent_id,child_id) VALUES(?,?);",(categoryid,childid))
            else:
                for cat in categories:
                    best_offer = False
                    if 'BestOfferEnabled' in cat:
                        best_offer = True
                    cur.execute("INSERT INTO category(name,category_ebay_id,level,best_offer) SELECT  ?, ?, ?, ? WHERE NOT EXISTS(SELECT 1 FROM category WHERE category_ebay_id = ?);", (cat['CategoryName'],cat['CategoryID'], 1, best_offer,cat['CategoryID']))
                    categoryid = cur.lastrowid
                    for x in range(2,7):
                        dashes = ("-" * (int(x/len("-"))+1))[:x]
                        print(dashes+"Fetching children from level {1} for Category {0}...".format(cat['CategoryID'],x))
                        values = self.loadData(int(cat['CategoryID']),x)
                        if(values['GetCategoriesResponse']['Ack'].lower() != "success"):
                            print(dashes+"Error fetching children from level {1} for category {0}".format(cat['CategoryID'],x))
                            sys.exit(2)
                        else:
                            print (dashes+"Success retrieving children from level {1} for category {0}".format(cat['CategoryID'],x))
                        count = int(values['GetCategoriesResponse']['CategoryCount'])
                        categories = values['GetCategoriesResponse']['CategoryArray']['Category']
                        if count == 1:
                            cat = categories
                            best_offer = False
                            if 'BestOfferEnabled' in categories:
                                best_offer = True
                            cur.execute("INSERT INTO category(name,category_ebay_id,level,best_offer) SELECT  ?, ?, ?, ? WHERE NOT EXISTS(SELECT 1 FROM category WHERE category_ebay_id = ?);", (cat['CategoryName'],cat['CategoryID'], x, best_offer,cat['CategoryID']))
                            childid = cur.lastrowid
                            cur.execute("SELECT * FROM category WHERE category_ebay_id = "+cat['CategoryID']+";")
                            row = cur.fetchone()
                            childid = row[0] #category_id in row selected
                            cur.execute("INSERT INTO category_relation(parent_id,child_id) VALUES(?,?);",(categoryid,childid))
                        else:
                            for cat in categories:
                                best_offer = False
                                if 'BestOfferEnabled' in categories:
                                    best_offer = True
                                cur.execute("INSERT INTO category(name,category_ebay_id,level,best_offer) SELECT  ?, ?, ?, ? WHERE NOT EXISTS(SELECT 1 FROM category WHERE category_ebay_id = ?);", (cat['CategoryName'],cat['CategoryID'], x, best_offer,cat['CategoryID']))
                                childid = cur.lastrowid
                                cur.execute("SELECT * FROM category WHERE category_ebay_id = "+cat['CategoryID']+";")
                                row = cur.fetchone()
                                childid = row[0] #category_id in row selected
                                cur.execute("INSERT INTO category_relation(parent_id,child_id) VALUES(?,?);",(categoryid,childid))
            con.commit()

        except lite.Error as e:
            print (e.args[0])
            sys.exit(2)
        finally:
            if con:
                con.close()
    else:
        print ("Error retrieving data from Ebay.")
        sys.exit(2)

class GetCategory:
    def __init__(self, categoriId):
        if categoriId is not None:
            #print (categoriId)
            rows = self.fetchData(categoriId,1)
            total = rows.copy()
            for row in rows:
                total += self.fetchData(row[1])
            self.stringify(total)
            templateLoader = jinja2.FileSystemLoader( searchpath="" )
            templateEnv = jinja2.Environment( loader=templateLoader )
            TEMPLATE_FILE = str('Templates/template.html')
            template = templateEnv.get_template( TEMPLATE_FILE )
            outputText = template.render()
            f = open('Templates/'+str(categoriId)+'.html', 'w');
            f.write(outputText)
            f.close()
        else:
            print ("You must specify at least one category. Use --help to see example usages.")
            sys.exit(2)
    def fetchData(self, val, mode = 0):
        con = None
        try:
            con = lite.connect('ebay_categories.db')
            cur = con.cursor()
            selectid = val
            if mode == 1:
                cur.execute("SELECT id from category WHERE category_ebay_id = "+val+";")
                resu = cur.fetchone()
                selectid = resu[0]
            cur.execute("""
                    SELECT DISTINCT category.name as child_name,category.id as child_id,category.category_ebay_id as child_ebay_id, 
                    category.level as child_level, category.best_offer as child_offer,parents.parent_name,parent as parent_id, 
                    parents.parent_ebay_id, parents.parent_level, parents.parent_offer FROM category 
                    JOIN 
                    (SELECT DISTINCT category.name as parent_name, category.category_ebay_id as parent_ebay_id, category.level as parent_level, 
                    category.best_offer as parent_offer,category_relation.parent_id as parent, category_relation.child_id as child 
                    FROM category_relation 
                    LEFT JOIN 
                    category ON category.id = parent WHERE category.id = """+str(selectid)+""") as parents 
                    ON parents.child = category.id
                    ORDER BY child_level
                    """)
            return cur.fetchall()
        except lite.Error as e:
            print (e.args[0])
            sys.exit(2)
        finally:
            if con:
                con.close()
    def stringify(self,rows):
        count = 1
        level = 1
        running = True
        licycle = iter(rows)
        nextelem = next(licycle)
        json_string = '{"name" :"' + nextelem[0] + '"'
        endcount = len(rows)
        levelchange = False
        bracketcount = 0
        json_string = '{'
        changes = 0
        while running:
                thiselem = nextelem
                try:
                    nextelem = next(licycle)
                except:
                    nextelem = None
                #this means next element is a nested child
                if count == 1:
                    json_string += '"name":'+'"'+thiselem[0]+'"'
                if nextelem is not None:
                    if thiselem[3] == nextelem[3]:
                        json_string += '},'
                        json_string += '{"name":'+'"'+nextelem[0]+'"'
                    else:
                        json_string += ',"children":[{"name":"'+thiselem[0]+'"'
                        changes += 1
                        bracketcount += 1
                else:
                    json_string += '}'
                    for x in range(1,bracketcount):
                        json_string += ']}'
                    running = False
                count += 1
        json_string += "]}"
        j = json.loads(json_string)
        f = open('Templates/data.json', 'w');
        f.write(json.dumps(j))
        f.close()
        
def usage():
  print (__doc__)

def main(argv):
  try:                                
    opts, args = getopt.getopt(argv, "hr:", ["help","render=","rebuild"])
  except getopt.GetoptError:          
    print ("Something went wrong with how you called the program. Try --help for information on how to use it")                        
    sys.exit(2)                     
  for opt, arg in opts:                
    if opt in ("-h", "--help"):      
      usage()                     
      sys.exit()                                   
    elif opt in ("-r", "--render"): 
      GetCategory(arg)
    elif opt in ("--rebuild"):
      RefreshDatabase()            

if __name__ == "__main__":
  main(sys.argv[1:])
