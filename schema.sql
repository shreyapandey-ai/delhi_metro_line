-- LINES
CREATE TABLE IF NOT EXISTS lines (
    line_code TEXT PRIMARY KEY,
    line_name TEXT,
    status TEXT
);

-- STATIONS (only those appearing in routes)
CREATE TABLE IF NOT EXISTS stations (
    station_code TEXT PRIMARY KEY,
    station_name TEXT
);

-- ROUTES (actual operational paths)
CREATE TABLE IF NOT EXISTS routes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_station TEXT,
    to_station TEXT,
    line_name TEXT,
    start_station TEXT,
    end_station TEXT,
    path_time TEXT
);

-- FARES
CREATE TABLE IF NOT EXISTS fares (
    from_station TEXT,
    to_station TEXT,
    weekday_fare INTEGER,
    weekend_fare INTEGER,
    total_time TEXT,
    stations INTEGER
);

-- FIRST & LAST TRAIN (BONUS)
CREATE TABLE IF NOT EXISTS first_last_trains (
    from_station TEXT,
    to_station TEXT,
    first_train TEXT,
    last_train TEXT
);

-- LINE ↔ STATION MAPPING
CREATE TABLE IF NOT EXISTS line_stations (
    line_code TEXT,
    station_code TEXT,
    station_order INTEGER,
    PRIMARY KEY (line_code, station_code)
);
