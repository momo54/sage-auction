# use source bid-naive from bash terminal

# naive bid
# that writes a sponsor, bid and tag
naibid() {
  if ! [ $# = 3 ] ; then
    echo 'usage: '
    echo 'naibid <sponsor> <entity> <bid amount>'
    return 1
  fi

  sponsor=$1
  # s_sponsor="$(echo $sponsor | sed 's/<.*\///g;s/>.*//g;')"
  entity=$2
  s_entity="$(echo $entity | sed 's/<.*\///g;s/>.*//g;')"

  bid=$3


  index="auction:$RANDOM-$s_entity-$bid"

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
  if ! [ $# = 1 ] ; then
    echo 'usage: '
    echo 'nairet <file containing query>'
    return 1
  fi

  sed "
  /select ?/{
    s/select \(?[a-Z0-9]* \)/select (coalesce( ?altid, \1) as ?link) /;
    p;
    s/select (coalesce( ?altid, \(.*\)) as ?link).*/\1/
    h;
    d;
  };
  /SELECT \*/{
    p;
    s/\(?[a-Z0-9]* \).*/\1/;
    s/.*\(?[a-Z0-9]* \)/\1/;
    h;
    a };
  }
  /}/{
    g;
    s/\(?[a-Z0-9]*\)/  optional {\\n    \1 auction:bid ?bid;\\n      owl:sameAs ?altid\\n  }\\n} order by ?bid/;
    p;
    a damn;
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
