import numpy as np

f = open('dataset','w')

a = np.random.randn(10,4)

for row in range(0,len(a)):
	line = ''
	for col in range(0, len(a[0])):
		line+=str(a[row][col])+" "
	f.write(line+"\n")

f.close()