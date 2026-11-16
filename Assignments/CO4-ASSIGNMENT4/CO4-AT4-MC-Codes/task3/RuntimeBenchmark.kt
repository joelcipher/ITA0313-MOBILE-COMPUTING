package com.example.mcassignment

import android.os.Debug
import android.os.SystemClock
import android.util.Log

object RuntimeBenchmark {
    private const val TAG = "RuntimeBench"

    data class Result(
        val workload: String,
        val durationMs: Long,
        val javaHeapUsedBytes: Long,
        val nativeHeapAllocatedBytes: Long
    )

    private fun snapshot(name: String, started: Long): Result {
        val runtime = Runtime.getRuntime()
        val used = runtime.totalMemory() - runtime.freeMemory()
        return Result(
            workload = name,
            durationMs = (SystemClock.elapsedRealtimeNanos() - started) / 1_000_000,
            javaHeapUsedBytes = used,
            nativeHeapAllocatedBytes = Debug.getNativeHeapAllocatedSize()
        )
    }

    fun cpuBound(iterations: Int = 5_000_000): Result {
        val start = SystemClock.elapsedRealtimeNanos()
        var checksum = 0L
        for (i in 1..iterations) {
            checksum += (i.toLong() * 31L) % 997L
        }
        Log.i(TAG, "cpu_checksum=$checksum")
        return snapshot("cpu-bound", start)
    }

    fun allocationHeavy(objects: Int = 200_000): Result {
        val start = SystemClock.elapsedRealtimeNanos()
        val list = ArrayList<ByteArray>(objects)
        repeat(objects) { list.add(ByteArray(128)) }
        Log.i(TAG, "allocated_objects=${list.size}")
        // Release references before observing post-GC heap in a separate measurement.
        list.clear()
        return snapshot("allocation-heavy", start)
    }

    fun runAll() {
        Log.i(TAG, "cpu=${cpuBound()}")
        Log.i(TAG, "allocation=${allocationHeavy()}")
    }
}
