import json
import time
import sqlite3
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

DB = "db/delhi_metro_final.db"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch(url):
    try:
        req = Request(url, headers=HEADERS)
        with urlopen(req, timeout=20) as r:
            return json.loads(r.read())
    except (HTTPError, URLError):
        return None

conn = sqlite3.connect(DB)
cur = conn.cursor()

stations = cur.execute(
    "SELECT station_code FROM stations"
).fetchall()

stations = [s[0] for s in stations]

inserted = 0

for i in range(len(stations)):
    for j in range(i + 1, len(stations)):
        f, t = stations[i], stations[j]

        url = f"https://backend.delhimetrorail.com/api/v2/en/new_fare_with_route/{f}/{t}/least-distance/"
        data = fetch(url)

        if not data:
            continue

        cur.execute(
            """
            INSERT OR IGNORE INTO fares
            VALUES (?,?,?,?,?,?)
            """,
            (
                f,
                t,
                data.get("weekday_fare"),
                data.get("weekend_fare"),
                 data.get("total_time"),
                  data.get("stations")
            )

        )

        inserted += 1
        if inserted % 25 == 0:
            conn.commit()
            print(f"✅ {inserted} fares inserted...")
            time.sleep(1)

conn.commit()
conn.close()

print("🎉 FULL FARE MATRIX DONE")
