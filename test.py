from flask import Flask, request, jsonify
import time, sqlite3, datetime

app = Flask(__name__)
db = "animal_feeder.db"

conn = sqlite3.connect(db)
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

cursor.execute("""
CREATE TABLE IF NOT EXISTS cameras (
    cam_id TEXT UNIQUE NOT NULL,
    status TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS modules (
    mpdule_id TEXT UNIQUE NOT NULL,
    cam_id TEXT,
    status TEXT DEFAULT 'inactive' CHECK (status IN ('active', 'inactive')),
    weight REAL NOT NULL,
    FOREIGN KEY (cam_id) REFERENCES camera(cam_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS schedules (
    schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
    module_id TEXT,
    feed_time TEXT NOT NULL,
    amount REAL NOT NULL,
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'done')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (module_id) REFERENCES modules(module_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS history (
    history_id INTEGER PRIMARY KEY AUTOINCREMENT,
    schedule_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (schedule_id) REFERENCES schedules(schedule_id)
)
""")

conn.commit()
conn.close()

@app.route("/")
def home():
    return "mDNS OK"

@app.route("/check_sched", methods=["GET"])
def check_sched():
    device_id = request.args.get("device_id")
    if not device_id:
        return jsonify({"error": "Missing device_id"}), 400

    # now = datetime.datetime.now().strftime( "%H:%M")
    # conn = sqlite3.connect(DB)
    # cursor = conn.cursor()

    # cursor.execute("""
    #     SELECT schedule_id FROMM schedules
    #     WHERE device_id=? AND feed_time=? AND status='pending'
    # """, (device_id, now))

    # row = ccursor.fetchone()
    # conn.close()

    # if row:
    #     return jsonify({"dispense": True, "schedule_id": row[0]})
    # else:
    #     return jsonify({"dispense": False})

    if device_id == "MODULE01":
        return jsonify({"dispense": True, "amount": 100})
    else:
        return jsonify({"dispense": False})

@app.route("/weight_update", methods=["POST"])
def weight_update():
    device_id = request.form.get("device_id")
    weight = request.form.get("weight")
    status = "active"
    cam_id = "CAMERA01"

    print("Device ID:", device_id)
    print("Cam ID:", cam_id)
    print("Status:", status)
    print("Weight:", weight)

    # conn = sqlite3.connect(db)
    # cursor = conn.cursor()

    # cursor.execute("""
    #     INSERT INTO modules (device_id, cam_id, status, weight)
    #     VALUES (?, ?, ?, ?)
    # """, (device_id, cam_id, status, weight))

    return "Received: " + str(device_id) + ", " + str(cam_id) + ", " + str(status) + ", " + str(weight)

@app.route("/upload_image", methods=["POST"])
def upload_image():
    image = request.data

    filename = f"cam_{int(time.time())}.jpg"
    with open(filename, "wb") as f:
        f.write(image)

    print(f"Saved: {filename}, Size: {len(image)} bytes")
    return "Image received", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
