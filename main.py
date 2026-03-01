import tkinter as tk
from queue import PriorityQueue
import math
import time

CELL_SIZE = 30
GRID_SIZE = 10

EMPTY_COLOR = "white"
OBSTACLE_COLOR = "black"
FRONTIER_COLOR = "yellow"
VISITED_COLOR = "pink"
PATH_COLOR = "#98FB98"
START_COLOR = "orange"
GOAL_COLOR = "purple"

root = tk.Tk()
root.title("Pathfinding Visualization")

canvas = tk.Canvas(root, width=GRID_SIZE*CELL_SIZE, height=GRID_SIZE*CELL_SIZE)
canvas.pack()

metrics_label = tk.Label(root, text="", font=("Arial", 12))
metrics_label.pack(pady=5)

# Grid Initialization 
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
rects = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

for r in range(GRID_SIZE):
    for c in range(GRID_SIZE):
        rects[r][c] = canvas.create_rectangle(
            c*CELL_SIZE, r*CELL_SIZE,
            (c+1)*CELL_SIZE, (r+1)*CELL_SIZE,
            fill=EMPTY_COLOR, outline="gray"
        )

start_node = None
goal_node = None
placing = "start"  

def manhattan(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def euclidean(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def get_neighbors(node):
    directions = [(1,0), (-1,0), (0,1), (0,-1)]
    neighbors = []
    r, c = node
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
            if grid[nr][nc] == 0:
                neighbors.append((nr, nc))
    return neighbors

def reconstruct_path(came_from, current):
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.append(current)
    path.reverse()
    return path

def visualize_node(node, color, delay=0.02):
    r, c = node
    canvas.itemconfig(rects[r][c], fill=color)
    root.update()
    time.sleep(delay)

def reset_grid_colors():
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if (r, c) == start_node:
                canvas.itemconfig(rects[r][c], fill=START_COLOR)
            elif (r, c) == goal_node:
                canvas.itemconfig(rects[r][c], fill=GOAL_COLOR)
            elif grid[r][c] == 1:
                canvas.itemconfig(rects[r][c], fill=OBSTACLE_COLOR)
            else:
                canvas.itemconfig(rects[r][c], fill=EMPTY_COLOR)

def a_star(start, goal, heuristic):
    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    g_score = {start: 0}
    visited_count = 0
    start_time = time.time()

    while not open_set.empty():
        current = open_set.get()[1]
        visited_count += 1
        if current != start and current != goal:
            visualize_node(current, VISITED_COLOR)

        if current == goal:
            end_time = time.time()
            path = reconstruct_path(came_from, current)
            for node in path:
                if node != start and node != goal:
                    visualize_node(node, PATH_COLOR, delay=0)
            metrics_label.config(
                text=f"Nodes Visited: {visited_count}  |  Path Cost: {len(path)-1}  |  Time: {round((end_time-start_time)*1000,2)} ms"
            )
            return

        for neighbor in get_neighbors(current):
            temp_g = g_score[current] + 1
            if neighbor not in g_score or temp_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g
                f_score = temp_g + heuristic(neighbor, goal)
                open_set.put((f_score, neighbor))
                if neighbor != start and neighbor != goal:
                    visualize_node(neighbor, FRONTIER_COLOR)

def greedy_bfs(start, goal, heuristic):
    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    visited = set()
    visited_count = 0
    start_time = time.time()

    while not open_set.empty():
        current = open_set.get()[1]
        visited_count += 1
        if current != start and current != goal:
            visualize_node(current, VISITED_COLOR)

        if current == goal:
            end_time = time.time()
            path = reconstruct_path(came_from, current)
            for node in path:
                if node != start and node != goal:
                    visualize_node(node, PATH_COLOR, delay=0)
            metrics_label.config(
                text=f"Nodes Visited: {visited_count}  |  Path Cost: {len(path)-1}  |  Time: {round((end_time-start_time)*1000,2)} ms"
            )
            return

        visited.add(current)

        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                came_from[neighbor] = current
                priority = heuristic(neighbor, goal)
                open_set.put((priority, neighbor))
                if neighbor != start and neighbor != goal:
                    visualize_node(neighbor, FRONTIER_COLOR)

def on_canvas_click(event):
    global start_node, goal_node, placing
    r = event.y // CELL_SIZE
    c = event.x // CELL_SIZE

    if placing == "start":
        if start_node:
            canvas.itemconfig(rects[start_node[0]][start_node[1]], fill=EMPTY_COLOR)
        start_node = (r, c)
        canvas.itemconfig(rects[r][c], fill=START_COLOR)

    elif placing == "goal":
        if goal_node:
            canvas.itemconfig(rects[goal_node[0]][goal_node[1]], fill=EMPTY_COLOR)
        goal_node = (r, c)
        canvas.itemconfig(rects[r][c], fill=GOAL_COLOR)

    elif placing == "obstacle":
        if (r, c) != start_node and (r, c) != goal_node:
            grid[r][c] = 1 - grid[r][c]  
            color = OBSTACLE_COLOR if grid[r][c] == 1 else EMPTY_COLOR
            canvas.itemconfig(rects[r][c], fill=color)

canvas.bind("<Button-1>", on_canvas_click)

def start_algorithm(algorithm, heuristic_choice):
    if start_node is None or goal_node is None:
        metrics_label.config(text="Please set start and goal nodes!")
        return
    reset_grid_colors()
    heuristic = manhattan if heuristic_choice == "Manhattan" else euclidean
    if algorithm == "A*":
        a_star(start_node, goal_node, heuristic)
    else:
        greedy_bfs(start_node, goal_node, heuristic)

controls_frame = tk.Frame(root)
controls_frame.pack(pady=5)

tk.Label(controls_frame, text="Algorithm:").pack(side=tk.LEFT)
tk.Button(controls_frame, text="A*", command=lambda: start_algorithm("A*", heuristic_var.get())).pack(side=tk.LEFT)
tk.Button(controls_frame, text="Greedy BFS", command=lambda: start_algorithm("Greedy BFS", heuristic_var.get())).pack(side=tk.LEFT)

heuristic_var = tk.StringVar(value="Manhattan")
tk.Label(root, text="Heuristic:").pack()
tk.Radiobutton(root, text="Manhattan", variable=heuristic_var, value="Manhattan").pack()
tk.Radiobutton(root, text="Euclidean", variable=heuristic_var, value="Euclidean").pack()

placement_frame = tk.Frame(root)
placement_frame.pack(pady=5)
tk.Label(placement_frame, text="Click Mode:").pack(side=tk.LEFT)
tk.Button(placement_frame, text="Start Node", command=lambda: set_placing("start")).pack(side=tk.LEFT)
tk.Button(placement_frame, text="Goal Node", command=lambda: set_placing("goal")).pack(side=tk.LEFT)
tk.Button(placement_frame, text="Obstacles", command=lambda: set_placing("obstacle")).pack(side=tk.LEFT)

def set_placing(mode):
    global placing
    placing = mode

root.mainloop()