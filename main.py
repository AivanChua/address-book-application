import sqlite3
from fastapi import FastAPI
from geopy.geocoders import Nominatim

DB_PATH = "address_book.db"

#create database table if not yet existing
def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
      CREATE TABLE IF NOT EXISTS addresses (
        id INTEGER PRIMARY KEY,
        given_address TEXT NOT NULL,
        geocode_address TEXT,
        latitude REAL,
        longitude REAL
      )
    """)
    conn.commit()
    conn.close()

init_db()   

app = FastAPI()

#function for adding address to database
@app.post("/address")
def create_address(address: str):
    geocoder = Nominatim(user_agent="address_book", timeout=10)
    try:
        location = geocoder.geocode(address)
        if not location:
            return {"error":"not found"}

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(
          "INSERT INTO addresses (given_address,geocode_address,latitude,longitude) VALUES (?,?,?,?)",
          (address, location.address, location.latitude, location.longitude)
        )
        conn.commit()
        item_id = cur.lastrowid
        conn.close()

        return {
          "id": item_id,
          "query": address,
          "address": location.address,
          "latitude": location.latitude,
          "longitude": location.longitude
        }
    except Exception as e:
        return {"error": str(e)}

#function for getting addresses from database
@app.get("/addresses")
def get_addresses():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM addresses ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

#function for updating an address in the database
@app.put("/address")
def update_address(given_address: str, latitude: float, longitude: float):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "UPDATE addresses SET latitude = ?, longitude = ? WHERE given_address = ?",
        (latitude, longitude, given_address)
    )
    updated = cur.rowcount
    conn.commit()
    conn.close()

    if updated == 0:
        return {"updated": 0, "message": "No matching address found"}
    return {"updated": updated, "message": f"Updated {updated} row(s)"}

#function to delete address from database
@app.delete("/address")
def delete_address(given_address: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM addresses WHERE given_address = ?",
        (given_address,)
    )
    deleted = cur.rowcount
    conn.commit()
    conn.close()

    if deleted == 0:
        return {"deleted": 0, "message": "No matching address found"}
    return {"deleted": deleted, "message": f"Deleted {deleted} row(s)"}