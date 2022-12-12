import pickle, random, time
import matplotlib.pyplot as plt
from math import factorial
from timeit import default_timer as timer
from graph_gen import Vertex, Point, plot_graph

def is_valid_vertex_cover(edges, vertex_cover):
    for (u, v) in edges:
        if u not in vertex_cover and v not in vertex_cover:
            return False

    return True

def min_weight_vertex_cover_randomized(n, p):
    path = "./graphs"
    with open(f'{path}/v{n}_e{p}.pkl', 'rb') as f:
        vertexes, edges = pickle.load(f)

    basic_op = tested_configs = already_tested_sample_counter = 0
    total_samples_tested = 1
    samples = set()
    min_vertex_cover = None
    min_weight = float('inf')
    weights = {v.id : v.weight for v in vertexes}
    basic_op += len(vertexes) # for

    while already_tested_sample_counter / total_samples_tested < 0.5:
        total_samples_tested += 1
        vertex_cover = set()
        vertex_cover.add(str(random.choice(vertexes))) # Randomly select a vertex and add it to the vertex cover
        basic_op += 3 # add to set + random.choice + convert to str

        edges_copy = list(edges)

        while len(edges_copy):
            random_index = random.randint(0, len(edges_copy)-1)
            (u,v) = edges_copy.pop(random_index)

            if u not in vertex_cover and v not in vertex_cover:
                if random.random() < 0.5: # Randomly select one of the vertices and add it to the vertex cover
                    vertex_cover.add(u)
                else:
                    vertex_cover.add(v)

                basic_op += 2 + 1 + 1 # ifs + gen random.random() + add to set

        # Ensure that the sample was not tested already
        if vertex_cover in samples:
            already_tested_sample_counter += 1
            continue # already tested, therefore skip to next iteration
        
        tested_configs += 1
        samples.add(frozenset(vertex_cover))

        # Check if the vertex cover is valid and has minimum weight
        local_solution_weight = sum(weights[v] for v in vertex_cover)
        basic_op += len(vertex_cover) + 1 # for + sum

        if is_valid_vertex_cover(edges, vertex_cover) and local_solution_weight < min_weight:
            min_vertex_cover = vertex_cover
            min_weight = local_solution_weight
            basic_op += 1 + len(edges) # if + for inside is_valid function

    return min_weight, min_vertex_cover, basic_op, tested_configs


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
            weight, comb, basic_op, tested_configs = min_weight_vertex_cover_randomized(n, p)
            end = timer()
            times.append(end-start)
            print(f"{n} Vertexes; {p} Edges; Basic Operations: {basic_op}; Execution Time: {end-start}; Configurations Tested: {tested_configs}")
            print(f"{comb} <- Total Weight: {weight}")
        
        #plot_complexity([i for i in range(2,27)],times)