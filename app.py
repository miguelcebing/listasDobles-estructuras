"""MetroLine: Flask server exposing the doubly linked list as a JSON API."""

from flask import Flask, jsonify, render_template, request

from linked_list import DoublyLinkedList
from seed_data import INITIAL_STATIONS

app = Flask(__name__)

# Single global instance: the whole application state lives here (in Python).
metro_line = DoublyLinkedList()
for station_name, station_zone in INITIAL_STATIONS:
    metro_line.add_at_end(station_name, station_zone)


def success(message, status=200):
    """Build a success response with the current state of the line."""
    return jsonify({
        "ok": True,
        "message": message,
        "line": {
            "size": metro_line.size,
            "current": metro_line.current.name if metro_line.current else None,
            "head": metro_line.head.name if metro_line.head else None,
            "tail": metro_line.tail.name if metro_line.tail else None,
            "stations": metro_line.to_list_forward(),
        },
    }), status


def error(message, status=400):
    """Build an error response."""
    return jsonify({"ok": False, "message": message}), status


def validate_name(raw_name):
    """Return a clean station name or None if it is invalid."""
    if raw_name is None:
        return None
    name = str(raw_name).strip()
    if name == "" or len(name) > 30:
        return None
    return name


def validate_zone(raw_zone):
    """Return an integer zone (1-3) or None if it is invalid."""
    try:
        zone = int(raw_zone)
    except (TypeError, ValueError):
        return None
    if zone < 1 or zone > 3:
        return None
    return zone


@app.route("/")
def index():
    """Serve the frontend page."""
    return render_template("index.html")


@app.route("/api/line")
def get_line():
    """Return the full state of the line."""
    return success("Line state loaded")


@app.route("/api/stations", methods=["POST"])
def add_station():
    """Add a station at the start, the end or after another station."""
    body = request.get_json(silent=True) or {}
    name = validate_name(body.get("name"))
    zone = validate_zone(body.get("zone"))
    position = body.get("position", "end")

    if name is None:
        return error("Name is required and must be 1-30 characters")
    if zone is None:
        return error("Zone must be a number between 1 and 3")

    if position == "start":
        node = metro_line.add_at_start(name, zone)
        where = "at the start"
    elif position == "end":
        node = metro_line.add_at_end(name, zone)
        where = "at the end"
    elif position == "after":
        after = validate_name(body.get("after"))
        if after is None:
            return error("A valid 'after' station name is required")
        node = metro_line.add_after(after, name, zone)
        if node is None and metro_line.find(after) is None:
            return error("Target station '" + after + "' not found", 404)
        where = "after " + after
    else:
        return error("Position must be 'start', 'end' or 'after'")

    if node is None:
        return error("Station '" + name + "' already exists")
    return success("Station " + where + ": " + name)


@app.route("/api/stations/<name>", methods=["DELETE"])
def delete_station(name):
    """Remove a station by name."""
    clean_name = validate_name(name)
    if clean_name is None:
        return error("Invalid station name")
    if metro_line.find(clean_name) is None:
        return error("Station '" + clean_name + "' not found", 404)
    metro_line.remove(clean_name)
    return success("Station removed: " + clean_name)


@app.route("/api/stations/search")
def search_station():
    """Search a station and return it with its neighbours."""
    clean_name = validate_name(request.args.get("name"))
    if clean_name is None:
        return error("Query parameter 'name' is required")
    node = metro_line.find(clean_name)
    if node is None:
        return error("Station '" + clean_name + "' not found", 404)
    # locate the index by walking the list (keeps it simple and explicit)
    index = 0
    walker = metro_line.head
    while walker is not None and walker is not node:
        index += 1
        walker = walker.next
    body = {
        "ok": True,
        "message": "Station found: " + node.name,
        "line": {
            "size": metro_line.size,
            "current": metro_line.current.name if metro_line.current else None,
            "head": metro_line.head.name if metro_line.head else None,
            "tail": metro_line.tail.name if metro_line.tail else None,
            "stations": metro_line.to_list_forward(),
        },
        "found": metro_line.node_to_dict(node, index),
    }
    return jsonify(body), 200


@app.route("/api/train/next", methods=["POST"])
def train_next():
    """Move the train forward one station."""
    node = metro_line.move_next()
    if node is None:
        return error("The train is already at the last station")
    return success("Train moved to: " + node.name)


@app.route("/api/train/previous", methods=["POST"])
def train_previous():
    """Move the train backward one station."""
    node = metro_line.move_previous()
    if node is None:
        return error("The train is already at the first station")
    return success("Train moved to: " + node.name)


@app.route("/api/train/goto", methods=["POST"])
def train_goto():
    """Jump the train to a given station."""
    body = request.get_json(silent=True) or {}
    name = validate_name(body.get("name"))
    if name is None:
        return error("A valid station name is required")
    if metro_line.go_to(name) is False:
        return error("Station '" + name + "' not found", 404)
    return success("Train moved to: " + name)


@app.route("/api/line/reverse", methods=["POST"])
def reverse_line():
    """Reverse the direction of the whole line."""
    metro_line.reverse()
    return success("Line direction reversed")


@app.route("/api/line/backward")
def line_backward():
    """Walk the list from tail to head using prev (proves prev works)."""
    return jsonify({
        "ok": True,
        "message": "Backward traversal (tail -> head)",
        "line": {
            "size": metro_line.size,
            "current": metro_line.current.name if metro_line.current else None,
            "head": metro_line.head.name if metro_line.head else None,
            "tail": metro_line.tail.name if metro_line.tail else None,
            "stations": metro_line.to_list_forward(),
        },
        "backward": metro_line.to_list_backward(),
    }), 200


if __name__ == "__main__":
    app.run(debug=True)
