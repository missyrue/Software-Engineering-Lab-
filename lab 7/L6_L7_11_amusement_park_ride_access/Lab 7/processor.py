def validate_height_and_fastpass(rider_spec):
    if not isinstance(rider_spec, str):
        return "Invalid rider specification"
    parts = rider_spec.strip().split(':')
    if len(parts) != 2:
        return "Invalid rider specification"
    height_str, pass_str = (part.strip() for part in parts)
    if not height_str.isdecimal() or pass_str.upper() not in {"YES", "NO"}:
        return "Invalid rider specification"
    height = int(height_str)
    has_fastpass = pass_str.upper() == "YES"
    eligible = height >= 120
    status = "FastPass Priority" if has_fastpass else "Standard Entry"
    return f"Height {height}cm: {'Approved' if eligible else 'Denied'} ({status})"

def compute_dispatch_throughput(ride_metric_str):
    if not isinstance(ride_metric_str, str):
        return None
    parts = ride_metric_str.strip().split('/')
    if len(parts) != 2:
        return None
    riders_str, mins_str = (part.strip() for part in parts)
    try:
        riders = float(riders_str)
        cycle_mins = float(mins_str)
    except (TypeError, ValueError, OverflowError):
        return None
    if not (0 <= riders < float('inf')) or not (0 < cycle_mins < float('inf')):
        return None
    rate = riders / cycle_mins
    if not rate < float('inf'):
        return None
    return round(rate, 2)

def resolve_safety_restraint_code(zone_code):
    if not isinstance(zone_code, str):
        return "Unknown ride zone"
    prefix = zone_code.strip().upper()[:3]
    restraint_types = {
        "CST": "Over-the-Shoulder Harness",
        "WTR": "Lap Bar and Seatbelt",
        "DRP": "Hydraulic Shoulder Vest",
        "WHL": "Manual Safety Bar"
    }
    return restraint_types.get(prefix, "Unknown ride zone")

def main():
    print("==== Running validate_height_and_fastpass ====")
    r_input = input("Enter rider spec (Height:FastPass, e.g. 140:YES): ")
    print(validate_height_and_fastpass(r_input))

    print("\n==== Running compute_dispatch_throughput ====")
    t_input = input("Enter riders/mins (e.g. 48/2.5): ")
    print("Throughput (riders/min):", compute_dispatch_throughput(t_input))

    print("\n==== Running resolve_safety_restraint_code ====")
    z_input = input("Enter ride zone code (e.g. CST_01, WTR_A): ")
    print("Restraint:", resolve_safety_restraint_code(z_input))

if __name__ == "__main__":
    main()
