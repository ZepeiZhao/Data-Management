from lxml import etree
import collections
import sys
import json

# python3 search.py fsimage.xml index.xml core site
file1 = sys.argv[1]
file2 = sys.argv[2]
tree1 = etree.parse(open(file1))
tree2 = etree.parse(open(file2))

# Build name&id dict
res = {}
keywords = sys.argv[3:]
for element in tree2.xpath('/index/postings'):
    list1 = []
    for i in element.xpath('./inumber'):
        list1.append(i.text)
        for j in element.xpath('./name'):
            res[j.text] = list1

# Clear unrelated words in keywords          
for i in keywords:
    if i.lower() not in res.keys():
        print('Cannot find:', i , ', I will remove wrong name or please rerun and input the right file name')
        keywords.remove(i)

# Find keywords' inumber
def combineInum(keywords):
    inumlist = []
    if len(keywords) == 1:
        for i in keywords:
            for each in res[i]:
                inumlist.append(each)
        return inumlist
    else:
        for i in keywords:
            inumlist.append(res[i])
        inumlist = list(set(inumlist[0]).intersection(*inumlist[1:]))
        if len(inumlist) == 0:
            print('Cannot find this file')
        else:
            return inumlist
inumlist = combineInum(keywords)

# Construct inode info
temp_res = []
tmp_dic = {}
for element in tree1.xpath('/fsimage/INodeSection/inode'):
    temp = {}
    #print(element.text)
    for j in element.xpath('./id'):
        temp['id']=j.text
    for z in element.xpath('./name'):
        tmp_dic[j.text] = z.text
    for i in element.xpath('.//type'):
        temp['type'] = i.text
    for k in element.xpath('.//mtime'):
        temp['mtime'] = k.text
    for m in element.xpath('./blocks/block/id'):
        temp['blocks'] = m.text.split()
    temp_res.append(temp)    
tmp_dic['16385'] = ''
#print(temp_res)

# Build Child-parent dict
cp1={}
for i in tree1.xpath('/fsimage/INodeDirectorySection/directory'):
    for child in i.xpath('.//child'):
        for parent in i.xpath('.//parent'):
            cp1[child.text]=parent.text
            
# Build path
path_dict = {}
for i in inumlist:
    path_list=[]
    s = i
    path_list.append(i)
    while (s in cp1): 
        path_list.append(cp1[s])
        s = cp1[s]
    path_dict[i] = path_list[::-1]

dict2 = {}
for key,val in path_dict.items():
    tmp_list = []
    for i in path_dict[key]:
        for k in tmp_dic.keys():
            if i == k:
                tmp_list.append(tmp_dic[k])
                dict2[key] = tmp_list
#print(dict2)

endlist = []
for key,value in dict2.items():
    dict3 = {}
    path = ''
    for i in value:
        path = path + i + '/'
        dict3[key] = path
    endlist.append(dict3)

# Print path
def printf(endlist):
    for i in endlist:
        for key,val in i.items():
            print(val)
            for j in temp_res:
                if j['id']==key:
                    print(json.dumps(j))
printf(endlist)
