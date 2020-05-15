import sys
from lxml import etree
from collections import defaultdict

# python3 invert.py fsimage.xml index.xml
file1 = sys.argv[1]
file2 = sys.argv[2]

#open the fsimage file 
tree = etree.parse(file1)

#get name to a list
list1=[]
for name in tree.xpath('//name'):
    list1.append(name.text)
list1[0] = ''

#remove '.xml'
list_1 = []
for each in list1:
    each = each.split('.')[0]
    list_1.append(each)
    
#split '-' in name
list3 = []
for each in list_1:
    each = each.split('-')
    list3.append(each)

#build unique nameset
list4 = []
for i in list3:
    for j in i:
        list4.append(j)
nameSet = list(set(list4))

#get 'id' 
list2 = []
for id in tree.xpath('//inode/id'):
    list2.append(id.text)

#combine name and id
z = list(zip(list2,list3))
newlist = []
for i in range(len(nameSet)):
    for j in z:
        dic2 = {}
        if nameSet[i] in j[1]:
            dic2[nameSet[i]] = j[0]
            newlist.append(dic2)

#build name&id dictionary
newdict = {}
for _ in newlist:
    for k, v in _.items():
        newdict.setdefault(k, []).append(v)
#print(newdict)

#write dict to xml
root = etree.Element('index')
for key,value in newdict.items():
    head = etree.SubElement(root,'postings')
    body1 = etree.SubElement(head,'name')
    body1.text = key
    for each in value:
        body2 = etree.SubElement(head,'inumber')
        body2.text = each
index = etree.ElementTree(root)
index.write(file2, pretty_print = True, xml_declaration = True, encoding = 'utf-8')
print('Success')
