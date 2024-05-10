from rdflib.plugins.sparql.parser import parseQuery
from rdflib.plugins.sparql.algebra import translateQuery
from rdflib.plugins.sparql.sparql import Bindings, QueryContext
from rdflib.plugins.sparql.parserutils import Expr
from rdflib.term import Identifier, Variable, URIRef
from rdflib.plugins.sparql.algebra import CompValue
from rdflib.util import from_n3
from rdflib.plugins.sparql.algebra import pprintAlgebra
import pprint

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

class CoalesceVisitor:

    my_query = []

    def visit(self, algebra):
        # Determine the type of the node and visit it
        method_name = 'visit_' + type(algebra).__name__
        if hasattr(algebra, 'name'):
            method_name = 'visit_' + algebra.name
        #print(f"try visiting method_name: {method_name}")
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(algebra)

    def generic_visit(self, algebra):
        # Handle generic visiting logic
        #print(f"Visiting {type(algebra).__name__}")
#        print(f"Visiting {algebra.name}")

        if isinstance(algebra, CompValue):
            #print(f"comp value: {algebra.items()}")
            for key, value in algebra.items():
                if isinstance(value, list):
                    for item in value:
                        self.visit(item)
                elif isinstance(value, CompValue):
                    self.visit(value)
        elif isinstance(algebra, list):
            print(f"list: {algebra}")
            for item in algebra:
                self.visit(item)

    def visit_Project(self, project):
        #print("Visiting Project:", project)
        self.my_query.append("select * WHERE {")
        self.visit(project.p)
        self.my_query.append("}")

    def visit_OrderBy(self, order_by):
        # print("Visiting OrderBy:", order_by)
        self.visit(order_by.p)

    def visit_Extend(self, node):
        # print("Visiting Extend:", node)
        self.visit(node.p)

    def visit_LeftJoin(self, node):
        # print("Visiting LeftJoin:", node)
        self.visit(node.p1)
        self.my_query.append("  OPTIONAL {")   
        self.visit(node.p2)
        self.my_query.append(" }")       

    # Example specific visit method
    def visit_BGP(self, node):
        # print("Visiting BGP:", node)
        triples = "".join(
                    triple[0].n3() + " " + triple[1].n3() + " " + triple[2].n3() + " . "
                    for triple in node.triples
                )
        self.my_query.append(triples) 

    # Add more methods for other specific types of nodes

class  CoalesceVisitor_rename(CoalesceVisitor):
    def visit_LeftJoin(self, node):
        # print("Visiting LeftJoin:", node)
        self.visit(node.p1)
# no need of optional with rename strategy.
#        self.my_query.append("  OPTIONAL {")   
#        self.visit(node.p2)
#        self.my_query.append(" }")

def rewrite_coalesce(query_str):
    parsed_query = parseQuery(query_str)
    algebra = translateQuery(parsed_query)
    # print(pprintAlgebra(algebra))

    visitor = CoalesceVisitor()
    visitor.visit(algebra.algebra)
    result="".join(visitor.my_query)
    return result

def rewrite_coalesce_rename(query_str):
    parsed_query = parseQuery(query_str)
    algebra = translateQuery(parsed_query)
    # print(pprintAlgebra(algebra))

    visitor = CoalesceVisitor_rename()
    visitor.visit(algebra.algebra)
    result="".join(visitor.my_query)
    return result

#print(rewrite_coalesce_rename(query_str))
