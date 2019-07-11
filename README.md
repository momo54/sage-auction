

This is the source code for the delayed auction implementation experiments.

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

**Running**


**workload_relevant_check.py** takes *all.rq* in argument and detects the use of types of
Products to select relevant queries and writes them to **workload_uniq_rele**, i.e. workload_uniq_rele contains 220 queries formed with 3 and 13 joins.

There are two files that are references for the databases:
**sage.dump** and **sager.dump** that can be used to restore postgreSQL databases.
the files are equivalent.

**res/** is the folder that all experience results are written to.
since it will contain several gigabytes of data it is git-ignored.
