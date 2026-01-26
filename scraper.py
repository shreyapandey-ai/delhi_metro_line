import json
import time
import sqlite3
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

# ---------------- CONFIG ----------------
DB = "db/delhi_metro_final.db"
HEADERS = {"User-Agent": "Mozilla/5.0"}

# ---------------- DB ----------------
conn = sqlite3.connect(DB)
cur = conn.cursor()

# ---------------- SAFE FETCH ----------------
def fetch(url, retries=3):
    for _ in range(retries):
        try:
            req = Request(url, headers=HEADERS)
            with urlopen(req, timeout=20) as r:
                return json.loads(r.read().decode())
        except (HTTPError, URLError) as e:
            print(f"⚠️ API error → {url}")
            time.sleep(2)
        except Exception:
            time.sleep(2)
    print(f"❌ Skipped → {url}")
    return None

# ---------------- 1. LINES ----------------
LINES_API = "https://backend.delhimetrorail.com/api/v2/en/line_list?format=json"
lines = fetch(LINES_API)

if not lines:
    print("❌ Line API failed. Exiting.")
    exit()

for l in lines:
    cur.execute(
    """
    INSERT OR IGNORE INTO lines (line_code, line_name, status)
    VALUES (?,?,?)
    """,
    (
        l["line_code"],
        l["name"],
        l.get("status")
    )
)


# ---------------- 2. STATIONS BY LINE ----------------
for l in lines:
    code = l["line_code"]
    url = f"https://backend.delhimetrorail.com/api/v2/en/station_by_line/{code}"
    stations = fetch(url)

    if not stations:
        continue

    for idx, s in enumerate(stations):
        cur.execute(
            "INSERT OR IGNORE INTO stations VALUES (?,?)",
            (s["station_code"], s["station_name"])
        )
        cur.execute(
            """
            INSERT OR IGNORE INTO line_stations
            VALUES (?,?,?)
            """,
            (code, s["station_code"], idx + 1)
        )

# ---------------- 3. FARE + ROUTE ----------------
def fetch_fare(f, t):
    url = f"https://backend.delhimetrorail.com/api/v2/en/new_fare_with_route/{f}/{t}/least-distance/"
    return fetch(url)

pairs = [("RCK", "DLIG"), ("KG", "CWBR")]

for f, t in pairs:
    data = fetch_fare(f, t)
    if not data:
        continue

    cur.execute(
        """
        INSERT INTO fares
        VALUES (?,?,?,?,?,?)
        """,
        (
            data["from"],
            data["to"],
            data["weekday_fare"],
            data["weekend_fare"],
            data["total_time"],
            data["stations"]
        )
    )

    for r in data["route"]:

      cur.execute(
          """
          INSERT INTO routes
         (from_station, to_station, line_name, start_station, end_station, path_time)
          VALUES (?,?,?,?,?,?)
          """,
        (
           data["from"],
           data["to"],
           r["line"] if isinstance(r["line"], str) else json.dumps(r["line"]),
           r["start"],
           r["end"],
           r["path_time"]
        )
    )



# ---------------- 4. FIRST & LAST TRAIN ----------------
def fetch_first_last(f, t):
    url = f"https://backend.delhimetrorail.com/api/v2/en/first_and_last_train_with_filter/{f}/{t}/least-distance/"
    return fetch(url)

for f, t in pairs:
    d = fetch_first_last(f, t)
    if not d:
        continue

    cur.execute(
           """
           INSERT INTO first_last_trains
          (from_station, to_station, first_train, last_train)
           VALUES (?,?,?,?)
           """,
        (
           f,
           t,
           json.dumps(d.get("first_train")),
           json.dumps(d.get("last_train"))
        )
    )


# ---------------- FINISH ----------------
conn.commit()
conn.close()
print("✅ Delhi Metro data scraping COMPLETE")
