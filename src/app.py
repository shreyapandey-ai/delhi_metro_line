import os
import sqlite3
from graph import load_graph
from shortest_path import dijkstra

# ---------------- PATH ----------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "db", "delhi_metro_final.db")

# ---------------- DB HELPERS ----------------
def station_name_to_code(name):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT station_code FROM stations WHERE station_name = ?",
        (name.upper(),)
    )
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None

# ---------------- LOAD GRAPH ----------------
graph = load_graph(DB_PATH)
print("Total stations:", len(graph))
print("Sample graph keys:", list(graph.keys())[:5])

# ---------------- INPUT ----------------
start_name = "RAJIV CHOWK"
end_name = "DELHI GATE"

start = station_name_to_code(start_name)
end = station_name_to_code(end_name)

print("Start:", start_name, "→", start)
print("End:", end_name, "→", end)

if not start or not end:
    raise ValueError("Invalid station name")

# ---------------- SHORTEST PATH ----------------
distance, path = dijkstra(graph, start, end)

print("Distance:", distance)
print("Path:", path)
