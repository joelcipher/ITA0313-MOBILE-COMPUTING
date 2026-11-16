TASK 6 — BATTERY-AWARE SECURE FIELD-TRACKING PROTOTYPE
-----------------------------------------------------
Run:
python task6/tracking_policy.py

The program simulates six conditions and prints:
- battery/network/motion/thermal state,
- selected sampling interval,
- upload action,
- whether encryption/TLS are mandatory,
- estimated energy units (illustrative model only).

It also runs a 3-case independent validation and a load/scalability loop.
The simulation does not encrypt real records or measure real mAh. Implement encryption
in the Android app using Android Keystore AES-GCM and use HTTPS for transport.
