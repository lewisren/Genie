Genie
==========

Graph Learning via Label Propagation & Data Visualization  
* [Introduction](https://github.com/lewisren/Genie/blob/master/README.md#introduction)  
* [How-It-Works](https://github.com/lewisren/Genie/blob/master/README.md#how-it-works)  
* [How-To-Run Genie](https://github.com/lewisren/Genie/blob/master/README.md#how-to-run-genie)  

Introduction
------------
Genie is a product recommendation tool based on user clustering. The idea is that you want to give every user the possibility of a product within the network as a recommendation; however, be able to rank them in such a way that is most relevant to the specific user. By clustering users based on [modularity](http://en.wikipedia.org/wiki/Modularity_(networks\)) we can determine how big of an impact a specific user will have on the rest of the network. For example, a high modularity node that makes a decision will have a stronger impact on its neighbors, but will propagate out slower and have a small to negligible effect on outer nodes. Similarly, a low modularity node that makes a decision will have a lesser impact, but will radiate outwards much more quickly.  

<a href="http://www.youtube.com/watch?feature=player_embedded&v=PzCtioqsJ_k" target="_blank">
<img src="http://img.youtube.com/vi/PzCtioqsJ_k/0.jpg" alt="Genie" width="240" height="180" border="0" />
</a>  
*It uses [GraphLab](http://graphlab.org/)/[GraphChi](http://graphlab.org/graphchi/)'s powerful distributed graph computing power to generate data predictions and [Gephi](https://gephi.org/) to render the data.*

How-It-Works
------------
Genie is essentially broken up into 5 big components.

### Formatting & Cleaning Data
Takes in a RAW data dump file and cleans up corrupted entries and reformats them into a more useful form.     
*Note: Reformatter will not include lines that contain illegal characters or are  missing data fields.*

Reformatter takes a data dump file consisting of the format:
```python
[Date, Load_ID, Client, IP_UA, BVID, BVBrandID, Brand, Category, Product_ID, Content_Type]
```
and turns it into:
```python
[Client, BVID, Brand, Category, Product_ID]
```

### Aggregation of Data
Aggregates the now cleaned data file and tallies up unique User->Product combinations. This is done by concatenating the UserID with the ProductID together and storing that into a dictionary as a unique key and keeping track of the key's occurrence in its value.

### "Graph-ifying" the Data
GraphLab&Chi require the input to be in MatrixMarket Format.
```
%%MatrixMarket matrix coordinate real general
Row Col Number_Of_Edges
Starting_Node End_Node Weight
...
...
```
This is done by extracting the User, Product, and Weight (Occurrence of the User:Prod combination) from the dictionary and generating an inversely mapped dictionary to map a NodeID to a User or Product node. This is to maintain uniformity in identifying nodes within the graph and ensure each NodeID is unique so that multiple edges are not created. 

### Label Propagation
The brains of the program. This will treat the weight of each edge as an "interest level" that a user has toward a product. For each user all interest levels for viewed products are normalized to form a probabilitic distribution spanning all seen products. Then using those probabilities, propagate to neighboring nodes and alter their distributions which will in turn cause a ripple-effect through the graph at each update. Eventually at some point the updates will converge and Label Propagation will end.

### Parsing & Ranking the Results
The output of Label Propagation returns an NxD matrix where N=# of Nodes and D=# of Products. Given this result we return to our inversely mapped dictionary to decipher what each NodeID represents in terms of an actual ProductID. Using heapsort to optimize for speed we maintain the k-largest elements (k highest probabilities) and output them as recommendations.


How-To-Run Genie
---------------------
### Setup
```bash
$ cd /path/to/genie/graphchi
$ ./install.sh
$ cd toolkits/graph_analytics
$ make
```

### Cleaning & Reformatting Data
```bash
$ cd /path/to/genie/graphchi
$ python reformatter.py [raw_dump_data_file]
```

### Executing
```bash
$ python graphify.py [cleaned_data_file] 
```
