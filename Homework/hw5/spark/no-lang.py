from operator import add
import sys
from pyspark import SparkContext


def splitRepl(row):
    name = row.strip("'").split(',')[1]
    code = row.strip("'").split(',')[0]
    return code,name
def sr2(row):
    language = row.strip("'").split(',')[1]
    countrycode = row.strip("'").split(',')[0]
    return countrycode,language

def select(row):
    if None in row[1]:
        return row[1][0]

if __name__ == "__main__":
    sc = SparkContext()
    lines1 = sc.textFile("country.csv")
    lines2 = sc.textFile("countrylanguage.csv")

    l1 = lines1.map(splitRepl)
    l2 = lines2.map(sr2).groupByKey().map(lambda x: (x[0],list(x[1])))
    result = l1.leftOuterJoin(l2).map(select).filter(lambda row: row is not None).collect()

    for row in result:
        print('%s' % row.strip(" ").strip("'"))
