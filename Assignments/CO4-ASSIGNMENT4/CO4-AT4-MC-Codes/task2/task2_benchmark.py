import argparse
import statistics
import time
from concurrent.futures import ThreadPoolExecutor

def work_chunk(values):
    # Deterministic CPU work; same function is used by both designs.
    total = 0
    for value in values:
        x = value
        for _ in range(20):
            x = (x * 1664525 + 1013904223) & 0xFFFFFFFF
        total += x
    return total

def chunks(data, count):
    size = max(1, (len(data) + count - 1) // count)
    return [data[i:i + size] for i in range(0, len(data), size)]

def sequential(data):
    return work_chunk(data)

def threaded(data, workers):
    parts = chunks(data, workers)
    with ThreadPoolExecutor(max_workers=workers) as pool:
        return sum(pool.map(work_chunk, parts))

def measure(fn, data, repeats):
    times, result = [], None
    for _ in range(repeats):
        start = time.perf_counter()
        result = fn(data)
        times.append((time.perf_counter() - start) * 1000)
    return statistics.median(times), result, times

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", type=int, default=250000)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--repeats", type=int, default=5)
    args = parser.parse_args()

    if args.size < 1 or args.workers < 1 or args.repeats < 1:
        raise SystemExit("size, workers and repeats must be positive")

    data = list(range(args.size))
    single_ms, single_result, single_runs = measure(sequential, data, args.repeats)
    multi_ms, multi_result, multi_runs = measure(
        lambda d: threaded(d, args.workers), data, args.repeats
    )

    print(f"input_items={args.size}, workers={args.workers}, repeats={args.repeats}")
    print(f"single_median_ms={single_ms:.3f}, runs={single_runs}")
    print(f"threaded_median_ms={multi_ms:.3f}, runs={multi_runs}")
    print(f"outputs_match={single_result == multi_result}")
    print("Note: Python CPU threads may not scale because of the CPython GIL.")
    print("Use Android Profiler/Perfetto for device CPU, PSS and frame-time evidence.")

if __name__ == "__main__":
    main()
