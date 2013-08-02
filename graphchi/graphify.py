import os
import sys
import time
import heapq
import pprint

inputfile = sys.argv[1]
user_interest = {}
usr_store = {}
prod_store = {}
inv_prod_store = {}
inv_store = {}
start_time = time.time()

# Aggregate 
with open(inputfile, "r") as input, open(inputfile+"_nodes.csv", "w") as nodes:
	index = 0
	num_products = 0
	nodes.write("Id;Label\n")
	for line in input:
		value = line.split(",")
		if '\\' not in value[1] and '\\' not in value[4]:
			usr = value[1].strip()
			prod = value[4].strip()
			out = usr + ":" + prod
			if user_interest.get(out):
				user_interest[out] = user_interest.get(out) + 1
			else:
				if not usr_store.get(usr):
					usr_store[usr] = index
					inv_store[index] = ("user", usr)
					index = index + 1
					nodes.write(usr+";"+usr+"\n")
				if not prod_store.get(prod):
					prod_store[prod] = index
					inv_prod_store[num_products] = prod
					inv_store[index] = ("product", prod)
					index += 1
					num_products += 1
					nodes.write(prod.replace(' ','-')+";"+prod.replace(' ','-')+"\n")
				user_interest[out] = 1

nodes.close()
input.close()
print "Done aggregating..... " + str(len(user_interest)) + " Unique Edges..... Time Elapsed: " + str(time.time() - start_time)

# Write to files
size = str(len(usr_store)+len(prod_store))
output = open(inputfile+"_temp", "wb")
edges = open(inputfile+"_edges.csv", "w")
output.write("%%MatrixMarket matrix coordinate real general\n")
output.write(size + " " + size + " " + size + "\n")
edges.write("Source;Target;Weight\n")

for key, value in user_interest.iteritems():
	nodes = key.split(":")
	user = nodes[0]
	product = nodes[1]
	if usr_store.get(user) and prod_store.get(product):
		output.write(str(usr_store[user]) + " " + str(prod_store[product]) + " " + str(value) + "\n")
		edges.write(user + ";" + product.replace(' ','-') + ";" + str(value) +"\n")
edges.close()
output.close()

D = str(len(prod_store))
seed = open(inputfile+"_temp.seeds", "w")
seed.write("%%MatrixMarket matrix coordinate real general\n")
seed.write(str(len(usr_store)+len(prod_store)) + " " + D + " " + "0\n")
seed.close()

print "Done formatting..... D=" + D + "..... Time Elapsed: " + str(time.time() - start_time)
# For Gephi OpenOrd, use Random Seed: 4180811794490061113 

# Begin Label Propagation
# TODO: Fix security issue
os.system("./toolkits/graph_analytics/label_propagation --training="+inputfile+"_temp --D="+D)
print "Done propagating..... Time Elapsed: " + str(time.time() - start_time)

# Begin Parsing and Top-5 
with open(inputfile+"_temp_U.mm", "r") as result, open(inputfile+"_edges_recommendation", "w") as recommendation_edges, open("final_result", "w") as final_result:
	counter = 0
	prod_num = 0
	top_items = {}
	l = []
	recommendation_edges.write("Source;Target\n")

	for x in xrange(3):
		result.next()
	for eachline in result:
		line = float(eachline.rstrip())
		if inv_store.get(counter)[0] == "user":
			if prod_num < len(prod_store):
				l.append(line)
				prod_num += 1
			else:
				top_five = heapq.nlargest(5, enumerate(l), key=lambda x: x[1])
				final_result.write(inv_store.get(counter)[1] + " : ")
				for pref in top_five:
					final_result.write(inv_prod_store[pref[0]] + " , ")
					recommendation_edges.write(inv_store.get(counter)[1] + ";" + inv_prod_store[pref[0]].replace(' ','-') + "\n")
				final_result.write("\n")
				counter += 1
				if inv_store.get(counter)[0] == "user":
					l = [line]
				prod_num = 1
		else:
			if prod_num >= len(prod_store):
				counter += 1
				if inv_store.get(prod_num)[0] == "product":
					l = [line]
					prod_num = 0
			prod_num += 1
result.close()
final_result.close()
recommendation_edges.close()

print "DONE! Time Elapsed: " + str(time.time() - start_time)
print



