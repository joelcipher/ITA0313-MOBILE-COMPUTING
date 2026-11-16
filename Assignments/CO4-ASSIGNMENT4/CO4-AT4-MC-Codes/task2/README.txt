TASK 2 — SINGLE-THREAD VS MULTI-THREAD
--------------------------------------
Run: python task2_benchmark.py --size 250000 --repeats 5

The script compares:
A. sequential processing in one thread
B. a bounded ThreadPoolExecutor splitting the same workload

Use a large size to expose parallel overhead and a tiny size (e.g. 20) for the
counterexample. Python's GIL means CPU-bound Python threads may not speed up on
standard CPython; this is itself an important interpretation. For Android evidence,
use the Kotlin pattern below and Android Studio Profiler / Perfetto.
