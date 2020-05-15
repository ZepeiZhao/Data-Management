from operator import add
import sys
from pyspark import SparkContext


def splitRepl(row):
    continent = row.replace("'","").split(',')[2]
    le = row.replace("'","").replace(' ','').split(',')[7]
    gnp = row.replace("'","").replace(" ","").split(',')[8]
    # if le is ' ':

    if float(gnp)>10000:
        return continent,le



if __name__ == "__main__":
    sc = SparkContext()
    lines1 = sc.textFile("country.csv")

    l1 = lines1.map(splitRepl).filter(lambda row: row is not None) \
        .filter(lambda row: row[1] is not u'').map(lambda row: (row[0], float(row[1]))) \
        .aggregateByKey((0, 0), lambda u, v: (u[0] + v, u[1] + 1), lambda u, v: (u[0] + v[0], u[1] + v[1])) \
        .filter(lambda row: (row[1][1] >= 5)).map(lambda row: (row[0], float(row[1][0] / row[1][1]))).map(lambda row:(row[0].strip(' '),row[1]))

    # print l1.collect()
    for row in l1.collect():
        print('%s, %s' % (row[0], row[1]))
