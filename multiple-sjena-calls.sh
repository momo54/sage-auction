
single-update(){
  if ! [ $# = 3 ] ; then
    echo 'usage: '
    echo 'multiple-updates <file> <target-dataset> <line number>'
    echo '(http://localhost:8000/sparql/)'
    return 1
  fi

  count=$((0))

  exec 3<> $1
    while read -r LINE; do
      count=$(($count+1))
      if (($3 == $count)) ; then
        echo "$LINE"
        ../sage-jena-1.1/bin/sage-jena --update -q="$LINE" $2
        return 0
      fi
    done <&3
  exec 3>&-
}

multiple-updates(){

  if ! [ $# = 2 ] ; then
    echo 'usage: '
    echo 'multiple-updates <file> <target-dataset>'
    echo '(http://localhost:8000/sparql/)'
    return 1
  fi
  exec 3<> $1
    while read -r LINE; do
      ../sage-jena-1.1/bin/sage-jena --update -q="$LINE" $2
    done <&3
  exec 3>&-
}

multiple-runs(){

  if ! [ $# = 4 ] ; then
    echo 'usage: '
    echo 'multiple-runs <file> <index_of_query_start> <naive/reorder> <target-endpoint>'
    echo '(http://localhost:8000/sparql/)'
    return 1
  fi

  if (( $2 == 0 )) ; then
    rm -f "res/measure_$3.txt"
    rm -f "res/nres_$3.txt"
    touch "res/measure_$3.txt"
    touch "res/nres_$3.txt"
  fi
  count=$((0))

  exec 3<> $1
    while read -r LINE; do
      count=$(($count+1))
      echo "$count"
      if (($2 < $count)) ; then
        ../sage-jena-1.1/bin/sage-jena --measure="res/measure_$3.txt" --format='csv' -q="$LINE" "$4" > "res/$3/$count.txt"
        wc -l "res/$3/$count.txt" >> "res/nres_$3.txt"
        echo ';' >> "res/measure_$3.txt"
      fi
    done <&3
  exec 3>&-
}
