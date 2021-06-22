from grafo_pronto import grafo
import matplotlib.pyplot as plt
import networkx as nx
class visual:
    G = nx.Graph()
    node_pos = None
    node_color = None
    edge_color = None
    edge_label = None
    node_label = None
    solution_nodes = None
    def arruma(self,x,y):
        return (min(x,y),max(x,y))
    def edges(self,Gra,solution_edges):
        mapa={}
        for e in range(len(solution_edges)):
            mapa[self.arruma(Gra.arestas[e].idx_i,Gra.arestas[e].idx_j)] = solution_edges[e]
        for e in range(len(Gra.arestas)):
            self.G.add_edge(Gra.arestas[e].idx_i,Gra.arestas[e].idx_j)
        print(len(self.G.edges))
        self.edge_color = ['red' for e in range(len(self.G.edges))]
        c = 0
        self.edge_label ={}
        for e in self.G.edges:
            if mapa[e] == 0:
                self.edge_color[c] = 'white'
            else:
                self.edge_label[e] = str(mapa[e]) + '|' + '480'
            c+=1
        c = 0

    def nodes(self,Gra,solution_nodes):
        self.node_label = {}
        for i in range(len(Gra.nos)):
            self.G.add_node(i)
        for i in range(len(self.G.nodes)):
            self.node_label[i] = Gra.nos[i].nome
        for i in range(len(Gra.nos)):
            self.G.nodes[i]['pos'] = (Gra.nos[i].cx,Gra.nos[i].cy)
        self.node_color = ['red' if i in solution_nodes else 'white' for i in self.G.nodes]
        self.node_pos = nx.get_node_attributes(self.G,'pos')
        print(self.G.nodes)

    def plot(self):
        '''
        nx.draw_networkx(self.G,self.node_pos,with_labels=False,node_color=self.node_color,node_size=300)
        nx.draw_networkx_edges(self.G,self.node_pos,edge_color=self.edge_color)
        nx.draw_networkx_labels(self.G, self.node_pos, self.node_label)
        :return:
        '''
        nx.draw_networkx(self.G, self.node_pos, with_labels=False, node_color=self.node_color, node_size=300)
        nx.draw_networkx_edges(self.G, self.node_pos, edge_color=self.edge_color)
        nx.draw_networkx_labels(self.G, self.node_pos, self.node_label)
        nx.draw_networkx_edge_labels(self.G,self.node_pos,edge_labels=self.edge_label)
        plt.show()

    def generate_solution_nodes(self,solution_edges,Gra):
        self.solution_nodes = []
        for e in range(len(solution_edges)):
            if solution_edges[e] == 0:
                continue
            n1 = Gra.arestas[e].idx_i
            n2 = Gra.arestas[e].idx_j
            if not n1 in self.solution_nodes:
                self.solution_nodes.append(n1)
            if not n2 in self.solution_nodes:
                self.solution_nodes.append(n2)

    def __init__(self,Gra,solution_edges):
        self.generate_solution_nodes(solution_edges,Gra)
        self.nodes(Gra,self.solution_nodes)
        self.edges(Gra,solution_edges)
        self.plot()

