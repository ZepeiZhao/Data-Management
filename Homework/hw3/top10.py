import csv
import sys
import datetime

# running time:0.010792 Seconds
# duration time of mysql execution: 0.0062 sec
# using mysql is faster than using python

# The time complexity of my code is o(nm),
# n and m are the length of table(dict) c and cl
# since there are at most two 'for' loop.
# In cltable function, I construct a dictionary to
# store language and CountryCode pair.
# So, it traverses langauge list and countrylanguage table in two loops.
# About improvement, using different data stucture may work better,
# list traversal is slower than other structure.
# Besides, reducing the number of loop also can help. 

# The time complexity is o(n).
# I use conditions as filters for every steps.
# For example, first, I choose official language as a constraint to reduce list length.
# So the space complexity is reduced.

def readCSV(csvFile):
    reader = csv.DictReader(csvFile)
    rows = [row for row in reader]
    csvFile.close()
    return rows

def newlist(dict_):
    res = []
    for i in dict_:
        temp = {}
        if dict_ == dict1:
            if i.keys() == '#Code' or 'Population':
                temp['#Code'] = i['#Code']
                temp['Population'] = i['Population']
                res.append(temp)
        else:
            if i.keys() == '#CountryCode' or '#Language' or 'IsOfficial':
                if i['IsOfficial'] == 'T':
                    temp['#CountryCode'] = i['#CountryCode']
                    temp['#Language'] = i['#Language']
                    res.append(temp)
    return res

#country table with population>1000000
def ctable(country):
    c = []
    for i in country:
        tmp = {}
        if 'Population' in i.keys():
            if int(i['Population']) > 1000000:
                tmp['#Code'] = i['#Code']
                tmp['Population'] = int(i['Population'])
                c.append(tmp)
    return c

#cl table {language:[countrycode]}
def cltable(countrylanguage):
    cl = {}
    tmplist = []
    for i in countrylanguage:
        tmplist.append(i['#Language'])

    for j in tmplist:
        sublist = []
        for i in countrylanguage:
            if j == i['#Language']:
                sublist.append(i['#CountryCode'])
                cl[j] = sublist
    return cl

#get dict{language:[population]}
def getlan_po(cl,c):
    newdict = {}
    for i in cl:
        tmp_ = []
        for j in c:
            if j['#Code'] in cl[i]:
                tmp_.append(j['Population'])
                newdict[i] = tmp_
    return newdict

def getSum(newdict):
    dic_ = {}
    for i in newdict:
        dic_[i] = sum(newdict[i])
    return dic_

def getTop(dic_):
    topList = sorted(dic_.items(),key = lambda item:item[1])[::-1]
    return topList

def getRes(topList):
    top10 = topList[:10]
    result = []
    for i in top10:
        result.append(i[0])
    return result

if __name__ == "__main__":
    start = datetime.datetime.now()
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    csvFile1 = open(file1, "r")
    csvFile2 = open(file2, "r")

    dict1 = readCSV(csvFile1)
    dict2 = readCSV(csvFile2)
    country = newlist(dict1)
    countrylanguage = newlist(dict2)
    c = ctable(country)
    cl = cltable(countrylanguage)
    newdict = getlan_po(cl, c)
    dic_ = getSum(newdict)
    topList = getTop(dic_)
    result = getRes(topList)

    print(result)
    end = datetime.datetime.now()
    print('running time:%s Seconds' %(end-start))
