// Enable only in a debug build. Do not use penaltyDeath for this assignment demo.
if (BuildConfig.DEBUG) {
    StrictMode.setThreadPolicy(
        StrictMode.ThreadPolicy.Builder()
            .detectDiskReads()
            .detectDiskWrites()
            .detectNetwork()
            .penaltyLog()
            .build()
    )
}

// Controlled retained-reference demonstration (debug only):
// Keep a small list of ByteArray objects, observe heap growth in Memory Profiler,
// then clear the list. Do not allocate until the emulator becomes unstable.
