TASK 3 — ART RUNTIME BENCHMARK AND FAILURE DETECTION
----------------------------------------------------
Add RuntimeBenchmark.kt to an Android app and call RuntimeBenchmark.runAll() from a
debug button. It measures a CPU loop and allocation workload. For UI-list rendering,
display a RecyclerView with a fixed dataset and capture frame timing using Android
Studio Profiler or Perfetto.

Useful commands (package name must be replaced):
adb shell am force-stop YOUR.PACKAGE.NAME
adb shell monkey -p YOUR.PACKAGE.NAME 1
adb shell dumpsys meminfo YOUR.PACKAGE.NAME
adb logcat -v time | grep -i -E 'art|gc|dalvik'
adb shell cmd package compile -m verify -f YOUR.PACKAGE.NAME
adb shell cmd package compile -m speed-profile -f YOUR.PACKAGE.NAME
adb shell cmd package compile -m speed -f YOUR.PACKAGE.NAME
adb shell cmd package compile --reset YOUR.PACKAGE.NAME

Compilation filters differ by Android version. Run only on your own test app/device.
