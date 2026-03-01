 Pathfinding Visualization Project

 Overview
This project implements a **Dynamic Pathfinding Agent** that navigates a 2D grid environment.  
The agent uses **informed search algorithms** to find the optimal route from a **fixed start node** to a **goal node**.  

It features an interactive GUI where users can visualize A* and Greedy Best-First Search algorithms in **real-time**. Metrics such as nodes visited, path cost, and execution time are displayed during execution.

---

Features

- **Informed Search Algorithms**: Choose between **A\*** and **Greedy Best-First Search**.  
- **Heuristics**: Toggle between **Manhattan Distance** and **Euclidean Distance**.  
- **Real-Time Visualization**:  
  - **Frontier nodes**: sky blue  
  - **Visited/Expanded nodes**: blue  
  - **Final path**: light pink  
- **Metrics Dashboard**: Displays:  
  - Total nodes visited  
  - Path cost  
  - Execution time (ms)  
- **Step-by-step Agent Movement**: Watch the algorithm explore the grid dynamically and find the path.

---

Dependencies
This project is built entirely using Python's standard libraries:  

- `tkinter` – GUI  
- `queue.PriorityQueue` – frontier management  
- `time` – execution timing  
- `math` – heuristic calculations  

No external modules or installations are required.

---

## How to Run

1. Clone the repository:
```bash
git clone https://github.com/samanexe/Dynamic-Pathfinding-Agent.git
