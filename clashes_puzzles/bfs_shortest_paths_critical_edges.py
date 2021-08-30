import operator

# n: the total number of nodes in the level, including the gateways
# l: the number of links
# e: the number of exit gateways
n, l, e = [int(i) for i in input().split()]
graph = {}

for i in range(l):
    # n1: N1 and N2 defines a link between these nodes
    n1, n2 = [int(j) for j in input().split()]
    graph.setdefault(n1, []).append(n2)
    graph.setdefault(n2, []).append(n1)

gateway_nodes = [int(input()) for i in range(e)]
adjacent_gateways = {
    vertex: len([adj for adj in adjs if adj in gateway_nodes])
    for vertex, adjs in graph.items()
    if vertex not in gateway_nodes
}

# game loop
while True:
    si = int(input())  # The index of the node on which the Skynet agent is positioned this turn
    
    bfs_q = [(si, [si])]
    visited = [si]

    vertex_distance = {}
    valid_edge_for_vertex = {}
    critical_vertex = None

    while(bfs_q and critical_vertex is None):
        vertex, history = bfs_q.pop(0)
        visited.append(vertex)
        for adj in graph[vertex]:
            if adj in gateway_nodes:
                distance = len(history)
                vertex_distance.setdefault(vertex, distance)
                valid_edge_for_vertex.setdefault(vertex, (vertex, adj))
                
                # The number of removals that has to be made in this shortest path
                priority = sum((adjacent_gateways[v] for v in history))

                # if the number of removals required is equal to the number of steps in the path
                #this is a critical path.
                if priority == distance:
                    critical_vertex = vertex
                    break

            if adj not in visited and adj not in gateway_nodes:
                node_history = history.copy()
                node_history.append(adj)
                bfs_q.append((adj, node_history))

    if critical_vertex is None:
        #no edges are critical, just remove one from the shortest path
        critical_vertex = min(vertex_distance.items(), key=operator.itemgetter(1))[0]

    max_edge = valid_edge_for_vertex[critical_vertex]
    graph[max_edge[0]].remove(max_edge[1])
    graph[max_edge[1]].remove(max_edge[0])

    adjacent_gateways = {
        vertex: len([adj for adj in adjs if adj in gateway_nodes])
        for vertex, adjs in graph.items()
        if vertex not in gateway_nodes
    }

    print(f"{max_edge[0]} {max_edge[1]}")


