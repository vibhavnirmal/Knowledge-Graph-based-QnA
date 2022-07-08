import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

from kwQnA._getentitypair import GetEntity


class GraphEnt:
    """docstring for graphEnt."""

    def __init__(self):
        super(GraphEnt, self).__init__()
        self.x = GetEntity()

    def createGraph(self, dataEntities):
        entity_list = dataEntities.values.tolist()
        source, relations, target = [],[],[]

        for i in entity_list:
            # if i[0] == "" or i[1] == "" or i[3] == "":
            #     pass
            # else:
            source.append(i[0])
            relations.append(i[1])
            # aux_relations = i[2]
            target.append(i[3])
            # time = i[4]
            # place = i[5]


        kg_df = pd.DataFrame({'source':source, 'target':target, 'edge':relations})
        G=nx.from_pandas_edgelist(kg_df, "source", "target", edge_attr=True, create_using=nx.MultiDiGraph())

        plt.figure(figsize=(12,12))
        pos = nx.spring_layout(G, k = 2) # k regulates the distance between nodes
        nx.draw(G, with_labels=True, node_color='skyblue', node_size=1500, edge_cmap=plt.cm.Blues, pos = pos)
        # nx.draw_networkx_edge_labels(G,pos,edge_labels=labels,font_size=30)

        plt.show()

if __name__ == '__main__':
    test = GraphEnt()
    print("Can't Test directly")
