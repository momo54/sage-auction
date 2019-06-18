import random
import sys

if len(sys.argv) != 4 :
    print("usage: python sampler.py <source> <target> <amount_to_sample>")
    print(len(sys.argv))
    sys.exit()

products_file = open(sys.argv[1], 'r')
products= products_file.read()

selecteds_file = open(sys.argv[2], 'w')

for product in random.sample(products.splitlines(),k=int(sys.argv[3])) :
    
    selecteds_file.write(product+' '+bid)
    selecteds_file.write('\n')

products_file.close()
selecteds_file.close()
