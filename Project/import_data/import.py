import pandas as pd
import pymysql
import json
import requests
import decimal
from decimal import Decimal
from datetime import date

# import sys
# name=sys.argv[1]
databases=['world','sakila','basketballWoman']
key_word_list=[]
#create container which contains all tuples of the whole database
container=[]
#connect to mysql
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

# upload data to firebase
# table_list=list_table('127.0.0.1',3306,'root','zzp3221Z','sakila')
# database = 'world'
# table_list = ['city','country','countrylanguage']
database = 'sakila'
table_list = ['actor','film_actor','film']
# database = 'basketballWoman'
# table_list = ['awards_players','players','players_teams']

key_word_list_new=[]
for name in table_list:
    sql = "select * from %s" % name
    cur=connect('127.0.0.1',3306,'root','zzp3221Z',database)['cursor']
    cur.execute(sql)
    result = cur.fetchall()
    for i in result:
        i['table']=name
    container+=result#build container
    # print(result[1])
    final_dict={}
    for i in result:
        k=result.index(i)
        v=i
        final_dict[k]=i
        words=list(i.values())

        key_word_list+=words



    data=json.dumps(final_dict,default=default)
    # url = 'https://inf551-d17d1.firebaseio.com/%s/' %database +name+ '.json'
    # response = requests.patch(url, data)
    # print(response)
# print(key_word_list_new)
key_word_list=list(set(key_word_list))
keys=key_word_list[:]
for i in key_word_list:
    if type(i) == int or type(i) == float or type(i)==decimal.Decimal:
        keys.remove(i)
keyWords=keys
mid_list=[]
for val in keyWords:
    val= str(val).replace('-', ' ')
    val1=val.split(' ')
    mid_list+=val1
mid_keys=list(set(mid_list))
fin_keys=list(filter(None,mid_keys))
keyWords=fin_keys

#get key based on value in dict
def get_key (dict, value):
    return [k for k, v in dict.items() if v == value]
inverted_index={}
for word in keyWords:
    word=str(word)
    # columns={}
    # column=[]
    tup_dict={}
    i=0
    for tup in container:
        for val in list(tup.values()):
            if word in str(val):
                # column+= get_key(tup,val)
                tup_dict[i]=tup
                i+=1
    # columns['column_list']=column
    # final=dict(list(columns.items())+list(tup_dict.items()))
    inverted_index[word]=tup_dict
# print(inverted_index)

#deal with key words in order to make sure the data can be uploaded
fin_dict={}
for keyword,val in inverted_index.items():
    new_key=''
    for j in keyword:
        if j == '.' or j == '[' or j == ']' or j == '/' or j == '\\' or j=='$':
            continue
        new_key+=j
    fin_dict[new_key]=val

#delete the empty or symbol index node
# print(fin_dict)
fin_d = {}
for k in list(fin_dict.keys()):
    if k=='' or k=='&' or k==',' or k=='.':
        del(fin_dict[k])
    else:
        fin_d[k.lower()]=fin_dict[k]

# list_ = fin_d.keys()
# print(len(list_))


# inverted_json = json.dumps(fin_d, default=default)
# print(inverted_json)


try:
    inverted_json = json.dumps(fin_d, default=default)
    url = 'https://inf551-d17d1.firebaseio.com/%s/index.json' %database
    response = requests.put(url, inverted_json)
    if response.status_code == 200:
        print('success')
    else:
        print('Upload failed because:{}'.format(response.text))
except:
    print('Failed'.format())
#
#
db=connect('127.0.0.1',3306,'root','zzp3221Z',database)['db']
cur.close()
db.close()
