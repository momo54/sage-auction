# use source bid-naive from bash terminal

# naive bid
# that writes a sponsor, bid and tag
naibid() {
  if ! [ $# = 3 ] ; then
    echo 'usage: '
    echo 'bid.sh <sponsor> <entity> <bid amount>'
    return 1
  fi

  entity=$2
  bid=$3
  sponsor=$1

  index="auction:1111"

  echo "
  prefix wsdbm: <http://db.uwaterloo.ca/~galuc/wsdbm/>
  prefix auction: <http://www.example.auction.org/>
  prefix owl: <http://www.w3.org/2002/07/owl#>
  prefix xsd: <http://www.w3.org/2001/XMLSchema#>

  insert data {
  $entity auction:bid '$bid'^^xsd:integer ;
    auction:sponsor $sponsor ;
    owl:sameAs $index.
  }
  "
}

# naive retrieve
# rewrites a query to account for bids
nairet() {
  sed "
  /select /{
    s/select \(?[a-Z]* \)/select (coalesce( ?altid, \1) as ?link) /;
    p;
    s/select (coalesce( ?altid, \(.*\)) as ?link).*/\1/
    h;
    d;
  };
  /}/{
    g;
    s/\(?[a-Z]* \)/  optional {\\n    \1 auction:bid ?bid;\\n      owl:sameAs ?altid\\n  }\\n} order by ?bid/;
  };
  " $1
}

# reorder bid
# writes an update to rename/reindex the bidded entity
reobid(){
  if ! [ $# = 3 ] ; then
    echo 'usage: '
    echo 'bid.sh <sponsor> <entity> <bid amount>'
    return 1inverse file order in folder
  fi

  entity=$2
  bid=$3
  sponsor=$1

  index="auction:1111"

  echo "
  prefix wsdbm: <http://db.uwaterloo.ca/~galuc/wsdbm/>
  prefix auction: <http://www.example.auction.org/>
  prefix owl: <http://www.w3.org/2002/07/owl#>
  prefix xsd: <http://www.w3.org/2001/XMLSchema#>

  delete {
      $entity ?p1 ?o1 .
      ?s2 ?p2 $entity .
  }

  insert {
    $index auction:bid '$bid'^^xsd:integer ;
      auction:sponsor $sponsor ;
      ?p1 ?o1 ;
      owl:sameAs $entity .
    ?s2 ?p2 $index .
  }

  where {
    $entity ?p1 ?o1 .
    ?s2 ?p2 $entity .
  }
  "
}
