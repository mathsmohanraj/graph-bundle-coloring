"""
Total Coloring of Graph Bundles (Path Bundles Pm x F)
Based on the Constructive Algorithm for Type-1 Preservation.
Author: M. Mohanraj
"""

import networkx as nx

def generate_perfect_matchings(n):
    """Generate n perfect matchings for K_{n,n} using standard construction."""
    matchings = []
    for k in range(n):
        # Changed 'i' to 'v' to avoid variable shadowing with outer loops
        matching = [(v, (v + k) % n) for v in range(n)]
        matchings.append(matching)
    return matchings

def cyclic_shift(color, color_set):
    """
    Apply cyclic shift derangement within the given color set.
    """
    sorted_colors = sorted(color_set)
    idx = sorted_colors.index(color)
    return sorted_colors[(idx + 1) % len(sorted_colors)]

def total_coloring_path_bundle(m, fiber_graph, fiber_total_coloring):
    """
    Constructive polynomial-time algorithm for total coloring of Pm x F.
    
    Parameters:
    m (int): Number of vertices in the base path (Pm).
    fiber_graph (nx.Graph): The Type-1 fiber graph (F).
    fiber_total_coloring (dict): Valid Type-1 total coloring of the base fiber F1.
                                 Keys are vertices (int) and edges (tuple of two ints).
                                 Values are colors (int).
    
    Returns:
    dict: A valid Total Coloring for the Graph Bundle.
    """
    n = len(fiber_graph.nodes)
    
    if n == 0:
        raise ValueError("Fiber graph cannot be empty.")
        
    delta_F = max(dict(fiber_graph.degree()).values())
    delta_G = delta_F + 2 * n  # Maximum degree of the path bundle (Internal fibers)
    
    # Initialize global palette C: {1, 2, ..., Delta(G) + 1}
    global_palette = set(range(1, delta_G + 2))
    
    # Determine fiber color set (C_fiber) from the given coloring
    C_fiber = set(fiber_total_coloring.values())
    
    # Store the final coloring of all elements
    bundle_coloring = {}
    fiber_colorings = {}
    
    # Step 1: Apply phi to F1
    fiber_colorings[0] = fiber_total_coloring.copy()
    
    # Step 2: Loop through the base path vertices
    for i in range(1, m):
        # Apply cyclic shift derangement for the next fiber
        prev_fiber_coloring = fiber_colorings[i-1]
        next_fiber_coloring = {}
        
        for element, color in prev_fiber_coloring.items():
            next_fiber_coloring[element] = cyclic_shift(color, C_fiber)
            
        fiber_colorings[i] = next_fiber_coloring
        
        # Extract colors used strictly on vertices of adjacent fibers (needed for join)
        vertex_colors_i_1 = {color for element, color in prev_fiber_coloring.items() 
                              if isinstance(element, int)}
        vertex_colors_i = {color for element, color in next_fiber_coloring.items() 
                           if isinstance(element, int)}
        
        # Available colors for bipartite join (C_avail)
        used_vertex_colors = vertex_colors_i_1 | vertex_colors_i
        c_avail = global_palette - used_vertex_colors
        
        # Ensure at least n colors available for K_{n,n} matching
        if len(c_avail) < n:
            raise ValueError(f"Insufficient colors for join edges between F_{i-1} and F_{i}.")
        
        # Decompose E_join into perfect matchings (K_n,n)
        perfect_matchings = generate_perfect_matchings(n)
        
        # Assign colors to bipartite edges deterministically
        join_edges_coloring = {}
        c_avail_list = sorted(list(c_avail)) # Sorted for deterministic outputs
        
        for idx, matching in enumerate(perfect_matchings[:n]):
            color_c = c_avail_list[idx]
            for edge in matching:
                # Edge is represented as tuple ((i-1, u), (i, v))
                join_edges_coloring[((i-1, edge[0]), (i, edge[1]))] = color_c
                
        bundle_coloring[f'E_join_{i-1}_to_{i}'] = join_edges_coloring
    
    # Store all fiber colorings into the final output
    for i in range(m):
        bundle_coloring[f'Fiber_{i}'] = fiber_colorings[i]
    
    return bundle_coloring


if __name__ == "__main__":
    # Example Execution: Path Bundle P3 x P2
    # Base graph: Path with 3 vertices (m=3)
    # Fiber graph: Path with 2 vertices (n=2)
    
    m_base = 3
    fiber = nx.path_graph(2)
    
    # A valid proper total coloring of P2 using colors {1, 2, 3}
    # Vertices: 0 -> Color 1, 1 -> Color 2. Edge: (0,1) -> Color 3
    base_phi = {0: 1, 1: 2, (0, 1): 3}
    
    print(f"--- Executing Total Coloring for Path Bundle P{m_base} x P{len(fiber.nodes)} ---")
    print(f"Base Fiber Coloring (Phi): {base_phi}\n")
    
    try:
        result = total_coloring_path_bundle(m_base, fiber, base_phi)
        print("? Total Coloring Successful! No incidence conflicts detected.\n")
        
        for key, value in sorted(result.items()):
            print(f"{key}:")
            print(f"  {value}\n")
            
    except ValueError as e:
        print(f"? Error: {e}")
