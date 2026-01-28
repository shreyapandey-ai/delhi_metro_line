import heapq

def dijkstra(graph, start, end):
    pq = [(0, start, [])]
    visited = set()

    while pq:
        cost, node, path = heapq.heappop(pq)

        if node in visited:
            continue
        visited.add(node)

        path = path + [node]

        if node == end:
            return cost, path

        for nxt, weight in graph.get(node, []):
            if nxt not in visited:
                heapq.heappush(pq, (cost + weight, nxt, path))

    return float("inf"), []

import json
import sqlite3

def save_shortest_path(db_path, start, end, distance, path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute(
        """
        INSERT OR REPLACE INTO shortest_paths
        (from_station, to_station, distance_meters, path)
        VALUES (?,?,?,?)
        """,
        (start, end, distance, json.dumps(path))
    )

    conn.commit()
    conn.close()
