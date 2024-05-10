import click
import json
import yaml
import csv
import os
import re
import glob
import logging
import hashlib
import urllib.parse
import time
import requests
import rdflib
import rewrite_coalesce
import rewrite_coalesce2


from pandas import DataFrame
from typing import Tuple, List

from spy import Spy
from approaches.factory import ApproachFactory


###############################################################################
# ### Helping functions
###############################################################################


def list_files(path: str) -> List[str]:
    if not os.path.isdir(path):
        return glob.glob(path)
    files = list()
    for filename in os.listdir(path):
        if filename.endswith(".sparql"):
            files.append(f"{path}/{filename}")
    return files


def load_queries(path: str) -> List[Tuple[str, str]]:
    queries = list()
    for file in list_files(path):
        with open(file, "r") as reader:
            filename = os.path.basename(file).split(".")[0]
            query = reader.read()
            queries.append((filename, query))
    return queries


def save_dataframe(dataframe: DataFrame, output: str, mode: str = "w") -> None:
    if output is not None:
        directory = os.path.dirname(output)
        if not os.path.exists(directory):
            os.makedirs(directory)
        header = not (mode == "a" and os.path.exists(output))
        dataframe.to_csv(output, mode=mode, index=False, header=header)


def save_json(data: dict, output: str) -> None:
    if output is not None:
        directory = os.path.dirname(output)
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(output, "w") as outfile:
            json.dump(data, outfile, indent=4)



def execute_query(query: str, endpoint: str, graph_uri: str):    
    logging.info(f"query sent to the server:\n{query}")

    headers = {
        "accept": "text/html",
        "content-type": "application/json"}
    payload = {
        "query": query,
        "next": None,
        "defaultGraph": graph_uri}

    has_next = True

# no -> no resume for web preemption 
#    while has_next:
    data = json.dumps(payload)
    response = requests.post(
        endpoint, headers=headers, data=data).json()
    
#        print(f"response: {response}")

    payload["next"] = response["next"]
    has_next = response["next"] is not None

    solutions=[]
    for solution in response["bindings"]:
        solutions.append(solution)



    return solutions



###############################################################################
# ### Command-line interface
###############################################################################


@click.group()
def cli():
    pass


