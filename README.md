# Graph Bundle Total Coloring

This repository contains the Python implementation of **Algorithm 1** from the paper:

**"Structural Decomposition, Algorithmic Complexity, and Total Coloring of Graph Bundles"** by M. Mohanraj and C. Vimala (IAENG Journal, 2026)

## 📁 Files
- `Graph-Bundle-Coloring.py` – Main implementation of Algorithm 1 for total coloring of path bundles (P_m \times F).
- `experiments.py` – Script to reproduce the experimental results shown in **Table I** and **Table II** of the paper.

## 📦 Requirements
- Python 3.9 or higher
- NetworkX (`pip install networkx`)

## 🚀 Usage
1. Clone the repository:
```bash
   git clone [https://github.com/mathsmohanraj/graph-bundle-coloring.git](https://github.com/mathsmohanraj/graph-bundle-coloring.git)
   cd graph-bundle-coloring

## 📝 Notes
- The current implementation uses \(P_2\) as the fiber graph (which is **Type‑2**) for demonstration.  
  For **Type‑1** fibers (e.g., \(P_3\), \(P_4\)), the total number of colours used by the algorithm will be \(\Delta(G)+1\) exactly as proved in the paper.
- The implementation follows the constructive proof of Theorem 1 and produces a valid total colouring without incidence conflicts.  
- All colour palettes are defined dynamically based on the maximum degree of the bundle.
