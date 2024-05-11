import yaml
import glob
import sys
import os
import csv


def list_files(path):
    if not os.path.isdir(path):
        return glob.glob(path)
    files = list()
    for filename in os.listdir(path):
        if filename.endswith(".sparql"):
            files.append(f"{path}/{filename}")
    return files


def load_queries(path):
    queries = list()
    for file in list_files(path):
        with open(file, 'r') as reader:
            filename = os.path.basename(file).split('.')[0]
            query = reader.read()
            queries.append((filename, query))
    return queries

def run_files(wcs):
    files = []
    output = "output" if "output" not in config else config["output"]
    for filename, query in load_queries(config["queries"]):
        for approach in config["approaches"]:
            for run in config["runs"]:
                files.append((
                    f"{output}/{approach}/"
                    f"{run}/{filename}.csv"))
    print(f"run_files: ({wcs}) ({output}) / {files}")
    return files


rule run_all:
    input: ancient(run_files)

rule run_query:
    input:
        query = ancient(
            "queries/read/watdiv_bid/{query}.sparql"),
        config = ancient(
            expand("{configfile}.yaml", configfile=config["name"]))
    output:
        metrics = "{output}/{approach}/{run,[0-9]}/{query}.csv",
        solutions = "{output}/{approach}/{run,[0-9]}/{query}.json"
    params:
        endpoint = "http://localhost:8000/sparql",
        approach = lambda wildcards: wildcards.approach
    shell:
        "python scripts/cli.py auction-run {input.query} {params.endpoint}  \
            --approach {params.approach} \
            --stats {output.metrics} \
            --output {output.solutions} "

rule check_python:
    shell:
        "which python; python -V"

rule collect_all:
    input: 
        data=ancient(run_files)
    output: 
        final="{output}/final.csv"
    run:
        print("Collecting data")
        with open(output[0], 'w') as outfile:
            for path in input.data:
                path_parts = path.split(os.sep)
                approach = path_parts[1]  
                run = path_parts[2]  
                query = os.path.splitext(path_parts[-1])[0]  # 'q73' without extension
                with open(path, newline='') as csvfile:
                    # Create a DictReader
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        outfile.write(f"{query},{approach},{run},{row['elapsed_time']},{row['solutions']} \n")    

