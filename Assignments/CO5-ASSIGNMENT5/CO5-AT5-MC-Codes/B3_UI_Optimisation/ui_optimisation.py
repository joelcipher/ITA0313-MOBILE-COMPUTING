"""B3: Exact enumeration versus adaptive heuristic for a simplified feed renderer."""
from itertools import product

def cost_for(items, quality, cache):
    frame_penalty = sum(max(0, item["load"] / quality - cache) for item in items)
    energy = sum(item["load"] * quality * 0.7 for item in items) + cache * 2
    quality_penalty = sum((3 - quality) * item["importance"] for item in items)
    return frame_penalty * 5 + energy + quality_penalty

def exact_search(items, qualities=(1, 2, 3), caches=(1, 2, 3)):
    best, evaluated, item_evaluations = None, 0, 0
    for q, c in product(qualities, caches):
        evaluated += 1
        item_evaluations += len(items)
        value = cost_for(items, q, c)
        candidate = {"quality": q, "cache": c, "cost": value}
        if best is None or value < best["cost"]:
            best = candidate
    best.update(configurations_evaluated=evaluated,
                item_cost_evaluations=item_evaluations)
    return best

def adaptive(items):
    q, cache, changes = 2, 2, 0
    avg_load = sum(x["load"] for x in items) / max(1, len(items))
    if avg_load > 4:
        q, cache, changes = 1, 1, 2
    elif avg_load < 2:
        q, cache, changes = 3, 3, 2
    value = cost_for(items, q, cache)
    return {"quality": q, "cache": cache, "cost": value,
            "quality_cache_changes": changes,
            "item_scans": len(items), "cache_evictions": max(0, len(items)-cache)}

def run_tests():
    cases = {
        "Light feed": [{"load":1,"importance":1},{"load":1,"importance":2}],
        "Heavy feed": [{"load":6,"importance":1},{"load":5,"importance":1},{"load":6,"importance":2}],
        "Mixed feed": [{"load":1,"importance":5},{"load":6,"importance":1},{"load":2,"importance":4}],
        "Counter-example": [{"load":8,"importance":1}] + [{"load":1,"importance":8} for _ in range(5)]
    }
    print("B3 small-instance comparison")
    for name, items in cases.items():
        exact, approx = exact_search(items), adaptive(items)
        print(f"{name:18} exact=({exact['quality']},{exact['cache']}) cost={exact['cost']:.2f}; "
              f"adaptive=({approx['quality']},{approx['cache']}) cost={approx['cost']:.2f}; "
              f"match={abs(exact['cost']-approx['cost']) < 1e-9}")

def scalability():
    print("\nB3 scalability operation counts")
    print("items | exact configs | exact item evaluations | adaptive scans | adaptive changes")
    for n in (5, 20, 100, 500):
        items = [{"load": (i % 7) + 1, "importance": (i % 5) + 1} for i in range(n)]
        e, a = exact_search(items), adaptive(items)
        print(f"{n:5} | {e['configurations_evaluated']:13} | {e['item_cost_evaluations']:21} | "
              f"{a['item_scans']:14} | {a['quality_cache_changes']}")

if __name__ == "__main__":
    run_tests()
    scalability()
