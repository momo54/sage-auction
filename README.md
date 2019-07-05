

This is the source code for the delayed auction implementation experiments.

All resources and their use will be quickly summarized.

this uses the watidv_queries from the sage experiments as source, but they
were read and compiled in the file **all.rq**.

running


**workload_relevant_check.py** takes *all.rq* in argument and detects the use of types of
Products to select relevant queries and writes them to **workload_uniq_rele

there are two files that are references for the databases:
**sage.dump** and **sager.dump** that can be used to restore postgreSQL databases.
the files are equivalent.

**res/** is the folder that all experience results are written to.
since it will contain several gigabytes of data it is git-ignored.
