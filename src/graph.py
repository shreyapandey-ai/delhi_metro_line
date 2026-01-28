import sqlite3
from collections import defaultdict

def station_name_to_code(name):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(
        "SELECT station_code FROM stations WHERE station_name = ?",
        (name.upper(),)
    )
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None

def load_graph(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    graph = defaultdict(list)

    cur.execute("""
        SELECT from_station, to_station, travel_time
        FROM routes
    """)

    for src, dst, time_sec in cur.fetchall():
        graph[src].append((dst, time_sec))

    conn.close()
    return graph
