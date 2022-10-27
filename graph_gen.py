import string, random, math, os, pickle
import networkx as nx
import matplotlib.pyplot as plt

class Vertex:
    def __init__(self, id, point, weight):
        self.id = id
        self.point = point
        self.weight = weight

    def __repr__(self):
        return f"[{self.id}{self.point} weight={self.weight}]"

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x},{self.y})"

def distance(p1, p2):
		return int(math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2))

# Function to build the graph
def build_graph(n, p): # n: number of vertexes; p: percentage of edges
    v = [] # list of vertexes [(id,x,y),(id,x,y)]
    letters = string.ascii_uppercase
    random.seed(98597)

    # generate n random non coincident points
    points = set()
    while len(points) != n:
        points.add(Point(random.randint(1,20), random.randint(1,20)))
    points = list(points)

    # generate n vertexes
    for i in range(n):
        v.append(Vertex(id=letters[i],point=points[i],weight=distance(points[i],Point(0,0))))

    # generate n connected edges
    p =  int(max((n*(n-1)/2)*p, n-1)) # calculate number of edges from percentage using the formula
    e = set()
    visited = []
    unvisited = list(letters[:n])
    while len(e) != p:
        if len(e) == 0: # if e is empty, pick 2 unvisited vertexes to form the first edge
            sample = random.sample(unvisited, 2)
            e.add(tuple(sorted(sample)))
            unvisited = list(set(unvisited) - set(sample))
            visited = list(set(visited).union(sample))
        elif len(unvisited) != 0: # if e is not empty and there are still unvisited nodes, pick 1 random unvisited and 1 random visited (to ensure the graph is connected)
            v1 = random.choice(unvisited)
            v2 = random.choice(visited)
            e.add(tuple(sorted([v1,v2])))
            unvisited.remove(v1)
        else: # all vertexes have atleast one edge, therefore pick random ones
            e.add(tuple(sorted(random.sample(letters[:n], 2))))

    return v,e
    
def plot_graph(e):
    G = nx.Graph()
    for edge in e:
        G.add_edge(edge[0],edge[1], weight=1)
    nx.draw(G, node_size=700 , with_labels=True)
    plt.show()

 
if __name__ == "__main__":
    path = "./graphs"
    if not os.path.exists(path): # make a new dir to save temporary blocks as well as final index
        os.makedirs(path)

    for n in range(2,27):
        for p in [0.125, 0.25, 0.5, 0.75]:
            v,e = build_graph(n, p)
            with open(f'{path}/v{n}_e{p}.pkl', 'wb') as f:
                pickle.dump([v,e], f)
    '''
    v,e = build_graph(26, 0.75)
    print(v)
    plot_graph(e)
    '''