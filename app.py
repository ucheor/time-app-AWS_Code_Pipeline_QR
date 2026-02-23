from flask import Flask, jsonify, send_from_directory
from datetime import datetime
import pytz
import os

app = Flask(__name__, static_folder="static")

TIMEZONES = [
    {"abbr": "PST / PDT", "label": "Pacific Time",  "tz": "America/Los_Angeles", "offset": "UTC−8/−7"},
    {"abbr": "MST / MDT", "label": "Mountain Time", "tz": "America/Denver",       "offset": "UTC−7/−6"},
    {"abbr": "CST / CDT", "label": "Central Time",  "tz": "America/Chicago",      "offset": "UTC−6/−5"},
    {"abbr": "EST / EDT", "label": "Eastern Time",  "tz": "America/New_York",     "offset": "UTC−5/−4"},
]

@app.route("/api/times")
def get_times():
    result = []
    for zone in TIMEZONES:
        tz = pytz.timezone(zone["tz"])
        now = datetime.now(tz)
        result.append({
            "abbr":   zone["abbr"],
            "label":  zone["label"],
            "offset": zone["offset"],
            "time":   now.strftime("%I:%M:%S"),
            "ampm":   now.strftime("%p"),
            "date":   now.strftime("%a, %b %d %Y"),
            "hour24": now.hour,
        })

    utc_now = datetime.now(pytz.utc)
    return jsonify({
        "zones": result,
        "utc": utc_now.strftime("%H:%M:%S UTC"),
    })

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
