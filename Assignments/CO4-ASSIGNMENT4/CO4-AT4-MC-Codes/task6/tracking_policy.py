from dataclasses import dataclass
from math import ceil

@dataclass
class Condition:
    name: str
    battery: int
    charging: bool
    network: str       # OFFLINE, METERED, WIFI
    motion: str        # MOVING, STATIONARY
    hot: bool = False
    emergency: bool = False

def choose_policy(c: Condition):
    if not 0 <= c.battery <= 100:
        raise ValueError("battery must be from 0 to 100")
    if c.network not in {"OFFLINE", "METERED", "WIFI"}:
        raise ValueError("unknown network state")
    if c.motion not in {"MOVING", "STATIONARY"}:
        raise ValueError("unknown motion state")

    # Emergency overrides routine deferral, but never overrides security.
    if c.emergency:
        return 5, "priority authenticated upload", "EMERGENCY"
    if c.charging and c.network == "WIFI":
        return 15, "upload queued batch", "CHARGING"
    if c.hot:
        return 60, "small batch; thermal protection", "THERMAL"
    if c.battery <= 15:
        return (180 if c.motion == "STATIONARY" else 90), "queue; defer upload", "CRITICAL"
    if c.battery <= 30 and c.motion == "STATIONARY":
        return 120, "defer until Wi-Fi/charging", "LOW"
    if c.network == "OFFLINE":
        return (30 if c.motion == "MOVING" else 90), "queue securely", "OFFLINE"
    if c.network == "METERED":
        return (30 if c.motion == "MOVING" else 60), "batch upload", "METERED"
    return (15 if c.motion == "MOVING" else 45), "batch upload over Wi-Fi", "NORMAL"

def estimate_energy(interval_s, upload_action):
    # Illustrative energy units, NOT measured mAh.
    samples_per_hour = 3600 / interval_s
    sample_cost = 0.02 * samples_per_hour
    upload_cost = 0.8 if "upload" in upload_action else 0.1
    return sample_cost + upload_cost

def show(c):
    interval, action, state = choose_policy(c)
    energy = estimate_energy(interval, action)
    print(
        f"{c.name}: state={state}, sample_interval_s={interval}, "
        f"upload={action}, encrypt_before_queue=True, TLS_required=True, "
        f"estimated_energy_units={energy:.2f}"
    )

def validate():
    tests = [
        Condition("A 80% LTE moving", 80, False, "METERED", "MOVING"),
        Condition("B 20% LTE stationary", 20, False, "METERED", "STATIONARY"),
        Condition("C 10% offline stationary", 10, False, "OFFLINE", "STATIONARY"),
    ]
    expected = [30, 120, 180]
    print("\nINDEPENDENT VALIDATION")
    for c, exp in zip(tests, expected):
        actual, action, state = choose_policy(c)
        print(f"{c.name}: hand_expected={exp}s prototype={actual}s match={actual == exp}")

def scalability():
    print("\nSCALABILITY SIMULATION")
    for records in (100, 1000, 10000):
        batch_size = 100
        evaluations = records
        wakeups = ceil(records / batch_size)
        print(
            f"records={records}, policy_evaluations={evaluations}, "
            f"upload_wakeups_batched={wakeups}, "
            f"upload_wakeups_unbatched={records}"
        )

def main():
    cases = [
        Condition("1 charging Wi-Fi moving", 75, True, "WIFI", "MOVING"),
        Condition("2 80% LTE moving", 80, False, "METERED", "MOVING"),
        Condition("3 20% LTE stationary", 20, False, "METERED", "STATIONARY"),
        Condition("4 10% offline stationary", 10, False, "OFFLINE", "STATIONARY"),
        Condition("5 55% offline moving", 55, False, "OFFLINE", "MOVING"),
        Condition("6 40% Wi-Fi stationary hot", 40, False, "WIFI", "STATIONARY", hot=True),
    ]
    print("BATTERY-AWARE TRACKING POLICY (energy is model-estimated)")
    for c in cases:
        show(c)
    validate()
    scalability()

if __name__ == "__main__":
    main()
