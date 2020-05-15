import pymysql
import csv
import json
import requests
from decimal import Decimal
import decimal
from datetime import date

database = 'sakila'
table=['film_actor','actor']
tabledic = {'actor':'actor_id','film_actor':'actor_id'}

table1=['film_actor','film']
tabledic1 = {'film':'film_id','film_actor':'film_id'}

def connect(localhost,port_num,username,pas,data):
  db = pymysql.connect(host=localhost,
                         port=port_num,
                         user=username,
                         password=pas,
                         database=data,
                         charset='utf8')
  cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
  return {"db": db, "cursor": cursor}

def default(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    if isinstance(obj,date):
        return str(obj)
    raise TypeError("Object of type '%s' is not JSON serializable" % type(obj).__name__)

result_=[]
for tablename in table:
    sql = "select * from %s" % tablename
    cur = connect('127.0.0.1', 3306, 'root', 'zzp3221Z', database)['cursor']
    cur.execute(sql)
    result = cur.fetchall()
    result_.append(result)

for i in result_[1]:
    i['table'] = table[1]

print(len(result_[0]))
list_key = []
for i in result_[0]:
    list_key.append(i[tabledic[table[0]]])
list_key = list(set(list_key))

#print(len(result_))

dic = {}
for k in list_key:
    tmp_list = []
    for h in result_[1]:
        if h[tabledic[table[1]]]==k:

            tmp_list.append(h)
           # tmp_list.append()
    dic[k] = tmp_list
dic_result = {}
dic_result[table[1]]=dic
print(dic_result)

result_1=[]
for tablename in table1:
    sql = "select * from %s" % tablename
    cur = connect('127.0.0.1', 3306, 'root', 'zzp3221Z', database)['cursor']
    cur.execute(sql)
    result1 = cur.fetchall()
    result_1.append(result1)

for i in result_1[1]:
    i['table'] = table1[1]

# print(len(result_[0]))
list_key1 = []
for i in result_1[0]:
    list_key1.append(i[tabledic1[table1[0]]])
list_key1 = list(set(list_key1))

#print(len(result_))

dic1 = {}
for k in list_key1:
    tmp_list = []
    for h in result_1[1]:
        if h[tabledic1[table1[1]]]==k:

            tmp_list.append(h)
           # tmp_list.append()
    dic1[k] = tmp_list

dic_result[table1[1]]=dic1
print(dic_result.keys())



try:
    inverted_json = json.dumps(dic_result, default=default)
    url = 'https://inf551-d17d1.firebaseio.com/%s.json' %table[0]
    response = requests.patch(url, inverted_json)
    if response.status_code == 200:
        print('success')
    else:
        print('Upload failed because:{}'.format(response.text))
except:
    print('Failed'.format())