from operator import add
import sys
from pyspark import SparkContext

def splitRepl(row):
    name = row.replace("'","").replace(" ","").split(',')[1]
    continent = row.replace("'","").replace(" ","").split(',')[2]
    population = row.replace("'","").replace(" ","").split(',')[6]
    if continent == inputword:
        return float(population),name

if __name__ == "__main__":
    inputword = "Asia"
    sc = SparkContext()
    lines = sc.textFile("country.csv")

    result = lines.map(splitRepl)\
            .filter(lambda row: row is not None)\
            .sortByKey(False).map(lambda row: (row[1],row[0])).take(10)
    for row in result:
        print('%s, %s' % (row[0], row[1]))
