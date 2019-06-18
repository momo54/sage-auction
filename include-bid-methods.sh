# use source bid-naive from bash terminal

naibid() {
  if ! [ $# = 3 ] ; then
    echo 'usage: '
    echo 'naibid <sponsor> <entity> <bid amount>'
    return 1
  fi

  python bid-methods.py naibid $1 $2 $3
}

naibid-chain() {
  if ! [ $# = 1 ] ; then
    echo 'usage: '
    echo 'naibid-chain <file>'
    return 1
  fi

  python bid-methods.py naibid_chain $1
}

nairet() {
  if ! [ $# = 2 ] ; then
    echo 'usage: '
    echo 'nairet <file containing queries> <file destination of translated queries>'
    return 1
  fi

  python bid-methods.py nairet $1 $2
}

# reorder bid
# writes an update to rename/reindex the bidded entity
reobid(){
  if ! [ $# = 3 ] ; then
    echo 'usage: '
    echo 'bid.sh <sponsor> <entity> <bid amount>'
    return 1inverse file order in folder
  fi

  python bid-methods.py reobid $1 $2 $3
}

reobid-chain() {
  if ! [ $# = 1 ] ; then
    echo 'usage: '
    echo 'reobid-chain <file>'
    return 1
  fi

  python bid-methods.py reobid-chain $1
}
