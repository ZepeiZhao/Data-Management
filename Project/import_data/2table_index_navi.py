import pymysql
import csv
import json
import requests
from decimal import Decimal
import decimal
from datetime import date

# database = 'world'
#
# table = ['country','city','countrylanguage']
# tabledic = {'city':'CountryCode','country':'Code','countrylanguage':'CountryCode'}

database = 'basketballWoman'
table = ['players','players_teams','awards_players']
tabledic = {'players_teams':'playerID','players':'bioID','awards_players':'playerID'}

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

for j in result_[1]:
    j['table'] = table[1]
for g in result_[2]:
    g['table'] = table[2]
print(result_[1])

list_key = []
for i in result_[0]:
    list_key.append(i[tabledic[table[0]]])
list_key = list(set(list_key))
#print(len(result_[2]))

dic = {}
for k in list_key:
    tmp_list = []
    for h in result_[1]:
        if h[tabledic[table[1]]] == k:
            tmp_list.append(h)

    #dic[k] = tmp_list
    for j in result_[2]:
        if j[tabledic[table[2]]] == k:
            tmp_list.append(j)
#
    dic[k] = tmp_list
print(dic)
dic_new = {}
dic_new[table[0]] = dic
print(dic_new)
#
try:
    inverted_json = json.dumps(dic_new, default=default)
    url = 'https://inf551-d17d1.firebaseio.com/%s.json' %table[0]
    response = requests.put(url, inverted_json)
    if response.status_code == 200:
        print('success')
    else:
        print('Upload failed because:{}'.format(response.text))
except:
    print('Failed'.format())