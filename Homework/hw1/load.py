from collections import defaultdict
import requests
import re
import json
import csv
import sys
import pandas as pd

#python3 load.py country.csv city.csv countrylanguage.csv

csvpath1 = sys.argv[1]
csvpath2 = sys.argv[2]
csvpath3 = sys.argv[3]

def remove_quote(_str):
    if not _str: return
    temp = ""
    for i in _str:
        if i == "'":
            continue
        else: temp += i
    return temp

my_dict1 = {}
my_dict2 = {}
my_dict3 = {}

def dict_change(original_dict, my_dict):
    for key in original_dict.keys():
        value = original_dict[key]
        new_key = remove_quote(key)
        if isinstance(value, dict):
            temp_dic = {}
            dict_change(value, temp_dic)
            my_dict.update({new_key: temp_dic})
        else:
            value = remove_quote(value)
            my_dict.update({new_key: value})

def strip_dict(d):
    return {key: strip_dict(value)
    if isinstance(value, dict)
    else value.replace('(', ' ').replace('-', ' ').replace(')', ' ').replace('/', ' ').replace('[', ' ').replace(']',' ')
    for key, value in d.items()}

#open file and data clean
    
def csv_j(csvfile):
    f = pd.read_csv(csvfile, encoding='latin-1')
    fd = pd.DataFrame(f)
    if csvfile == csvpath1:
        fd = fd.drop(columns=["Unnamed: 15"])
        fd = fd.drop(index=[14, 18, 37, 44, 74, 149, 228, 229])
        fd = fd.reset_index()
        fd.rename(columns={'# Code': 'Code', ' Name': 'Name', ' SurfaceArea': 'SurfaceArea', ' LocalName': 'LocalName',
                           ' GovernmentForm': 'GovernmentForm', ' HeadOfState': 'HeadOfState',
                           ' Continent': 'Continent', ' Region': 'Region', ' Code2': 'Code2'}, inplace=True)
        fd = fd.drop(columns=['index'])
        fd = fd.set_index('Code').to_dict(orient='index')
        dict_change(fd, my_dict1)
        fd1 = json.dumps(my_dict1)
        url = 'https://inf551-a33ef.firebaseio.com/world/country.json'
        response = requests.put(url, fd1)
        print('country.csv-DONE')
        dict1 = strip_dict(my_dict1)
        data1 = pd.DataFrame(dict1)
        country = data1.T
        ls1 = data1.values.tolist()
        del ls1[3:9]
        del ls1[6]
        return country, ls1
    elif csvfile == csvpath2:
        fd.rename(columns={'# ID': 'ID', ' District': 'District', ' Name': 'Name', ' CountryCode': 'CountryCode'},
                  inplace=True)
        fd.index = fd.index.map(str)
        fd = fd.to_dict(orient='index')
        dict_change(fd, my_dict2)
        fd2 = json.dumps(my_dict2)
        url = 'https://inf551-a33ef.firebaseio.com/world/city.json'
        response = requests.put(url, fd2)
        print('city.csv-DONE')
        dict2 = strip_dict(my_dict2)
        data2 = pd.DataFrame(dict2)
        city = data2.T
        ls2 = data2.values.tolist()
        del ls2[0]
        del ls2[-1]
        return city, ls2
    elif csvfile == csvpath3:
        fd.rename(columns={'# CountryCode': 'CountryCode', ' Language': 'language'}, inplace=True)
        fd.index = fd.index.map(str)
        fd = fd.to_dict(orient='index')
        dict_change(fd, my_dict3)
        fd3 = json.dumps(my_dict3)
        url = 'https://inf551-a33ef.firebaseio.com/world/countrylanguage.json'
        response = requests.put(url, fd3)
        print('countrylanguage-DONE')
        dict3 = strip_dict(my_dict3)
        data3 = pd.DataFrame(dict3)
        countrylanguage = data3.T
        ls3 = data3.values.tolist()
        del ls3[-1]
        return countrylanguage, ls3
    else:
        print('wrong file path')

def tableword(ls):
    lists = []
    for each in ls:
        for i in each:
            cut = i.split()
            lists.extend(cut)
    lists = list(set(lists))
    return lists

# Build invert index
def index(tablename, table, name, allWords):
    keydf = dict()
    for key in allWords:
        df2 = dict()
        temp = []
        code = []
        for j in name:
            tablelist = []
            if len(table[(table[j].str.strip().str.find(key) >= 0)].index.tolist()) > 0:
                temp.append(j)
                code = list(set(code + table[(table[j].str.strip().str.find(key) >= 0)].index.tolist()))
                df2['TABLE'] = tablename
                df2['COLUMN'] = temp
                df2['CODE'] = code
                tablelist.append(df2)
                keydf[key] = tablelist
    return keydf

def index2(alldf, tablename, table, name, allWords):
    s='';x=0
    if tablename == 'city':
        s = 'ID';x=0
    if tablename == 'countrylangauge':
        s = 'LANGUAGE';x=1
    for key in allWords:
        df2 = dict()
        temp = []
        code = []
        la = []
        allist = []
        for j in name:
            tablelist = []
            if len(table[(table[j].str.strip().str.find(key) >= 0)].index.tolist()) > 0:
                temp.append(j)
                code = list(set(code + table[(table[j].str.strip().str.find(key) >= 0)].index.tolist()))
                for cou_code in code:
                    la.append(table.iat[int(cou_code),x])
                df2['TABLE'] = tablename
                df2['COLUMN'] = temp
                df2[s] = list(set(la))
                tablelist.append(df2)
                allist = tablelist
        if key in alldf:
            alldf[key].extend(allist)
        else:
            alldf[key] = allist
    #print(alldf)
    return alldf

def cleanword(allWords):
    str = ' '
    import re
    pat = '[a-zA-Z]+'
    allWords = re.findall(pat, str.join(allWords))
    return allWords

# Capital to Lower
def c_to_l(dict_info):
    new_dict = {}
    for i, j in dict_info.items():
        new_dict[i.lower()] = j
    return new_dict

if __name__ == '__main__':
    country, ls1 = csv_j(csvpath1)
    city, ls2 = csv_j(csvpath2)
    countrylanguage, ls3 = csv_j(csvpath3)

    list1 = tableword(ls1);
    list2 = tableword(ls2);
    list3 = tableword(ls3)

    allword = []
    allword.extend(list1);
    allword.extend(list2);
    allword.extend(list3)
    allWords = list(set(allword))

    countrycolumn = ["Name", "Continent", "Region", "SurfaceArea", "LocalName", "GovernmentForm", "HeadOfState",
                     "Code2"]
    citycolumn = ["Name", "District", "CountryCode"]
    languagecolumn = ["language"]
    allWords = set(cleanword(allWords))
    allWords = list(allWords)
    wordlist = []
    for each in allWords:
        if len(each.strip())>=3:
            wordlist.append(each.strip())
    wordlist = set(wordlist)

    df1 = index('country', country, countrycolumn, wordlist)
    df2 = index2(df1, 'city', city, citycolumn, wordlist)
    df3 = index2(df2, 'countrylangauge', countrylanguage, languagecolumn, wordlist)
    new_dict = c_to_l(df3)
    invertIndex = json.dumps(new_dict)
    #print('INVERT INDEX:',invertIndex)
    url = 'https://inf551-a33ef.firebaseio.com/index.json'
    response = requests.put(url, invertIndex)
    print('Invert Index-DONE')
