"""B2: Same-sized favourable and adversarial workloads using the B1 scheduler."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "B1_Background_Work"))
from background_simulation import WorkItem, DeviceState, run_scheduler, print_metrics

def build_workloads():
    favourable = [
        WorkItem(f"A{i}", priority=(5 if i in (2, 7) else 2),
                 critical=(i in (2, 7)), encrypted=True, size_kb=20)
        for i in range(1, 9)
    ]
    difficult = [
        WorkItem("B1", 5, True, True, True, 500),
        WorkItem("B2", 2, False, True, False, 2000),
        WorkItem("B3", 3, True, True, False, 900),
        WorkItem("B4", 4, True, True, True, 700),
        WorkItem("B5", 1, True, True, False, 1500),
        WorkItem("B6", 2, True, False, False, 100),
        WorkItem("B7", 3, True, True, False, 800),
        WorkItem("B8", 5, True, True, True, 400),
    ]
    return favourable, difficult

def main():
    good, hard = build_workloads()
    print("Prediction: Workload B should produce more deferrals and permanent rejections")
    print("because network, battery, Doze and security constraints are less favourable.")
    scenarios = [
        ("Workload A — favourable", good, DeviceState(80, "WIFI", False, True)),
        ("Workload B — adversarial", hard, DeviceState(18, "WEAK", True, True)),
    ]
    for title, items, state in scenarios:
        result = run_scheduler(items, state, "PRIORITY")
        print_metrics(title, result)

if __name__ == "__main__":
    main()
