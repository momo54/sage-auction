import os

# take a file containing many queries and create a query file for each query in a directory
def install_queries(filename,dir='queries'):
    # Create directory hierarchy if it doesn't exist
    os.makedirs(dir, exist_ok=True)
    with open(filename, 'r') as file:
        i = 0
        for line in file:
            target = f"{dir}/q{i}.sparql"
            with open(target, 'w') as temp_file:
                temp_file.write(line)
            print(f"wrote: {target} with {line}")  # Juste pour afficher chaque ligne à titre d'exemple
            i += 1

filename = '/Users/molli-p/sage-auction/update_queries_naive.sparql'
install_queries(filename,"queries/update/watdiv_bid")

filename = '/Users/molli-p/sage-auction/update_queries_reorder.sparql'
install_queries(filename,"queries/update/watdiv_renamed")

filename = '/Users/molli-p/sage-auction/workload_uniq_relevant_full.sparql'
install_queries(filename,"queries/read/watdiv_renamed")

filename = '/Users/molli-p/sage-auction/workload_uniq_relevant_full_naive.sparql'
install_queries(filename,"queries/read/watdiv_bid")
