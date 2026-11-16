TASK 5 — POWER MANAGEMENT
-------------------------
Use the Kotlin worker pattern to schedule non-urgent sync work with constraints.
Do not hold a partial wakelock continuously. Use foreground service only for a
user-visible, ongoing task that qualifies under current Android policy.

Measurement commands:
adb shell dumpsys batterystats --reset
# Run one controlled trial for a fixed interval.
adb shell dumpsys batterystats YOUR.PACKAGE.NAME
adb shell dumpsys power
adb shell dumpsys deviceidle
adb shell dumpsys jobscheduler
adb bugreport bugreport.zip

Compare baseline and modified trials on the same device, workload and duration.
