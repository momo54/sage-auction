from rdflib.plugins.sparql.parser import parseQuery
from rdflib.plugins.sparql.algebra import translateQuery
from rdflib.plugins.sparql.sparql import Bindings, QueryContext
from rdflib.plugins.sparql.parserutils import Expr
from rdflib.term import Identifier, Variable, URIRef
from rdflib.plugins.sparql.algebra import CompValue
from rdflib.util import from_n3
from rdflib.plugins.sparql.algebra import pprintAlgebra
import pprint

from rewrite_coalesce import CoalesceVisitor

# a visitor to get rid of projection with coalesce, orderby, but keep optional/
# The rewritten query should be executed with a local order_by operator.
# enough for the paper.

query_str='''SELECT (coalesce( ?altid, ?v1 ) as ?link) ?v5 ?v10 ?v4 ?v9 ?v8 ?v7 ?v6 ?v2 ?v0 WHERE {
 ?v1 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://db.uwaterloo.ca/~galuc/wsdbm/ProductCategory8> .  
 ?v0 <http://purl.org/goodrelations/includes> ?v1 .  
 ?v1 <http://ogp.me/ns#tag> ?v2 .  
 ?v1 <http://schema.org/contentRating> ?v6 .  
 ?v1 <http://schema.org/description> ?v7 .  
 ?v1 <http://schema.org/keywords> ?v8 .  
 ?v1 <http://schema.org/text> ?v9 .  
 ?v1 <http://db.uwaterloo.ca/~galuc/wsdbm/hasGenre> ?v4 .
 ?v10 <http://db.uwaterloo.ca/~galuc/wsdbm/likes> ?v1 .  
 ?v4 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?v5 .  
 optional { 
   ?v1  <http://auction.example.org/bid> ?bid; 
   <http://www.w3.org/2002/07/owl#sameAs> ?altid } } 
   order by ?bid'''


class  CoalesceVisitor_rename_bid(CoalesceVisitor):
    bid_variable=None
    def visit_BGP(self, node):
        # print("Visiting BGP:", node)
        triples = "".join(
                    triple[0].n3() + " " + triple[1].n3() + " " + triple[2].n3() + " . "
                    for triple in node.triples
                )
        self.my_query.append(triples) 

    def visit_OPTIONAL(self, node):
        for triple in node.triples:
            if triple[2]==Variable('bid'):
                self.bid_variable=triple[0]

    def visit_LeftJoin(self, node):
        # print("Visiting LeftJoin:", node)
        self.visit(node.p1)
        self.visit_OPTIONAL(node.p2)

def rewrite_coalesce_rename_bid(query_str):
    parsed_query = parseQuery(query_str)
    algebra = translateQuery(parsed_query)
    #print(pprintAlgebra(algebra))

    visitor = CoalesceVisitor_rename_bid()
    visitor.visit(algebra.algebra)
    result="".join(visitor.my_query)
    result="#bid_variable("+str(visitor.bid_variable)+")\n"+result
#    print(f"bid_variable: {visitor.bid_variable}")
    return result

#print(rewrite_coalesce_rename_bid(query_str))
