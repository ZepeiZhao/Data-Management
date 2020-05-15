from operator import add
import sys
from pyspark import SparkContext

def splitRepl(row):
    name = row.replace("'","").strip(' ').split(',')[1]
    # name = row.strip("'").strip(' ').split(',')[1]
    code = row.strip("'").strip(" ").split(',')[0]
    return code,name
def sr2(row):
    isofficial = row.strip("'").split(',')[2]
    countrycode = row.strip("'").split(',')[0]
    if 'F' in isofficial:
        return countrycode,isofficial

def judge(row):
    if row[1][0] is not None:
        return row


if __name__ == "__main__":
    sc = SparkContext()
    lines1 = sc.textFile("country.csv")
    lines2 = sc.textFile("countrylanguage.csv")

    l1 = lines1.map(splitRepl)
    l2 = lines2.map(sr2).filter(lambda row: row is not None)\
        .groupByKey().map(lambda x: (x[0],list(x[1]))).map(lambda row:(row[0],len(row[1])))\
        .filter(lambda row: row[1]>=10)

    result = l1.leftOuterJoin(l2).filter(lambda row:row[1][1] is not None).map(lambda row:row[1])\
        .map(lambda row:(row[1],row[0])).sortByKey(False).map(lambda row:(row[1],row[0])).map(lambda row:row[0]).collect()

    for row in result:
        print('%s' % row)
