class Graph(object):
    def __innit__(self, v=1000):
        self.v = v
        # creating graph of v verticals
        self.graph = [[] for i in range(v)]

    def add_edge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)