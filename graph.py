import networkx as nx
import matplotlib.pyplot as plt
from collections import deque, defaultdict
import heapq

# 1.1. Nhập đồ thị
def input_graph():
    G = nx.Graph()
    n = int(input("Nhập số lượng đỉnh: "))
    vertices = []
    print("Nhập tên các đỉnh:")
    for i in range(n):
        v = input(f"Đỉnh {i+1}: ")
        vertices.append(v)
        G.add_node(v)
    print("Nhập trọng số giữa các đỉnh (0 = không nối):")
    for i in range(n):
        for j in range(i + 1, n):
            try:
                w = int(input(f"{vertices[i]} - {vertices[j]}: "))
                if w != 0:
                    G.add_edge(vertices[i], vertices[j], weight=w)
            except:
                print("Lỗi nhập, bỏ qua!")

    return G


# 1.2. Vẽ đồ thị trực quan
def draw_graph(G):
    pos = nx.spring_layout(G)
    nx.draw(G, pos,
            with_labels=True,
            node_color='lightblue',
            node_size=2000)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.title("Graph bạn vừa nhập")
    plt.savefig("graph.png")
    plt.show()


# 2. Lưu đồ thị
def save_graph(G):
    nx.write_weighted_edgelist(G, "graph.txt")
    print("Đã lưu đồ thị vào file graph.txt")


# Convert cho Dijkstra / Prim
def convert_to_dict(G):
    graph = {}
    for u in G.nodes():
        graph[u] = []
        for v in G.neighbors(u):
            w = G[u][v]['weight']
            graph[u].append((v, w))
    return graph


# Convert cho BFS/DFS
def convert_to_unweighted_dict(G):
    graph = {}
    for u in G.nodes():
        graph[u] = list(G.neighbors(u))
    return graph


# Convert cho kiểm tra 2 phía
def convert_to_index_graph(G):
    nodes = list(G.nodes())
    index_map = {node: i for i, node in enumerate(nodes)}
    graph = [[] for _ in range(len(nodes))]
    for u in G.nodes():
        for v in G.neighbors(u):
            graph[index_map[u]].append(index_map[v])
    return graph, nodes


# 3.Tìm đường đi ngắn nhất (Dijkstra)
def dijkstra(graph, start):
    dist = {v: float('inf') for v in graph}
    dist[start] = 0
    visited = set()
    while len(visited) < len(graph):
        u = min((v for v in graph if v not in visited), key=lambda x: dist[x])
        visited.add(u)
        if dist[u] == float('inf'):
            break
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return dist


# 4.1. BFS
def bfs(graph, start):
    visited = set()
    queue = deque([start])
    visited.add(start)
    order = []
    print(f"\n🔵 BFS từ đỉnh {start}:")
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    print(f"  Thứ tự BFS: {order}")
    return order


# 4.2. DFS
def dfs_iterative(graph, start):
    visited = set()
    stack = [start]
    order = []
    print(f"\n🟢 DFS từ đỉnh {start}:")
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        order.append(node)
        for neighbor in reversed(graph[node]):
            if neighbor not in visited:
                stack.append(neighbor)
    print(f"  Thứ tự DFS: {order}")
    return order


# 5.  Kiểm tra một đồ thị có phải là đồ thị 2 phía không?
def kiem_tra_2_phia(do_thi, so_dinh):
    mau = [-1] * so_dinh
    for bat_dau in range(so_dinh):
        if mau[bat_dau] == -1:
            hang_doi = deque([bat_dau])
            mau[bat_dau] = 0
            while hang_doi:
                dinh = hang_doi.popleft()
                for dinh_ke in do_thi[dinh]:
                    if mau[dinh_ke] == -1:
                        mau[dinh_ke] = 1 - mau[dinh]
                        hang_doi.append(dinh_ke)
                    elif mau[dinh_ke] == mau[dinh]:
                        return False
    return True


# 6. Chuyển đổi qua lại giữa các phương pháp biểu diễn đồ thị:
class chuyendoi:
    def __init__(self, dothi=False):
        self.dothi = dothi
    def matran_danhsach(self, matran):
        return {i: [j for j in range(len(matran)) if matran[i][j] != 0] for i in range(len(matran))}
    def matran_canh(self, matran):
        return [(i, j) for i in range(len(matran)) for j in range(len(matran))
                if matran[i][j] != 0 and (self.dothi or i <= j)]


# 7.1 Prim
def prim(graph, start):
    in_tree = {start}
    mst_edges = []
    heap = [(w, start, v) for v, w in graph[start]]
    heapq.heapify(heap)
    while heap and len(in_tree) < len(graph):
        weight, u, v = heapq.heappop(heap)
        if v in in_tree:
            continue
        in_tree.add(v)
        mst_edges.append((weight, u, v))
        for neighbor, w in graph[v]:
            if neighbor not in in_tree:
                heapq.heappush(heap, (w, v, neighbor))
    return mst_edges


