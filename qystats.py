import re

query_file= open('workload_uniq_relevant_full.sparql', 'r')

target_file= open('goalcount.dmp', 'w')

find_dot=re.compile(' . ')

for query in query_file :
    n_goals=find_dot.split(query)
    number=len(n_goals)-1
    target_file.write(str(number))
    target_file.write('\n')
