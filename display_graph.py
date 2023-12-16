from src.NFA import NFA
import networkx as nx
import matplotlib.pyplot as plt

# v(0+1)*s
nfa0 = NFA('0')
nfa1 = NFA('1')
nfa0.add(nfa1)
nfa0.iterate()
nfav = NFA('v')
nfas = NFA('s')
nfav.concatenate(nfa0)
nfav.concatenate(nfas)


# print(nfav.data)
print(str(hash(nfav.start_state)), str(hash(nfav.finish_state)))
G = nx.Graph()
edges = dict()
for key in nfav.data:
    for letter in nfav.data[key]:
        for key1 in nfav.data[key][letter]:
            edges[(str(hash(key)), str(hash(key1)))] = letter
G.add_edges_from(list(edges.keys()))
pos = nx.circular_layout(G)
nx.draw(G, pos, with_labels=True)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edges)
plt.show()

