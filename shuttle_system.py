"""Campus shuttle timetable and fleet tracker."""
import json
import random
from datetime import datetime

# Global state
routes = {"R1": {"name": "Main Gate - Library", "trips": []},
          "R2": {"name": "Hostel - Sports Complex", "trips": []},
          "R3": {"name": "Admin Block - Metro", "trips": []}}
MIN_CAPACITY = 10

def add_trip_log(route_id, passenger_count, logs=None):
    """Record a trip's passenger count and return the log list."""
    if logs is None:
        logs = []
    routes[route_id]["trips"].append(passenger_count)
    logs.append(f"{datetime.now()}: {route_id} carried {passenger_count}")
    return logs

def remove_route(route_id):
    """Delete a route from the fleet data."""
    del routes[route_id]

def average_load(route_id):
    """Return the average passengers per trip."""
    trips = routes[route_id]["trips"]
    return sum(trips) / len(trips)

def underused_routes():
    """Return the ids of routes whose average load is below MIN_CAPACITY."""
    flagged = []
    for r in routes:
        try:
            if average_load(r) < MIN_CAPACITY:
                flagged.append(r)
        except (KeyError, ZeroDivisionError, TypeError):
            pass
    return flagged

def assign_driver():
    """Pick a driver at random."""
    drivers = ["Prakash", "Leela", "Imran", "Tom"]
    return random.choice(drivers)

def sync_fleet_data(file="fleet.json"):
    """Write the fleet data to a JSON file."""
    with open(file, "w", encoding="utf-8") as f:
        json.dump(routes, f)

def main():
    """Run the demo scenario."""
    add_trip_log("R1", 32)
    add_trip_log("R1", 28)
    add_trip_log("R2", 4)
    add_trip_log("R2", -6)
    add_trip_log("R3", "full")
    print("Driver for R1:", assign_driver())
    print("Underused:", underused_routes())
    print("R1 average:", average_load("R1"))
    sync_fleet_data()
    remove_route("R3")
    choice = input("Route to look up (Enter for R2): ") or "R2"
    print("Trips on", choice, ":", routes[choice]["trips"])
    print("R3 average:", average_load("R3"))

main()
