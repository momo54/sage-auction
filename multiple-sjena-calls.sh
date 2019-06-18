
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

  if (( $2 == 0 )) ; then
    rm -f 'measure_naive.txt'
    rm -f 'nres_naive.txt'
    touch 'measure_naive.txt'
    touch 'nres_naive.txt'
  fi
  count=$((0))

  exec 3<> $1
    while read -r LINE; do
      count=$(($count+1))
      echo "$count"
      if (($2 < $count)) ; then
        timeout 300 ../sage-jena-1.1/bin/sage-jena --measure='measure_naive.txt' --format='csv' -q="$LINE" http://localhost:8000/sparql/watdiv10m > "res/naive/$count.txt"
        wc -l "res/naive/$count.txt" >> 'nres_naive.txt'
        echo ';' >> measure_naive.txt
      fi
    done <&3
  exec 3>&-
}
