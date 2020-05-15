import mysql.connector
import csv
import sys

# get table name
def tableName():
    
    tablename = []
    cursor.execute("show tables")
    for x in cursor:
        tablename.append(x[0].replace(',',''))
    return tablename

# get column name
def getcol(tablename_):
    cur = info.cursor()
    col = []
    sql1 = "select COLUMN_NAME from information_schema.COLUMNS where table_name= " + "'" + tablename_ + "'"
    # print(sql1)
    cur.execute(sql1)
    for x in cur:
        col.append(x[0].replace(',', ''))
    return col

# get primary key
def getpk(tablename_):
    primarykey = []
    pk = info.cursor()
    sql3 = "SELECT column_name FROM INFORMATION_SCHEMA.`KEY_COLUMN_USAGE` WHERE table_name=" + "'"+ tablename_+ "'" + "AND CONSTRAINT_SCHEMA='world' AND constraint_name='PRIMARY'"
    pk.execute(sql3)
    for i in pk:
        primarykey.append(i[0].replace(',',''))
    return primarykey
#print(getcol('city'))

# transfer to csv
def tocsv():
    tablename = tableName()
    for tablename_ in tablename:
        sql = 'select * from ' + tablename_
        cursor.execute(sql.encode('utf-8'))
        data = cursor.fetchall()
        col = getcol(tablename_)
        primarykey = getpk(tablename_)
        #print(primarykey)
        for i in primarykey:
            for j in range(len(col)):
                if i == col[j]:
                    col[j] = '#'+ i
        #print(col)
        with open(tablename_ + '.csv', 'w', encoding='utf-8') as f:
            write = csv.writer(f, dialect='excel', delimiter=',')
            write.writerow(col)
            datanew = []
            for i in data:
                datanew.append(list(i))
            listnew = []
            for item in datanew:
                listtmp = []
                for i in range(len(item)):
                    if ',' in str(item[i]):
                        item[i] = '"'+item[i]+'"'
                        listtmp.append(item[i])
                    else:
                        listtmp.append(item[i])
                listnew.append(listtmp)

            for item in listnew:
                write.writerow(item)

if __name__ == "__main__":
    db = sys.argv[1]
    db = db.replace('"','')
    cnx = mysql.connector.connect(user='inf551', password='inf551', host='localhost', database=db)
    info = mysql.connector.connect(user='inf551', password='inf551', host='localhost', database='information_schema')
    cursor = cnx.cursor()
    tocsv()
    print('DONE')
    
