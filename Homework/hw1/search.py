import sys
import requests
import json
import re
import collections

#Enter file name and keyword in command line
#Load index from firebase

url = 'https://inf551-#####.firebaseio.com/index.json'
response = requests.get(url)
allDict = response.json()
keyword = sys.argv[1:]
print('Search keywords: ',keyword)

# Find keyword in allDict(index information)

keylist = []
for s in keyword:
    s = s.lower()
    for key in allDict.keys():
        if s == key:
            content=allDict[key]
            for i in content:
                result = {}
                val=i['TABLE']
                if val == 'city':
                    pk = 'ID'
                elif val == 'country':
                    pk = 'CODE'
                else: pk = 'LANGUAGE'
                pkval = i[pk]
                result[val] = pkval
                keylist.append(result)
#print(keylist)
                
# Combine values if dictionary items have same key

dict1 = {}
dict2 = {}
dict3 = {}
colist = []
temp_list1 = []
temp_list2 = []
temp_list3 = []
for i in keylist:
    if list(i.keys())[0] == 'city':
        temp_list1 = temp_list1 + list(i.values())[0]
    elif list(i.keys())[0] == 'country':
        temp_list2 = temp_list2 + list(i.values())[0]
    else:
        temp_list3 = []
        temp_list3 = temp_list3 + list(i.values())[0]

# Sorted by occurrence frequency

counts = collections.Counter(temp_list1)
list1 = sorted(temp_list1, key = lambda x: -counts[x])
counts = collections.Counter(temp_list2)
list2 = sorted(temp_list2, key = lambda x: -counts[x])
counts = collections.Counter(temp_list3)
list3 = sorted(temp_list3, key = lambda x: -counts[x])

#print(temp_list1)
dict1['city'] = list1
dict2['country'] = list2
dict3['countrylanguge'] = list3
colist.append(dict1)
colist.append(dict2)
colist.append(dict3)

# Remove empty table name

result=[]
for i in colist:
    if len(list(i.values())[0]) != 0:
        result.append(i)
print(result) #Show result

