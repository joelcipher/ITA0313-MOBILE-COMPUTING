MOBILE COMPUTING – ASSIGNMENT 5 (CO5)
PART B CODING PACKAGE

Contents
--------
B1_Background_Work/background_simulation.py
  Constraint-aware background work simulation. Includes FIFO and priority scheduling,
  three validation scenarios, state/constraint logs, counters and final backlog outcome.

B2_Adversarial_Workload/adversarial_workloads.py
  Two equal-sized eight-record workloads. Reuses the B1 scheduler to compare favourable
  and adversarial conditions.

B3_UI_Optimisation/ui_optimisation.py
  Exact enumeration and adaptive heuristic, four small test cases (including a counterexample),
  and operation-count scalability tests.

B4_Multimedia_Decision/multimedia_strategy.py
  Device-aware resolution/bitrate/upload-timing heuristic, sample device estimates and
  a deliberate counterexample.

How to run
----------
1. Extract this ZIP archive.
2. Install Python 3.9 or later. No third-party packages are required.
3. Open a terminal in the extracted folder.
4. Run all simulations:
       python run_all.py
5. Or run an individual task:
       python B1_Background_Work/background_simulation.py
       python B2_Adversarial_Workload/adversarial_workloads.py
       python B3_UI_Optimisation/ui_optimisation.py
       python B4_Multimedia_Decision/multimedia_strategy.py

Important academic/technical notes
----------------------------------
- The supplied assignment requires source code for Part B (B1-B4). Part A (A1-A5)
  requires language-independent pseudocode / architecture, not programming-language code.
- These are reproducible Python desktop simulations based on the supplied answer booklet's
  stated modelling assumptions. They do NOT run Android WorkManager, Android Services,
  real sensors, a physical camera, or a real backend.
- Battery and energy figures are explicitly estimates/proxies, not measured joules or
  physical-device battery readings.
- For B1/B2, successful upload means the simulation receives a server acknowledgement.
  Deferred work remains queued; invalid encryption/permission is rejected or cancelled.
- For a real Android implementation, adapt the decision rules to WorkManager, Android
  permissions, foreground-service restrictions, encrypted persistence, TLS and an
  authenticated backend. Do not present this desktop simulation as a native Android app.

Evidence to submit
------------------
For each task, retain:
- source code;
- test inputs and scenario assumptions;
- console output;
- instrumentation values;
- interpretation of what the measurements demonstrate.
Label all generated numerical results as simulation unless measured on a physical device.
