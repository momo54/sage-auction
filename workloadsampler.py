import random
import re
import sys

workload_file = open(sys.argv[1], 'r')

sampled_workload = open('sampled_workload.sparql', 'w')

finder=re.compile(r'.*<http://www\.w3\.org/1999/02/22-rdf-syntax-ns#type> <http://db\.uwaterloo\.ca/~galuc/wsdbm/ProductCategory.*', re.S)

for query in workload_file :
    if(finder.match(query)):
        sampled_workload.write(query)

workload_file.close()
sampled_workload.close()
