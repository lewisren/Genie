import sys
import time

inputfile = sys.argv[1]

start_time = time.time()
with open(inputfile, "r") as input, open("clean_"+inputfile, "w") as output:
	for line in input:
		value = line.split(",")
		if '\\' not in value[2] and '\\' not in value[9]:
			client = value[2].replace('"', '').strip()
			user = value[4].replace('"', '').strip()
			brand = value[7].replace('"', '').strip()
			category = value[8].replace('"', '').strip()
			product = value[9].replace('"', '').strip()
			
			if client and user and brand and category and product:
				out = client + "," + user + "," + brand + "," + category + "," + product + "\n"
				output.write(out)

input.close()
output.close()

print time.time() - start_time