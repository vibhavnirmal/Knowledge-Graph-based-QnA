import networkx as nx
import matplotlib.pyplot as plt
from getentitypair import GetEntity
from exportPairs import exportToJSON
import pandas as pd


exp = exportToJSON()
x = GetEntity()
p = x.get_entity(str('finalDataFiles.txt'))

h = p[0].values.tolist()
# print(h)

relations = [i[1] for i in h]
# print(relations)

source = [i[0] for i in h]
# print(source)
#
# # extract object
target = [i[2] for i in h]


kg_df = pd.DataFrame({'source':source, 'target':target, 'edge':relations})
G=nx.from_pandas_edgelist(kg_df, "source", "target",
                          edge_attr=True, create_using=nx.MultiDiGraph())

plt.figure(figsize=(12,12))
pos = nx.spring_layout(G, k = 0.5) # k regulates the distance between nodes
ff =nx.draw(G, with_labels=True, node_color='skyblue', node_size=1500, edge_cmap=plt.cm.Blues, pos = pos)

# edge_labels = nx.get_edge_attributes(ff,'relations')
# nx.draw_networkx_edge_labels(ff,pos, labels = edge_labels)
plt.show()

allData = p[0]

exp.dumpdata(allData)
