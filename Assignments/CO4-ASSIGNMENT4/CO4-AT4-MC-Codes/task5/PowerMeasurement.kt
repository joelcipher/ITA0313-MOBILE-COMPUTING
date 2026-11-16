// Instrument application-level wake/sync activity without forcing the CPU awake.
object PowerMeasurement {
    private const val TAG = "PowerMeasure"

    fun logEvent(event: String, detail: String) {
        Log.i(TAG, "time=${System.currentTimeMillis()} event=$event detail=$detail")
    }
}

// Design rules:
// - Persist sensor samples in batches.
// - Use WorkManager for deferrable uploads.
// - Avoid exact alarms for routine sync.
// - If a short wakelock is truly necessary, acquire it only around bounded work
//   and release it in finally; do not keep it for the whole shift.
// - Use platform sensor batching and fused location settings where suitable.
