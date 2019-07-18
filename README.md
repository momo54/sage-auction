

This is the source code for the delayed auction implementation experiments.

**Virtual environnement**
Please use a python virtual environment for executing the python code provided.
please note it was exclusively tested under python3, and that it is therefore
recommended to use python3, rather than python2.

All resources and their use will be quickly summarized.

**Experimental setup**

We use the WatDiv  SPARQL benchmark for both data and queries. The
dataset contains 10^7 triples. Among all products (of which there are 25000), 5%
are randomly sampled and assigned a random bid amount between 1 and 100.
We start with a workload of 12400 queries, of which there are SPARQL
conjunctive queries with STAR, PATH and SNOWFLAKE shapes. Removing
duplicate queries from the workload reduces it to around 4000 queries. Queries are stored in 
**all.rq**

We use PostgreSQL as backend with B+ trees and 3 indexes SPO, POS and
OSP.

**Data**
the original data is the watdiv10M.ttl file from [WatDiv](https://dsg.uwaterloo.ca/watdiv/#download)
There are two files that are references for the databases:
**sage.dump** and **sager.dump** that can be used to restore postgreSQL databases.
the files are equivalent. (too big?)

**Bid treatment pipeline**
**products_all.dmp**
this file is an exhaustive list of all the products in the database. it was obtained by running
```sql
select distinct(subject) from watdiv10m where predicate like '%type%' and object like '%ProductCategory%;
```

**products_sampled_bidded.dmp**
this file is a list of sampled products each separated from their bid amount by a single space.
obtained by running
```bash
python product_sampler_bidder.py products_all.dmp products_sampled_bidded.dmp 1250
```
you have to specify the amount you want to sample.
this list can then be declined into two sets of update queries, one for the rewriting approach,
and one for the reordering approach.

**update_queries_naive.sparql**
this file contains lines of update queries for the rewriting approach.
run
```
python bid-methods.py naibid_chain products_sampled_biddedd.dmp > update_queries_naive.sparql
```

**update_queries_reorder.sparql**
this file contains lines of update queries for the reordering approach.
run
```
python bid-methods.py reobid_chain products_sampled_biddedd.dmp > update_queries_reorder.sparql
```

**Query treatment pipeline**
**all.rq**
*all.rq* is a file containing all watdiv queries used in the sage experiments.
it was produced with the command
```bash
cat queries/*/* > all.rq
```
where *queries* was a folder containing 300 folders of queries. each folder had a different workload.
Queries are obtain through refinement of *all.rq*
**workload_uniq_full.sparql**
this file contains all the same queries of *all.rq* but it removes all duplicate lines.
it is obtained by running
```bash
uniq -c all.rq > workload_uniq_full.sparql
```
**workload_uniq_relevant_full.sparql**
this file contains all relevant queries in the workload. that is, all queries that relate to Products of 
the database. it is obtained by running
```bash
python workload_relevant_check.py workload_uniq_full.sparql
```
when looking at the *workload_relevant_check.py* file, on line 9 is
the regex used to identify any object of the relation`:type :ProductCategory`
which is the criterion for identifying Products.

queries from *workload_uniq_relevant_full.sparql* can be executed as they are,
but there are to rewriting variants
**workload_uniq_relevant_full_naive.sparql**
is rewriting queries with `coalesce`, `optional` and `order by`, for use in the
"naive/rewriting" approach.
it is obtained by running
```bash
python bid-methods.py nairet workload_uniq_relevant_full.sparql workload_uniq_relevant_full_naive.sparql
```
*note: nairet stands for naive-retrieve*

**workload_uniq_relevant_full_limit.sparql**
this is mostly the same as *relevant_full_naive* but is a simpler rewriting that appends `limit 1`
at the end of every line.
```bash
python bid-methods.py tffret workload_uniq_relevant_full.sparql workload_uniq_relevant_full_limit.sparql
```
*note: tffret stands for time-for-first-(results)-retrieve*


**res/** is the folder that all experience results are written to.
since it will contain several gigabytes of data it is git-ignored.

**MISC**

**banhammer_res_unord.sh**
to determine queries that will not return results, there is currently no other method than
executing all of them once and manually removing concerned queries after observing results.
banhammer is a small sed script that deletes the lines to be removed from the *workload_uniq_relevant_full.sparql* file.
the current version is specific to this query generation, so it should be edited to reflect the need of other random watdiv queries generation.

**include_bid_methods**
this is a utility files that used to wire *bid-methods.py* into the terminal.
since then *bid_methods.py* changed, making *include_bid_methods* not up to date.

**lastres.zip**
this is an archive of older *res/* folder, containing results from previous execution. the last one was used for the presentation.

**multiple-sjena-calls.sh**
this is a script that must be sourced (`source multiple-sjena-calls.sh`) and then has two uses:
for executing all updates on a sage-jena database interface
example usage:
```
multiple-updates update_queries_naive.sparql http:///localhost:8000/sparql/watdiv10m
```
and for executing all of the queries from the *workload* files onto a sage-jena interface.
example usage:
```
multiple-runs workload_uniq_relevant_full_naive.sparql 0 naive http:///localhost:8000/sparql/watdiv10m
```
multiple runs takes the line at which you want to start execution (in case of crashes for example)
meaning you can start at arbitrary query #102
it also takes a "kind" (here it is "naive")
kind is usually either naive, reorder or tff. in practice it changes the name of the result folders and files associated
with this run of the query execution.

NOTE: your sage-client cli will very likely be in a different location than `../sage-jena-1.1/bin/sage-jena` 
so editing *multiple-sjena-calls.sh* to reflect this is advised.
