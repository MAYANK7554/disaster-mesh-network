import networkx as nx
import matplotlib.pyplot as plt

def draw_network(G, path, title, figure_num):
    """Helper function to visualize the network and highlight the routing path."""
    plt.figure(figure_num, figsize=(8, 6))
    
    # Generate a layout for the nodes (seed ensures it looks the same every time)
    pos = nx.spring_layout(G, seed=42)
    
    # Draw all nodes and edges in standard colors
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, 
            font_size=12, font_weight='bold', edge_color='gray')
    
    # Highlight the shortest path in red if a path exists
    if path:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='lightgreen', node_size=2000)
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3)
        
    plt.title(title)
    # plt.show(block=False) allows the code to continue running while keeping the window open
    plt.show(block=False) 

def main():
    print("--- Disaster-Resilient Mesh Network Simulation ---")
    
    # 1. Initialize an undirected graph
    G = nx.Graph()
    
    # 2. Add nodes (R1 to R6 represent routers)
    nodes = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6']
    G.add_nodes_from(nodes)
    
    # 3. Create a mesh-like topology (Multiple paths exist between source and destination)
    # The numbers represent abstract link 'costs' or 'weights' (e.g., latency)
    edges = [
        ('R1', 'R2', 2), ('R1', 'R3', 4),
        ('R2', 'R4', 3), ('R2', 'R5', 6),
        ('R3', 'R4', 2), ('R3', 'R6', 5),
        ('R4', 'R5', 2), ('R4', 'R6', 1),
        ('R5', 'R6', 3)
    ]
    G.add_weighted_edges_from(edges)
    
    source = 'R1'
    destination = 'R6'
    
    # 4. Calculate initial shortest path (Normal Operation)
    print("\n[INFO] Normal Operation: Calculating shortest path from {} to {}...".format(source, destination))
    try:
        # Dijkstra's algorithm is used by default for weighted graphs in NetworkX
        initial_path = nx.shortest_path(G, source=source, target=destination, weight='weight')
        initial_cost = nx.shortest_path_length(G, source=source, target=destination, weight='weight')
        print("-> Optimal Path: {}".format(" -> ".join(initial_path)))
        print("-> Total Cost: {}".format(initial_cost))
        
        # Visualize pre-disaster network
        draw_network(G, initial_path, "Pre-Disaster: Normal Routing", 1)
        
    except nx.NetworkXNoPath:
        print("-> Error: No path exists between {} and {}.".format(source, destination))

    # Wait for user input to simulate the disaster
    input("\nPress Enter to simulate a disaster (Node R4 fails)...")
    
    # 5. Simulate Disaster (Node Failure)
    failed_node = 'R4'
    print("\n[ALERT] Disaster simulated: Node {} has failed and is removed from the network!".format(failed_node))
    G.remove_node(failed_node)
    
    # 6. Recalculate path after failure (Resilience)
    print("\n[INFO] Rerouting: Calculating new path from {} to {}...".format(source, destination))
    try:
        new_path = nx.shortest_path(G, source=source, target=destination, weight='weight')
        new_cost = nx.shortest_path_length(G, source=source, target=destination, weight='weight')
        print("-> New Optimal Path: {}".format(" -> ".join(new_path)))
        print("-> New Total Cost: {}".format(new_cost))
        
        # Visualize post-disaster network
        draw_network(G, new_path, "Post-Disaster: Rerouted Network", 2)
        
    except nx.NetworkXNoPath:
        print("-> CRITICAL FAILURE: No alternative path exists. Network partitioned.")

    print("\nSimulation complete. Close the plot windows to exit.")
    plt.show() # Keeps windows open until the user closes them

if __name__ == "__main__":
    main()