# 7.2 Kruskal
def kruskal(graph):
    edges = []
    for u in graph:
        for v, w in graph[u]:
            if u < v:  # tránh trùng cạnh
                edges.append((w, u, v))
    edges.sort()
    parent = {x: x for x in graph}
    rank = {x: 0 for x in graph}
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        if rank[ra] < rank[rb]:
            parent[ra] = rb
        elif rank[ra] > rank[rb]:
            parent[rb] = ra
        else:
            parent[rb] = ra
            rank[ra] += 1
        return True
    mst = []
    total = 0
    print("\n🌲 KRUSKAL - CÂY KHUNG NHỎ NHẤT")
    for w, u, v in edges:
        if union(u, v):
            mst.append((u, v, w))
            total += w
            print(f"{u} -- {v} ({w})")

    print("Tổng:", total)

# 7.3 Ford-Fulkerson
def bfs_ff(capacity, s, t, parent):
    visited = [False] * len(capacity)
    queue = deque([s])
    visited[s] = True
    parent[s] = -1
    while queue:
        u = queue.popleft()
        for v in range(len(capacity)):
            if not visited[v] and capacity[u][v] > 0:
                queue.append(v)
                parent[v] = u
                visited[v] = True
    return visited[t]
def ford_fulkerson(capacity, s, t):
    parent = [-1] * len(capacity)
    max_flow = 0
    while bfs_ff(capacity, s, t, parent):
        path_flow = float('inf')
        v = t
        while v != s:
            u = parent[v]
            path_flow = min(path_flow, capacity[u][v])
            v = u
        v = t
        while v != s:
            u = parent[v]
            capacity[u][v] -= path_flow
            capacity[v][u] += path_flow
            v = u
        max_flow += path_flow
    return max_flow


# 7.4 Fleury
class GraphFleury:
    def __init__(self, V):
        self.V = V
        self.graph = defaultdict(list)
    def them_canh(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)
    def xoa_canh(self, u, v):
        if v in self.graph[u]:
            self.graph[u].remove(v)
        if u in self.graph[v]:
            self.graph[v].remove(u)
    def dfs(self, v, visited):
        count = 1
        visited[v] = True
        for i in self.graph[v]:
            if not visited[i]:
                count += self.dfs(i, visited)
        return count
    def is_bridge(self, u, v):
        if len(self.graph[u]) == 1:
            return True
        visited = [False] * self.V
        before = self.dfs(u, visited)
        self.xoa_canh(u, v)
        visited = [False] * self.V
        after = self.dfs(u, visited)
        self.them_canh(u, v)
        return after < before
    def fleury(self, u, path):
        for v in list(self.graph[u]):
            if not self.is_bridge(u, v):
                path.append((u, v))
                self.xoa_canh(u, v)
                self.fleury(v, path)
                return
        for v in list(self.graph[u]):
            path.append((u, v))
            self.xoa_canh(u, v)
            self.fleury(v, path)
            return
    def start(self):
        start = 0
        for i in range(self.V):
            if len(self.graph[i]) % 2 != 0:
                start = i
                break
        path = []
        self.fleury(start, path)
        return path


# 7.5 Hierholzer
def hierholzer(graph, start):
    for u in graph:
        if len(graph[u]) % 2 != 0:
            return "Không phải đồ thị Euler (có đỉnh bậc lẻ)"
    temp = {u: graph[u][:] for u in graph}
    stack = [start]
    path = []
    while stack:
        u = stack[-1]
        if temp[u]:
            v = temp[u].pop()
            temp[v].remove(u)   # FIX QUAN TRỌNG
            stack.append(v)
        else:
            path.append(stack.pop())
    return path[::-1]


# MAIN
if __name__ == "__main__":
    G = input_graph()
    draw_graph(G)
    save_graph(G)

    graph_weighted = convert_to_dict(G)
    graph_unweighted = convert_to_unweighted_dict(G)

    start = input("\nNhập đỉnh bắt đầu: ")

    result = dijkstra(graph_weighted, start)
    print("\nDijkstra:")
    for node in result:
        print(f"{start} -> {node} = {result[node]}")

    bfs(graph_unweighted, start)
    dfs_iterative(graph_unweighted, start)

    graph_index, nodes = convert_to_index_graph(G)
    print("\nHai phía:", kiem_tra_2_phia(graph_index, len(nodes)))

    print("\n🌳 PRIM")
    mst = prim(graph_weighted, start)
    total = 0
    for w, u, v in mst:
        print(f"{u} -- {v} ({w})")
        total += w
    print("Tổng:", total)

    kruskal(graph_weighted)

    print("\n🌊 FORD-FULKERSON")
    nodes = list(graph_weighted.keys())
    index = {nodes[i]: i for i in range(len(nodes))}

    n = len(nodes)
    capacity = [[0] * n for _ in range(n)]

    for u in graph_weighted:
        for v, w in graph_weighted[u]:
            capacity[index[u]][index[v]] = w

    s = index[start]
    t_name = input("Đỉnh đích: ")
    t = index[t_name]

    print("Max Flow:", ford_fulkerson(capacity, s, t))

    print("\n🔁 FLEURY")
    nodes_list = list(graph_unweighted.keys())
    index_map = {nodes_list[i]: i for i in range(len(nodes_list))}

    g_f = GraphFleury(len(nodes_list))

    for u in graph_unweighted:
        for v in graph_unweighted[u]:
            g_f.them_canh(index_map[u], index_map[v])

    fleury_path = g_f.start()
    print([(nodes_list[u], nodes_list[v]) for u, v in fleury_path])

    print("\n🔁 HIERHOLZER")
    print(hierholzer(graph_unweighted, start))