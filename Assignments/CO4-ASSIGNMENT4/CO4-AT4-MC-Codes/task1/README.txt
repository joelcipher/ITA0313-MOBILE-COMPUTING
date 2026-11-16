TASK 1 — ANALYSE AND VALIDATE A MOBILE OS
-----------------------------------------
1) Run adb_commands.txt line by line in a terminal after enabling USB debugging.
2) Add LifecycleLogger.kt to an Android test app.
3) Launch the app, press Home, wait five minutes, return, and save logcat output.
4) For memory pressure, prefer a reduced-RAM AVD. 'am force-stop' is not a memory-pressure test.
5) Record PID before/after and the last lifecycle callback observed.
