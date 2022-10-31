import pickle, os
from itertools import combinations
from graph_gen import Vertex, Point, plot_graph

def min_weight_vertex_cover_exhaustive(n, p):
    path = "./graphs"
    with open(f'{path}/v{n}_e{p}.pkl', 'rb') as f:
        vertexes, edges = pickle.load(f)

    solution = 2**32 # just a big number
    solution_comb = None
    for i in range(1, n+1):
        for comb in combinations(vertexes, i): # generate vertex combinations of size n
            ids = {v.id for v in comb}

            for e in edges: # iterate through edges
                check = any(id in ids for id in e) # check if at least one vertex from current comb is part of the edge

                if check is False:
                    break
            
            if check is not False:
                local_solution = sum({v.weight for v in comb})
                solution = min(solution, local_solution)
                
                if solution == local_solution:
                    solution_comb = comb

    return solution, solution_comb

def min_weight_vertex_cover_greedy(n, p):
    '''
    A plausible heuristic for this problem is to consider the number of edges a given Vertex is connected to.
    Vertexes with a higher number of connected edges may be considered a better candidate for a possible solution by our algorithm.
    '''

    path = "./graphs"
    with open(f'{path}/v{n}_e{p}.pkl', 'rb') as f:
        vertexes, edges = pickle.load(f)

    # count the number of edges connected to each vertex.
    vertex_frequency = {}
    for tup in edges:
        for el in tup:
            if el in vertex_frequency:
                vertex_frequency[el] += 1
            else:
                vertex_frequency[el] = 1

    # sort from lowest to highest
    sorted_vertex = sorted(vertex_frequency.items(),key=lambda x:x[1],reverse = False)
    
    candidates = set()
    ids = set()
    while True:
        v = sorted_vertex.pop()[0] # pop vertex with highest number of connected edges
        v = next((x for x in vertexes if x.id == v), None) # find it's object
        candidates.add(v) # add it to the list of candidate vertexes
        ids.add(v.id)

        for e in edges: # iterate through edges
            check = any(id in ids for id in e) # check if at least one vertex from current comb is part of the edge

            if check is False:
                break

        if check is not False:
            local_solution = sum({v.weight for v in candidates})
            return local_solution, candidates

if __name__ == "__main__":
    for p in [0.125, 0.25, 0.5, 0.75]:
        for n in range(2,27):
            print(f"{n} Vertexes; {p} Edges:")
            #weight, comb = min_weight_vertex_cover_exhaustive(n, p)
            weight, comb = min_weight_vertex_cover_greedy(n, p)
            print(f"{comb} <- Total Weight: {weight}")
            #plot_graph(edges)
