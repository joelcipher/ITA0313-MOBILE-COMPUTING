"""B1: Constraint-aware background-work simulation.
Desktop simulation only; it does not execute Android WorkManager or access sensors.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class WorkItem:
    item_id: str
    priority: int
    encrypted: bool = True
    permission_valid: bool = True
    critical: bool = False
    size_kb: int = 20
    attempts: int = 0
    status: str = "QUEUED"

@dataclass
class DeviceState:
    battery: int = 80
    network: str = "WIFI"       # WIFI, GOOD_MOBILE, WEAK, OFFLINE
    doze: bool = False
    permission_valid: bool = True

@dataclass
class Metrics:
    enqueued: int = 0
    deferred: int = 0
    cancelled: int = 0
    successful: int = 0
    decisions: int = 0
    peak_workers: int = 0
    logs: List[str] = field(default_factory=list)

def feasible(item: WorkItem, state: DeviceState):
    if not item.encrypted:
        return "REJECT", "ciphertext/encryption validation failed"
    if not item.permission_valid or not state.permission_valid:
        return "CANCEL", "permission revoked"
    if state.network == "OFFLINE" or state.network == "WEAK":
        return "DEFER", "network unavailable or weak"
    if state.doze and not item.critical:
        return "DEFER", "Doze restricts noncritical work"
    if state.battery < 20 and not item.critical:
        return "DEFER", "battery below 20 percent"
    return "RUN", "constraints satisfied"

def run_scheduler(items: List[WorkItem], state: DeviceState, strategy="FIFO",
                  max_workers=2, acknowledge=True) -> Metrics:
    metrics = Metrics(enqueued=len(items))
    pending = list(items)
    if strategy == "PRIORITY":
        pending.sort(key=lambda x: (-int(x.critical), -x.priority, x.attempts, x.item_id))

    runnable = []
    for item in pending:
        metrics.decisions += 1
        action, reason = feasible(item, state)
        metrics.logs.append(f"{item.item_id}: {action} — {reason}; battery={state.battery}%, network={state.network}, doze={state.doze}")
        if action == "DEFER":
            item.status = "DEFERRED"; metrics.deferred += 1
        elif action in ("CANCEL", "REJECT"):
            item.status = action; metrics.cancelled += 1
        else:
            runnable.append(item)

    # Simulate bounded concurrent batches. Each batch represents workers that
    # may execute simultaneously; the pool never exceeds max_workers.
    for offset in range(0, len(runnable), max_workers):
        batch = runnable[offset:offset + max_workers]
        metrics.peak_workers = max(metrics.peak_workers, len(batch))
        for item in batch:
            item.attempts += 1
            if acknowledge:
                item.status = "ACKNOWLEDGED"; metrics.successful += 1
                metrics.logs.append(f"{item.item_id}: server acknowledgement received")
            else:
                item.status = "QUEUED"; metrics.deferred += 1
                metrics.logs.append(f"{item.item_id}: no acknowledgement; retained in durable queue")
    return metrics

def print_metrics(title, m):
    print(f"\n{title}")
    print("-" * len(title))
    for line in m.logs:
        print(line)
    print(f"Enqueued={m.enqueued}, decisions={m.decisions}, deferred={m.deferred}, cancelled/rejected={m.cancelled}, successful={m.successful}, peak_workers={m.peak_workers}")
    print("Final outcome:", "ALL DELIVERED" if m.successful == m.enqueued else f"RESIDUAL BACKLOG={m.enqueued-m.successful}")

def demo():
    items = [
        WorkItem("R1", 1), WorkItem("R2", 2), WorkItem("R3", 5, critical=True),
        WorkItem("R4", 3, encrypted=False), WorkItem("R5", 4),
        WorkItem("R6", 1), WorkItem("R7", 2), WorkItem("R8", 5, critical=True)
    ]
    scenarios = [
        ("Good connectivity and battery", DeviceState(80, "WIFI", False, True)),
        ("Doze / low battery", DeviceState(15, "WEAK", True, True)),
        ("Permission revoked mid-execution boundary", DeviceState(70, "WIFI", False, False)),
    ]
    for name, state in scenarios:
        for strategy in ("FIFO", "PRIORITY"):
            # Fresh records for each run
            cloned = [WorkItem(**vars(x)) for x in items]
            result = run_scheduler(cloned, state, strategy)
            print_metrics(f"{name} | {strategy}", result)

if __name__ == "__main__":
    demo()
