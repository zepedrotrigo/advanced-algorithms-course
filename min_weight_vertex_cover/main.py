import pickle
from itertools import combinations
from tqdm import tqdm
from graph_gen import Vertex, Point, plot_graph

def min_weight_vertex_cover(n, p):
    path = "./graphs"
    with open(f'{path}/v{n}_e{p}.pkl', 'rb') as f:
        vertexes, edges = pickle.load(f)

    solution = 2**32 # just a big number
    solution_comb = None
    for i in tqdm(range(1, n+1)):
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

    return solution, solution_comb, edges, vertexes

if __name__ == "__main__":
    p = 0.75
    for n in range(2,27):
        print(f"Number of Vertexes: {n}")
        comb, weight, edges, vertexes = min_weight_vertex_cover(n, p)
        #print(comb, weight)
        #print("\n\n",vertexes)
        #plot_graph(edges)