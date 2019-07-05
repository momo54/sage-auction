import sys
import re
import random

def naibid(sponsor, entity, bid_amount):
    bid_amount=str(bid_amount)

    expr=re.compile('<.*/', re.S)
    s_entity=expr.sub('', entity)
    expr=re.compile('>.*', re.S)
    s_entity=expr.sub('', s_entity)
    expr=re.compile('.*:', re.S)
    s_entity=expr.sub('', s_entity)

    index="auction:"+str(random.randint(1,1000))+"-"+s_entity+"-"+bid_amount

    print("prefix wsdbm: <http://db.uwaterloo.ca/~galuc/wsdbm/> prefix auction: <http://auction.example.org/> prefix owl: <http://www.w3.org/2002/07/owl#> prefix xsd: <http://www.w3.org/2001/XMLSchema#> insert data { %s auction:bid '%s'^^xsd:integer ; auction:sponsor %s ; owl:sameAs %s. }"%(entity, bid_amount, sponsor, index))

def reobid(sponsor, entity, bid_amount):
    str_bid=str(bid_amount)
    int_bid=int(bid_amount)

    expr=re.compile('<.*/', re.S)
    s_entity=expr.sub('', entity)
    expr=re.compile('>.*', re.S)
    s_entity=expr.sub('', s_entity)
    expr=re.compile('.*:', re.S)
    s_entity=expr.sub('', s_entity)

    index="auction:"+str(1000-int_bid)+"-"+s_entity+"-"+str_bid

    print("prefix wsdbm: <http://db.uwaterloo.ca/~galuc/wsdbm/> prefix auction: <http://auction.example.org/> prefix owl: <http://www.w3.org/2002/07/owl#> prefix xsd: <http://www.w3.org/2001/XMLSchema#> delete { %s ?p1 ?o1 . ?s2 ?p2 %s } insert { %s auction:bid '%s'^^xsd:integer ; auction:sponsor %s ; ?p1 ?o1 ; owl:sameAs %s . ?s2 ?p2 %s. } where { %s ?p1 ?o1 . optional { ?s2 ?p2 %s } }"%(entity, entity, index, bid_amount, sponsor, entity, index, entity, entity))

def bid_chain(file, kind):
    function_choice={
        'naibid' : naibid,
        'reobid' : reobid
    }
    sponsor='wsdbm:User0'

    entity_file = open(file, 'r')
    find_lr=re.compile(r'\n')
    find_space=re.compile(' ')

    for line in entity_file :
        line_nolr=find_lr.sub('', line)
        entity_bid=find_space.split(line_nolr)
        function_choice[kind](sponsor, entity_bid[0], entity_bid[1])

def nairet(file, dest):
    queries_file = open(file, 'r')
    content = queries_file.read()
    queries = content.split('SELECT * ')
    queries.pop(0)

    sampled_workload_naived = open(dest, 'w')

    find_variables = re.compile(r'\?[A-z0-9]* ', re.S)
    find_product=re.compile(r'\?[A-z0-9]* <http://www\.w3\.org/1999/02/22-rdf-syntax-ns#type> <http://db\.uwaterloo\.ca/~galuc/wsdbm/ProductCategory', re.S)

    for qy in queries :
        query = qy
        variables = find_variables.findall(query)
        variables=list(dict.fromkeys(variables))

        product = find_product.findall(query)
        product = product.pop(0)
        product = product.split(' ')[0]+' '

        variables.remove(product)
        for variable in variables :
            query = variable+query
        query = f'SELECT (coalesce( ?altid, {product}) as ?link) '+query
        query = query.split('}')[0] + 'optional { %s <http://auction.example.org/bid> ?bid; <http://www.w3.org/2002/07/owl#sameAs> ?altid } } order by ?bid'%(product)
        sampled_workload_naived.write(query)
        sampled_workload_naived.write('\n')

def tffret(file, dest):
    queries_file = open(file, 'r')
    content = queries_file.read()

    dest_file = open(dest, 'w')

    for qy in content.splitlines() :
        query= qy+" limit 1"
        dest_file.write(query)
        dest_file.write('\n')

def rollback_chain(file):
    sponsor='wsdbm:User0'

    entity_file = open(file, 'r')
    find_lr=re.compile(r'\n')
    find_space=re.compile(' ')

    for line in entity_file :
        line_nolr=find_lr.sub('', line)
        entity_bid=find_space.split(line_nolr)

        bid_amount=entity_bid[1]
        str_bid=str(bid_amount)
        int_bid=int(bid_amount)

        entity=entity_bid[0]

        expr=re.compile('<.*/', re.S)
        s_entity=expr.sub('', entity)
        expr=re.compile('>.*', re.S)
        s_entity=expr.sub('', s_entity)
        expr=re.compile('.*:', re.S)
        s_entity=expr.sub('', s_entity)

        index="auction:"+str(1000-int_bid)+"-"+s_entity+"-"+str_bid
        print("prefix wsdbm: <http://db.uwaterloo.ca/~galuc/wsdbm/> prefix auction: <http://auction.example.org/> prefix owl: <http://www.w3.org/2002/07/owl#> prefix xsd: <http://www.w3.org/2001/XMLSchema#> delete { %s auction:bid '%s'^^xsd:integer ; auction:sponsor %s ; ?p1 ?o1 ; owl:sameAs %s . ?s2 ?p2 %s } insert { %s ?p1 ?o1 . ?s2 ?p2 %s } where { %s ?p1 ?o1 . ?s2 ?p2 %s }"%(index, bid_amount, sponsor, entity, index, entity, entity, index, index))

if (sys.argv[1] == 'naibid'):
    naibid(sys.argv[2], sys.argv[3], sys.argv[4])

if (sys.argv[1] == 'reobid'):
    reobid(sys.argv[2], sys.argv[3], sys.argv[4])

if (sys.argv[1] == 'bid_chain'):
    bid_chain(sys.argv[2],sys.argv[3])

if (sys.argv[1] == 'naibid_chain'):
    bid_chain(sys.argv[2], 'naibid')

if (sys.argv[1] == 'reobid_chain'):
    bid_chain(sys.argv[2], 'reobid')

if (sys.argv[1] == 'nairet'):
    nairet(sys.argv[2],sys.argv[3])

if (sys.argv[1] == 'tffret'):
    tffret(sys.argv[2],sys.argv[3])

if (sys.argv[1] == 'rollback_chain'):
    rollback_chain(sys.argv[2])
