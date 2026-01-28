# delhi_metro_line

# 🚇 Delhi Metro Line – SQLite Database Project

# This repository contains a structured SQLite database built from multiple CSV datasets related to the Delhi Metro network.
The project focuses on data modeling, normalization, and querying, not just scraping or dumping CSVs.
![Screenshot](route.png)

📌 Project Overview

The goal of this project is to:

Convert raw CSV datasets into a relational SQLite database

Design a clean database schema

Enable easy querying and visualization using SQLite DB Browser

Serve as a foundation for analytics, APIs, or backend services

🗂️ Data Sources (CSV Files)

The following CSV files are used to populate the database:

CSV File	Description
stations.csv	All metro stations with codes, names, and line associations
lines.csv	Metro line details (line code, color, start & end stations)
routes.csv	Station-to-station connectivity across lines
fares.csv	Fare structure between stations
first_last_trains.csv	First and last train timings per station
🧱 Database File

Database Name: delhi_metro_final.db

Database Type: SQLite3

Tool Recommended: DB Browser for SQLite

🗃️ Database Schema

The database follows a normalized relational design.

Tables Overview
stations

Stores master data for metro stations.

station_code (PK)

station_name

line_code

latitude

longitude

lines

Stores metro line information.

line_code (PK)

line_name

color

start_station

end_station

routes

Defines connectivity between stations.

route_id (PK)

from_station

to_station

line_code

fares

Stores fare information.

fare_id (PK)

source_station

destination_station

fare_amount

first_last_trains

Train timing data.

id (PK)

station_code

first_train_time

last_train_time

🔗 Entity Relationship (ER) Design

One line → many stations

Stations are connected via routes

Fares depend on source & destination stations

Train timings map directly to stations

This structure avoids duplication and supports scalable querying.

▶️ How to Use
1️⃣ Open the Database
sqlite3 delhi_metro_final.db


Or open it directly in DB Browser for SQLite.

2️⃣ View Tables
.tables

3️⃣ Inspect Schema
.schema

4️⃣ Sample Queries

Find all stations on a specific line

SELECT station_name
FROM stations
WHERE line_code = 'LN1';


Get fare between two stations

SELECT fare_amount
FROM fares
WHERE source_station = 'RAJIV_CHOWK'
  AND destination_station = 'KASHMERE_GATE';

🛠️ Tech Stack

Python (CSV processing & ingestion)

SQLite3

DB Browser for SQLite

Git & GitHub
