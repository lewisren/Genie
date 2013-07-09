yolo-robot
==========

You-Only-Learn-Once Robot, so smart it only needs to learn once. 

Introduction
------------
Yolo-Robot is a Graph Learning Tool used to predict User interaction with Products. 
It uses [GraphLab](http://graphlab.org/) and [GraphChi](http://graphlab.org/graphchi/)'s powerful library to generate data predictions.


How-It-Works
------------
Is essentially broken up into 5 sections. 

### Formatting & Cleaning Data
Takes in a RAW data dump file and cleans up corrupted entries and reformats them into a more useful form. 
*Note: Reformatter will not include lines that contain illegal characters or are  missing data fields. 

Reformatter takes a data dump file consisting of the format:
'''python
[Date, Load_ID, Client, IP_UA, BVID, BVBrandID, Brand, Category, Product_ID, Content_Type]
'''
and turns it into:
'''python
[Client, BVID, Brand, Category, Product_ID]
'''

### Aggregation of Data
Aggregates the now-cleaned data file and tallies up unique User->Product combinations. This is done by concatenating the BVID with the Product_ID together and storing that into a dictionary as a unique key and keeping track of the key's occurrence in its value.

### "Graph-ifying" the Data
GraphLab&Chi require the input to be in MatrixMarket Format.
'''
%%MatrixMarket matrix coordinate real general
Row Col Number_Of_Edges
Starting_Node End_Node Weight
...
...
'''
This is done by extracting the User, Product, and Weight (Occurrence of the User:Prod combination) from the dictionary then generating an inverse mapped dictionary to map a Node_ID -> Users&Products. This is to maintain uniformity in identifying nodes within the graph and ensure each Node_ID is unique so that multiple edges are not created. 

### Label Propagation
The brains of the program. This will treat the weight of each edge as an "interest level" that a user has toward a product. For each user all interest levels for viewed products are normalized to form a probabilitic distribution spanning all seen products. Then using those probabilities, propagate to neighboring nodes and alter their distributions which will in turn cause a ripple-effect through the graph at each update. Eventually at some point the updates will converge and Label Propagation will end.

### Parsing & Ranking the Results
The output of Label Propagation returns an NxD matrix where N=# of Nodes and D=# of Products. Given this result we return to our inversely mapped dictionary to decipher what each Node_ID represents in terms of an actual Product_ID. Using heapsort to optimize for speed we maintain the k-largest elements (Or k highest probabilities) and output them as recommendations.


How-To-Run Yolo-Robot
---------------------
### Setup


### Reformatting Data
'''bash
$ cd /path/to/yolo-robot/graphchi/data
$ python reformatter.py [raw_dump_data_file]
'''

### Executing
'''bash
$ cd cd /path/to/yolo-robot/graphchi
$ python graphify.py [cleaned_data_file] 
'''