import uuid
import networkx as nx
import matplotlib.pyplot as plt
import heapq
from collections import deque

class Node:
    def __init__(self, key, color="#1296F0"):
        self.left = None
        self.right = None
        self.value = key
        self.color = color  # Additional argument to store node color
        self.id = str(uuid.uuid4())  # Unique identifier for each node

    def __str__(self):
        return f"Node(value={self.value}, color={self.color}, id={self.id})"

def add_edges(graph, node, pos, x=0, y=0, layer=1):
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.value)  # Use id and store node value
        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2 ** layer
            pos[node.left.id] = (l, y - 1)
            l = add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer
            pos[node.right.id] = (r, y - 1)
            r = add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    return graph

def heap_to_tree(heap, index=0):
    if index >= len(heap):
        return None
    node = Node(heap[index])
    node.left = heap_to_tree(heap, 2 * index + 1)
    node.right = heap_to_tree(heap, 2 * index + 2)
    return node

def collect_dfs_steps(node):
    steps = []
    if node:
        steps.append(node)
        steps.extend(collect_dfs_steps(node.left))
        steps.extend(collect_dfs_steps(node.right))
    return steps

def collect_bfs_steps(node):
    steps = []
    if not node:
        return steps
    queue = deque([node])
    while queue:
        current = queue.popleft()
        steps.append(current)
        if current.left:
            queue.append(current.left)
        if current.right:
            queue.append(current.right)
    return steps

def generate_colors(base_color, num_tints):
    base_rgb = tuple(int(base_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    tints = []
    for i in range(num_tints):  # Avoid white color
        factor = i / (num_tints)  # Scale factor from 0 to 1
        tint_rgb = tuple(base_rgb[j] + (1 - base_rgb[j]) * factor for j in range(3))
        tints.append(tint_rgb)
    
    return tints[:num_tints]

def assign_colors_to_nodes(colors, path):
    for step, color in zip(path, colors):
        step.color = color
    return [step.color for step in path]

def print_bfs_steps(node, colors):
    steps = collect_bfs_steps(node)
    
    assign_colors_to_nodes(colors, steps)
    for step in steps:
        print(f"Node(value={step.value}, color={step.color}, id={step.id})")
    print()  # For newline


def draw_tree(tree_root, traversal_func):
    path = traversal_func(tree_root)
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    tree = add_edges(tree, tree_root, pos)

    nodes = [node.id for node in path]
    num_nodes = len(nodes)
    colors = generate_colors("1296F0", num_nodes)
    print(f"colors: {colors}")
    print_bfs_steps(tree_root, colors)
    #values = assign_colors_to_nodes(colors, path))
    labels = {node[0]: node[1]['label'] for node in tree.nodes(data=True)}  # Use node value for labels
    node_colors = [node.color for node in path]
    plt.figure(figsize=(8, 5))
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=node_colors)
    plt.show()


# Create the tree
data = [2, 3, 6, 1, 7, 3, 8, 1, 5]
heapq.heapify(data)
tree = heap_to_tree(data)

# Display the tree with BFS traversal
print("BFS Traversal:")

draw_tree(tree, collect_bfs_steps)
