import subprocess
from click.testing import CliRunner
from sage.cli.debug import sage_query_debug
import asyncio



def execute_query(line):
     runner=CliRunner()

     loop = asyncio.new_event_loop()
     asyncio.set_event_loop(loop)

     async def run_invoke():
          return await loop.run_in_executor(
               None,
               runner.invoke,
               sage_query_debug,
               ['config.yaml','http://example.org/watdiv','-q', line])
     
     result = loop.run_until_complete(run_invoke())
#     assert result.exit_code == 0
     loop.close()


def execute_query_now(line,graph_uri='http://example.org/watdiv'):
     runner=CliRunner()
     result = runner.invoke(sage_query_debug,['config.yaml',graph_uri,'-q',line])
     print(result)
#     assert result.exit_code == 0


def update_rewrite(filename,graph_uri='http://example.org/watdiv'):
    with open(filename, 'r') as file:
        for line in file:
            # Écrire "line" dans un fichier temporaire
            #with open('temp_file.txt', 'w') as temp_file:
            #    temp_file.write(line)
            
            print(line)  # Juste pour afficher chaque ligne à titre d'exemple

            #execute_query(line)
            execute_query_now(line,graph_uri)

            # Appeler la commande pour chaque ligne ici
            # Remplacez cette ligne par la commande réelle que vous souhaitez exécuter    


def run_queries(filename,graph_uri='http://example.org/watdiv'):
    with open(filename, 'r') as file:
        for line in file:
            # Écrire "line" dans un fichier temporaire
            #with open('temp_file.txt', 'w') as temp_file:
            #    temp_file.write(line)
            
            print(line)  # Juste pour afficher chaque ligne à titre d'exemple

            #execute_query(line)
            execute_query_now(line,graph_uri)

            # Appeler la commande pour chaque ligne ici
            # Remplacez cette ligne par la commande réelle que vous souhaitez exécuter    


#filename = '/Users/molli-p/sage-auction/update_queries_naive.sparql'
#update_rewrite(filename,'http://example.org/watdiv')

#filename = '/Users/molli-p/sage-auction/update_queries_reorder.sparql'
#update_rewrite(filename,'http://example.org/watdiv_renamed')

filename = '/Users/molli-p/sage-auction/workload_uniq_relevant_full.sparql'
run_queries(filename,'http://example.org/watdiv_renamed')

