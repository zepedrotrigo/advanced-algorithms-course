import pickle, operator
import matplotlib.pyplot as plt
from timeit import default_timer as timer
from itertools import combinations
from graph_gen import Vertex, Point, plot_graph

def min_weight_vertex_cover_exhaustive(n, p):
    basic_op = 0
    tested_configs = 0
    path = "./graphs"
    with open(f'{path}/v{n}_e{p}.pkl', 'rb') as f:
        vertexes, edges = pickle.load(f)

    solution = 2**32 # just a big number
    solution_comb = None
    for i in range(1, n+1):
        for comb in combinations(vertexes, i): # generate vertex combinations of size n
            tested_configs += 1
            ids = {v.id for v in comb}
            basic_op += len(comb) # in

            for e in edges: # iterate through edges
                check = any(id in ids for id in e) # check if at least one vertex from current comb is part of the edge
                basic_op += len(ids) + len(e) # in + in

                if check is False:
                    break
                basic_op += 1
            
            if check is not False:
                local_solution = sum([v.weight for v in comb])
                solution = min(solution, local_solution)
                basic_op += 1 + len(comb) * 2 + 2# if + in + sum + min
                
                if solution == local_solution:
                    solution_comb = comb
                basic_op += 1

    return solution, solution_comb, basic_op, tested_configs

def min_weight_vertex_cover_greedy_least_edges(n, p):
    '''
    A plausible heuristic for this problem is to consider the number of edges a given Vertex is connected to.
    Vertexes with a higher number of connected edges may be considered a better candidate for a possible solution by our algorithm.
    '''
    basic_op = 0

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
            basic_op += 4 # if + in + addition

    # sort from lowest to highest
    sorted_vertex = sorted(vertex_frequency.items(),key=lambda x:(x[1],x[0]),reverse = False)
    basic_op += len(sorted_vertex)
    
    candidates = set()
    ids = set()
    while True:
        v = sorted_vertex.pop()[0] # pop vertex with highest number of connected edges
        v = next((x for x in vertexes if x.id == v), None) # find it's object
        candidates.add(v) # add it to the list of candidate vertexes
        ids.add(v.id)
        basic_op += 3 + len(vertexes) # pop + add + add + next

        for e in edges: # iterate through edges
            check = any(id in ids for id in e) # check if at least one vertex from current comb is part of the edge
            basic_op += len(ids) + len(e) # in + in

            if check is False:
                break
            basic_op += 1 # if

        if check is not False:
            local_solution = sum([v.weight for v in candidates])
            basic_op += 1 + len(candidates) * 2 # if + for loop + additions
            return local_solution, candidates, basic_op, 1

def min_weight_vertex_cover_greedy_least_weight(n, p):
    '''
    A plausible heuristic for this problem is to consider the weights a Vertex.
    Vertexes with a lower weight may be considered a better candidate for a possible solution by our algorithm.
    '''

    path = "./graphs"
    with open(f'{path}/v{n}_e{p}.pkl', 'rb') as f:
        vertexes, edges = pickle.load(f)

    # sort from highest to lowest
    sorted_vertex = sorted(vertexes, key=operator.attrgetter('weight'), reverse=True)
    candidates = set()
    ids = set()
    while True:
        v = sorted_vertex.pop() # pop vertex with lowest weight
        candidates.add(v) # add it to the list of candidate vertexes
        ids.add(v.id)

        for e in edges: # iterate through edges
            check = any(id in ids for id in e) # check if at least one vertex from current comb is part of the edge

            if check is False:
                break

        if check is not False:
            local_solution = sum([v.weight for v in candidates])
            return local_solution, candidates

def plot_complexity(elements, times):
    plt.xlabel("Number of vertexes")
    plt.ylabel("Execution Time (s)")
    plt.yscale('log')
    plt.plot(elements,times)
    plt.show()

if __name__ == "__main__":
    for p in [0.125, 0.25, 0.5, 0.75]:
        times = []
        for n in range(2,27):
            start = timer()
            #weight, comb, basic_op, tested_configs = min_weight_vertex_cover_exhaustive(n, p)
            weight, comb, basic_op, tested_configs = min_weight_vertex_cover_greedy_least_edges(n, p)
            end = timer()
            times.append(end-start)
            print(f"{n} Vertexes; {p} Edges; Basic Operations: {basic_op}; Execution Time: {end-start}; Configurations Tested: {tested_configs}")
            print(f"{comb} <- Total Weight: {weight}")
        
        plot_complexity([i for i in range(2,27)],times)