@cli.command()
@click.argument(
    "queryfile", type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.argument(
    "endpoint", type=click.STRING)
@click.option(
    "--approach", type=click.Choice(['bid', 'rename','rename-force','rename-force-top20','rename-force-500ms']), required=True)
@click.option(
    "--quota", type=click.INT, default=None)
@click.option(
    "--force-order/--default-ordering", default=False)
@click.option(
    "--output", type=click.Path(exists=False), default=None)
@click.option(
    "--stats", type=click.Path(exists=False), default=None)
@click.option(
    "--verbose/--quiet", default=False)
def auction_run(
    queryfile, endpoint, approach,  quota, force_order,  output, stats, verbose
):
    if verbose:
        logging.basicConfig(
            level="INFO",
            format="%(asctime)s - %(message)s",
            datefmt="%m/%d/%Y %I:%M:%S")
        
    filename, query = load_queries(queryfile)[0]

    #COALESCE Queries -> order by done locally, 
    # coalesce removed to *
    # to be executed on watdiv with explicit bids.
    if query.lower().find("order") == -1:
        print(f"query does not contain order by, skipping...")
        return

    if approach == "bid":
        query = rewrite_coalesce.rewrite_coalesce(query)
        graph_uri = "http://example.org/watdiv"
    elif approach == "rename":
        query = rewrite_coalesce.rewrite_coalesce_rename(query)
        graph_uri = "http://example.org/watdiv_renamed"
    elif approach == "rename-force":
        print("rename-force")
        query = rewrite_coalesce2.rewrite_coalesce_rename_bid(query)
        graph_uri = "http://example.org/watdiv_renamed"
    elif approach == "rename-force-top20":
        #carefull, server shoud  be configured to return the top20
        print("rename-force-top20")
        query = rewrite_coalesce2.rewrite_coalesce_rename_bid(query)
        graph_uri = "http://example.org/watdiv_renamed"
    elif approach == "rename-force-500ms":
        #carefull, server shoud  be configured to return the top20 and max 500ms
        print("rename-force-500ms")
        query = rewrite_coalesce2.rewrite_coalesce_rename_bid(query)
        graph_uri = "http://example.org/watdiv_renamed"


    start = time.time()
    elapsed_time = 0

    logging.info(f"executing query: {query}")

    solutions = execute_query(
        query, endpoint, graph_uri)


    if approach=="bid":
        datatype_uri = rdflib.URIRef("http://www.w3.org/2001/XMLSchema#integer")
        pattern = r'\"(\d+)\"\^\^<http://www.w3.org/2001/XMLSchema#integer>'

        def get_bid(solution):
            bid= solution.get('?bid')
            if bid is None:
                return 0
            else:
                match = re.match(pattern,bid)
                if match is None:
                    print(f"?? ({bid})")
                    return 0
                else:
                    return int(match.group(1))

        sorted_solutions = sorted(solutions, key=get_bid, reverse=True)
    else:
        sorted_solutions = solutions

    elapsed_time = (time.time() - start) * 1000

    data={'elapsed_time': elapsed_time, 'solutions': len(sorted_solutions)}

    for i in range(min(10, len(sorted_solutions))):
        logging.info(f"{i}: {sorted_solutions[i]}")


    logging.info((
        f" query executed in {elapsed_time / 1000} seconds "
        f"with {len(sorted_solutions)} solutions"))
    if len(sorted_solutions) > 0:
        first_solution = json.dumps(sorted_solutions[0], indent=4)
        last_solution = json.dumps(sorted_solutions[-1], indent=4)
        logging.info(f"first solution:\n{first_solution}")
        logging.info(f"last solution:\n{last_solution}")

    save_json(sorted_solutions[:20], output)
    save_dataframe(DataFrame(data,index=[0]), stats)


@cli.command()
@click.argument(
    "reference", type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.argument(
    "actual", type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option(
    "--output", type=click.Path(exists=False), default=None)
@click.option(
    "--verbose/--quiet", default=False)
def compare(reference, actual, output, verbose):
    if verbose:
        logging.basicConfig(
            level="INFO",
            format="%(asctime)s - %(message)s",
            datefmt="%m/%d/%Y %I:%M:%S")
    reference = json.load(open(reference, "r"))
    actual = json.load(open(actual, "r"))

    correct = True
    memory = {}
    for mappings in reference:
        sorted_mappings = {k: mappings[k] for k in sorted(mappings.keys())}
        key = hashlib.md5(str(sorted_mappings).encode("utf-8")).digest()
        if key not in memory:
            memory[key] = 0
        memory[key] += 1
    for mappings in actual:
        sorted_mappings = {k: mappings[k] for k in sorted(mappings.keys())}
        key = hashlib.md5(str(sorted_mappings).encode("utf-8")).digest()
        if key not in memory:
            logging.info(f"Incorrect solution: {sorted_mappings}")
            correct = False
            break
        memory[key] -= 1
        if memory[key] < 0:
            logging.info(f"Duplicated solution: {sorted_mappings}")
            correct = False
            break
    correct = all([value == 0 for value in memory.values()])

    if correct:
        logging.info("The TOP-K is correct")
    else:
        logging.info("The TOP-K is incorrect")
    save_dataframe(DataFrame([[correct]], columns=["correct"]), output)


@cli.command()
@click.argument(
    "queries", type=click.Path(exists=True, dir_okay=False, file_okay=True))
@click.argument(
    "output", type=click.Path(exists=True, dir_okay=True, file_okay=False))
@click.option(
    "--configfile",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    default="config/xp-watdiv.yaml")
def extract_queries(queries, output, configfile):
    config = yaml.safe_load(stream=open(configfile, "r"))
    engine = ApproachFactory.create("sage", config)

    nb_query = len(load_queries(output)) + 1

    expected = ["SELECT", "ORDER BY", "LIMIT"]
    rejected = [
        "OPTIONAL", "GROUP BY", "BIND", "DISTINCT", "RAND", "STRAFTER",
        "*", "|"]

    regex_service = re.compile(
        "((.*?\n)*?.*?)(SERVICE.*?ontology#label.*?{(.*?\n)*?.*?})")
    orderby_variables = re.compile("(ASC|DESC)\( (\?var[0-9])Label \)")

    with open(queries, 'r') as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')
        header = None
        for index, row in enumerate(rows):
            if header is None:
                header = row
                continue
            query = urllib.parse.unquote_plus(row[0])
            if not all([operator in query for operator in expected]):
                continue
            if any([operator in query for operator in rejected]):
                continue
            query = re.sub(regex_service, "\\1", query)
            query = re.sub(orderby_variables, "\\1( \\2 )", query)
            print(f"Wikidata Query:\n{query}")
            answer = input("Compute number of solutions (y/n): ")
            if answer != "y":
                continue
            solutions = engine.execute_query(query, Spy(), limit=1000000)
            print(f"Number of solutions: {len(solutions)}")
            answer = input("Keep this query (y/n): ")
            if answer == "y":
                with open(f"{output}/Q{nb_query}.sparql", "w") as queryfile:
                    queryfile.write(query)
                print(f"Number of queries: {nb_query}")
                nb_query += 1


if __name__ == "__main__":
    cli()
