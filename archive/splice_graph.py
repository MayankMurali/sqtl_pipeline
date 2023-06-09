
class SpliceGraph:
    def __init__(self):
        self.vertices = {}
        self.edges = {}
    
    def add_edge(self, u, v):
        if u not in self.vertices:
            self.vertices[u] = {'cluster': ''}
            self.edges[u] = {}
        if v not in self.vertices:
            self.vertices[v] = {'cluster': ''}
            self.edges[v] = {}
        self.edges[u][v] = True
        self.edges[v][u] = True

    def add_junction(self, sqtl_data):
        phenotype_id = sqtl_data['phenotype_id']
        donor_vertex = f"{phenotype_id}_d"
        acceptor_vertex = f"{phenotype_id}_a"
        junction_vertex = f"{phenotype_id}"

        if donor_vertex not in self.vertices:
            self.vertices[donor_vertex] = {'cluster': ''}
            self.edges[donor_vertex] = {}
        if acceptor_vertex not in self.vertices:
            self.vertices[acceptor_vertex] = {'cluster': ''}
            self.edges[acceptor_vertex] = {}
        if junction_vertex not in self.vertices:
            self.vertices[junction_vertex] = {'cluster': ''}
            self.edges[junction_vertex] = {}

        self.add_edge(donor_vertex, junction_vertex)
        self.add_edge(junction_vertex, acceptor_vertex)

        if 'sqtl_data' not in self.edges[junction_vertex]:
            self.edges[junction_vertex]['sqtl_data'] = {}

        if phenotype_id not in self.edges[junction_vertex]['sqtl_data']:
            self.edges[junction_vertex]['sqtl_data'][phenotype_id] = []

        self.edges[junction_vertex]['sqtl_data'][phenotype_id].append(sqtl_data)

        
    def generate_splice_graph(self):
        nodes = []
        edges = []

        for v in self.vertices:
            node = {'id': v}
            if 'sqtl_data' in self.edges[v]:
                node['sqtl_data'] = self.edges[v]['sqtl_data']
            nodes.append(node)

        for u in self.edges:
            for v in self.edges[u]:
                if v > u:  # only add edges once
                    edge = {'source': u, 'target': v}
                    edges.append(edge)

        splice_graph = {'nodes': nodes, 'edges': edges}

        return splice_graph


    def view_splice_graph(splicegraph):
        G = nx.Graph()
        # add edges to networkx graph
        for v in splicegraph.vertices:
            for e in splicegraph.edges[v]:
                G.add_edge(v, e)

        # draw graph
        pos = nx.spring_layout(G)
        nx.draw(G, pos=pos, with_labels=True)
        plt.show()


