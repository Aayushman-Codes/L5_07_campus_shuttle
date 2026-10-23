"""Campus shuttle timetable and fleet tracker.

Logs passenger counts per trip, computes average loads, flags under-used
routes and syncs the fleet data to a JSON file.
"""
import json
import secrets
from datetime import datetime

# Global state
routes = {"R1": {"name": "Main Gate - Library", "trips": []},
          "R2": {"name": "Hostel - Sports Complex", "trips": []},
          "R3": {"name": "Admin Block - Metro", "trips": []}}
MIN_CAPACITY = 10


def add_trip_log(route_id, passenger_count, logs=None):
    """Record a trip's passenger count and return the log list.

    Raises KeyError for an unknown route and ValueError if the count is
    not a non-negative integer.
    """
    if route_id not in routes:
        raise KeyError(f"Unknown route: {route_id}")
    if (not isinstance(passenger_count, int)
            or isinstance(passenger_count, bool) or passenger_count < 0):
        raise ValueError(
            f"Passenger count must be a non-negative integer, "
            f"got {passenger_count!r}")
    if logs is None:
        logs = []
    routes[route_id]["trips"].append(passenger_count)
    logs.append(f"{datetime.now()}: {route_id} carried {passenger_count}")
    return logs


def remove_route(route_id):
    """Delete a route from the fleet data."""
    del routes[route_id]


def average_load(route_id):
    """Return the average passengers per trip, or None if no trips exist."""
    trips = routes[route_id]["trips"]
    if not trips:
        return None
    return sum(trips) / len(trips)


def underused_routes():
    """Return the ids of routes whose average load is below MIN_CAPACITY."""
    flagged = []
    for r in routes:
        avg = average_load(r)
        if avg is not None and avg < MIN_CAPACITY:
            flagged.append(r)
    return flagged


def assign_driver():
    """Pick a driver at random."""
    drivers = ["Prakash", "Leela", "Imran", "Tom"]
    return secrets.choice(drivers)


def sync_fleet_data(file="fleet.json"):
    """Write the fleet data to a JSON file."""
    with open(file, "w", encoding="utf-8") as f:
        json.dump(routes, f)


def main():
    """Run the demo scenario."""
    add_trip_log("R1", 32)
    add_trip_log("R1", 28)
    add_trip_log("R2", 4)
    for bad_count in (-6, "full"):
        try:
            add_trip_log("R3", bad_count)
        except ValueError as err:
            print("Rejected trip:", err)
    print("Driver for R1:", assign_driver())
    print("Underused:", underused_routes())
    print("R1 average:", average_load("R1"))
    sync_fleet_data()
    remove_route("R3")
    choice = input("Route to look up (Enter for R2): ") or "R2"
    if choice in routes:
        print("Trips on", choice, ":", routes[choice]["trips"])
    else:
        print("Unknown route:", choice)
    if "R3" in routes:
        print("R3 average:", average_load("R3"))
    else:
        print("R3 has been removed; no average available.")


if __name__ == "__main__":
    main()
