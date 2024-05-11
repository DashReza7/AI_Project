import heapq


class min_heap:
    def __init__(self):
        self._queue = []
        self._index = 0
    
    def push(self, item, priority):
        heapq.heappush(self._queue, (priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]
        
    
    def size(self):
        return len(self._queue)


def restore_path(start_node, end_node, pred):
    path = []
    cur = end_node
    while True:
        path.append(cur)
        if cur == start_node:
            break
        cur = pred[cur]
    path.reverse()
    return path
    

# TODO: You should implement this from scratch and you cannot use any library (such as networkx) for finding the shortest path.
# Let's implement Dijkstra's salgorithm
def find_shortest_path(start_node, end_node, graph):
    """
    Find the shortest path between two nodes in a graph.
    :param start_node: The start node
    :param end_node: The end node
    :param graph: The graph
    :return: The shortest path. It is a list of node_ids from start_node to end_node.
    Note that you use all of the data in "pasdaran_streets" dataset appropriately such as "street_length" and "one_way".
    """
    # if start_node and end_node are tuples
    if isinstance(start_node, tuple):
        lat_1, lon_1 = start_node
        lat_2, lon_2 = end_node
        row = graph[((graph['u_lat'] == lat_1) & (graph['u_lon'] == lon_1))]
        if len(row) > 0:
            start_node = row['u'].values[0]
        else:
            row = graph[((graph['v_lat'] == lat_1) & (graph['v_lon'] == lon_1))]
            start_node = row['v'].values[0]
        
        row = graph[((graph['u_lat'] == lat_2) & (graph['u_lon'] == lon_2))]
        if len(row) > 0:
            end_node = row['u'].values[0]
        else:
            row = graph[((graph['v_lat'] == lat_2) & (graph['v_lon'] == lon_2))]
            end_node = row['v'].values[0]

        
    
    # Build the adjacency list
    adj = dict()
    for index, row in graph.iterrows():
        u = row['u']
        v = row['v']
        w = row['length']
        if u not in adj:
            adj[u] = set()
        if v not in adj:
            adj[v] = set()
        adj[u].add((v, w))
        adj[v].add((u, w))

    is_done = set()
    dist = {start_node: 0}
    pq = min_heap()
    pq.push(start_node, 0)
    pred = dict()

    while pq.size() > 0:
        u = pq.pop()
        is_done.add(u)
        if u == end_node:
            return restore_path(start_node, end_node, pred)
        for neighbor in adj[u]:
            v = neighbor[0]
            w = neighbor[1]
            if v in is_done:
                continue
            if v not in dist:
                dist[v] = float('inf')
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                pred[v] = u
                pq.push(v, dist[v])
    return []

